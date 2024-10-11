import logging
import os

env = os.environ.get("APP_ENV")

if env == "local":
    from ray import serve
    import requests

from fastapi import FastAPI, Query, HTTPException

from pydantic import BaseModel
from typing import Optional, List

env = os.environ.get("APP_ENV")
if env == "local":
    from configuration import configure_logging, configure_application
    from utils.constants import (APP_ENV,
                                 LLM_AI_AGENT_HOST,
                                 LLM_AI_AGENT_PORT)
    from core.llm_api_accessor import LlmApiAccessor
else:
    from .configuration import configure_logging, configure_application
    from .utils.constants import (APP_ENV,
                                 LLM_AI_AGENT_HOST,
                                 LLM_AI_AGENT_PORT)
    from .core.llm_api_accessor import LlmApiAccessor

class QueryRequest(BaseModel):
    prompt: str
    persona: Optional[str] = None


class QueryResponse(BaseModel):
    response: str

class IdeaQuery(BaseModel):
    query: str

class MatchedIdea(BaseModel):
    id: str
    sugBenefit: str
    sugChange: str
    sugCurrent: str
    sugSuggestionDate: str
    sugOrgDesc: str
    sugDenied: str
    sugImplement: str
    sugImplementationDate: str
    score: float

configure_logging()
configure_application()

logger = logging.getLogger(__name__)

app = FastAPI()


llm_api_host = os.environ.get(LLM_AI_AGENT_HOST)
llm_api_port = os.environ.get(LLM_AI_AGENT_PORT)
api_accessor = LlmApiAccessor(f'http://{llm_api_host}:{llm_api_port}')

@app.get("/echo")
async def echo(message: str = Query(None, alias="message")):
    logger.info(f"calling /echo with message={message}")
    return {"message": message}


@app.get("/health/readiness")
def health_check():
    logger.info(f"calling /health/readiness")
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):

    try:
        # Call the async function to query your AI model
        # construct json body
        json_body = request.json()
        logger.info(f"calling /query with {json_body}")
        response = api_accessor.post('/query', json_body)
        response_content = response.content
        return QueryResponse(response=response_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query AI model: {str(e)}")

@app.post("/idea_match", response_model=List[MatchedIdea])
async def idea_match(request: IdeaQuery):
    try:
        json_body = request.dict()  # Convert the Pydantic model to a dictionary
        logger.info(f"calling /idea_match with {json_body}")

        # Assuming api_accessor.post() is properly defined and returns a requests.Response object
        response = api_accessor.post('/idea_match', json=json_body)

        # Ensure the response is successful
        response.raise_for_status()

        # Parse the JSON content to Python objects (list of dicts)
        ideas = response.json()

        # Convert each dict in the list to your Pydantic model
        matched_ideas = [MatchedIdea(**idea) for idea in ideas]
        return matched_ideas
    except Exception as e:
        logger.exception("Failed to match ideas:", exc_info=e)
        raise HTTPException(status_code=500, detail=f"Failed to match ideas: {str(e)}")


@serve.deployment
@serve.ingress(app)
class FastAPIDeployment:
    pass


ray_inferencer_deployment = FastAPIDeployment.bind()


if env == "local":
    serve.run(ray_inferencer_deployment, route_prefix="/test-inference")
    resp = requests.get("http://localhost:8000/test-inference/echo?message=test")
    assert resp.json() == {'message': 'test'}
    print("verified and existing")
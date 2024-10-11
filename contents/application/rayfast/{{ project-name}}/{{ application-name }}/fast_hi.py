import logging

from fastapi import FastAPI
import os
env = os.environ.get("APP_ENV")

if env == "local":
    from ray import serve
    import requests

app = FastAPI()


@serve.deployment
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.get("/")
    def root(self):
        return "Hi, world!"


hi_fastapi = MyFastAPIDeployment.bind()

if env == "local":
    serve.run(hi_fastapi, route_prefix="/fast")
    resp = requests.get("http://localhost:8000/fast")
    assert resp.json() == "Hi, world!"
    print("verified and existing")

FROM anyscale/ray-llm:latest

ARG RAY_HOME="/home/ray"

ARG RAY_UID=1000
ARG RAY_GID=100

ARG RAY_API_DIR="${RAY_HOME}/api"

{% for item in application %}COPY --chown=${RAY_UID}:${RAY_GID} "./{{ item.application_name }}" "${RAY_API_DIR}/{{ item.application_name }}"
{% endfor %}


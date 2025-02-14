FROM python:3.12.8-slim-bookworm

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN getent group ${GROUP_ID} || groupadd -g ${GROUP_ID} app && \
useradd -m -l -u ${USER_ID} -g ${GROUP_ID} app
USER app

WORKDIR /home/app/actions/vertex_ai_pipeline

COPY --chmod=555 actions/vertex_ai_pipeline .

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python3", "vertex.py"]

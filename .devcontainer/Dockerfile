FROM mcr.microsoft.com/devcontainers/base:alpine
RUN apk add --no-cache python3 py3-pip
RUN python3 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv PATH="/opt/venv/bin:${PATH}"
RUN pip install pyinfra vdf

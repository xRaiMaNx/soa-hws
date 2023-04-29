FROM python:3.8-slim
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

CMD ["python", "-m", "proxy"]
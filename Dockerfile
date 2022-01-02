FROM python:3-slim AS build-env
COPY . /code
WORKDIR /code
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM python:3-slim
ENV LANG C.UTF-8
COPY --from=build-env /code /code
WORKDIR /code
VOLUME ./out
CMD python go_spider.py

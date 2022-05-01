FROM building5/gosu:1.10 AS gosu

FROM python:3.8 as dev

RUN apt update && apt install libssl-dev curl -y
COPY --from=gosu /gosu /usr/local/bin
RUN mkdir scripts
COPY ./scripts/entrypoint.sh ./scripts/entrypoint.sh
RUN ["chmod", "+x", "/scripts/entrypoint.sh"]
ENTRYPOINT ["/scripts/entrypoint.sh"]

FROM dev as prod
WORKDIR /app
RUN mkdir /app/src
COPY ./requirements.txt /app/requirements.txt
COPY ./src /app/src
COPY .gitignore /app/.gitignore 
RUN pip install -r /app/requirements.txt 
RUN ["chmod", "+x", "/scripts/entrypoint.sh"]
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["/scripts/entrypoint.sh"]



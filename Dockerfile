FROM python:3.11
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
EXPOSE 5432
ENTRYPOINT ["poetry" "run" "src/app.py" "--server.port=5432", "--server.adress.0.0.0.0"]
FROM python:3.11
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
CMD ["poetry", "run", "python", "src/app.py"]

FROM python:3.11.5
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["poetry", "run", "streamlit", "run", "src/app/app.py", "--server.port=8501", "--server.adress=0.0.0.0"]
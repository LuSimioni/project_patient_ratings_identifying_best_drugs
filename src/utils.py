import json
import os
import re
from pathlib import Path
import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine
from schema import ProdutoSchema

def load_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The DataFrame created from the CSV file.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, encoding ='utf-8')
        print(df)
        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is improperly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def load_settings():
    """Carrega as configurações a partir de variáveis de ambiente."""
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }
    return settings

def export_df_raw_to_sql() -> pd.DataFrame:

    settings = load_settings()


    # Criar a string de conexão com base nas configurações
    #connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    connection_string = os.getenv("DATABASE_URL")
    # Criar engine de conexão
    engine = create_engine(connection_string)
    
    with engine.connect() as conn, conn.begin():
        df = ingestion_raw_to_db()
        df.to_sql('tb_raw_reviews_all', con=conn, if_exists='replace', index=False)        
    return df


@pa.check_output(ProdutoSchema, lazy=True)
def export_df_work_to_sql() -> pd.DataFrame:

    settings = load_settings()


    # Criar a string de conexão com base nas configurações
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    # Criar engine de conexão
    engine = create_engine(connection_string)
    
    with engine.connect() as conn, conn.begin():
        df = ingestion_and_transform()
        df.to_sql('tb_work_reviews_all', con=conn, if_exists='replace', index=False)        
    return df    



def set_column_types(df: pd.DataFrame, json_file_path: str) -> pd.DataFrame:
    """
    Reads a JSON file specifying column types and applies them to the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to which column types will be applied.
    json_file_path (str): The path to the JSON file containing column types.

    Returns:
    pd.DataFrame: The DataFrame with updated column types.
    """
    try:
        # Load the JSON file
        with open(json_file_path, 'r') as file:
            column_types = json.load(file)
        
        # Iterate through the columns and apply types only if the column exists in the DataFrame

        for column in df:
            defined_type = column_types[column]
            if defined_type == 'string':
                df[column] = df[column].astype("string")
            elif defined_type == 'int':
                df[column] = df[column].astype("int")
        return df    
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from file '{json_file_path}'.")        


def camel_to_snake(column_name: str) -> str:
    """
    Converts a camelCase or PascalCase string to snake_case.
    
    Parameters:
    column_name (str): The original column name in camelCase or PascalCase.
    
    Returns:
    str: The column name converted to snake_case.
    """
    # Convert the camelCase/PascalCase to snake_case
    snake_case = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', column_name)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_case)
    return snake_case.lower()


def create_index_column(df:pd.DataFrame) -> pd.DataFrame:

    df.insert(0, 'id', df.index + 1)
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames all columns of a DataFrame from camelCase/PascalCase to snake_case.
    
    Parameters:
    df (pd.DataFrame): The DataFrame with columns to rename.
    
    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    df.columns = [camel_to_snake(col) for col in df.columns]
    df.drop(columns=['unnamed: 0'], inplace= True)
    create_index_column(df)

    return df

def ingestion_and_transform() -> pd.DataFrame:

    df_load_csv = load_csv_to_dataframe('assets/drugLibTrain_raw.csv')
    df_set_types = set_column_types(df_load_csv, 'config/column_types.json')
    df = rename_columns(df_set_types)

    return df

def ingestion_raw_to_db()-> pd.DataFrame:

    df = load_csv_to_dataframe('assets/drugLibTrain_raw.csv')

    return df
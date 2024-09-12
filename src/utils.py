import pandas as pd
import json
import re
import psycopg2
import os
from sqlalchemy import create_engine
from pathlib import Path
import pandera as pa
from dotenv import load_dotenv

def load_csv_to_dataframe(file_path):
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
        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file is improperly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def decode_dataframe(df):

    for col in df.select_dtypes(include=[object]):
        df[col] = df[col].apply(lambda x: x.encode('utf-8', errors='ignore').decode('utf-8') if isinstance(x, str) else x)

    return df

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

def extrair_do_sql(query: str) -> pd.DataFrame:
    """
    Extrai dados do banco de dados SQL usando a consulta fornecida.

    Args:
        query: A consulta SQL para extrair dados.

    Returns:
        Um DataFrame do Pandas contendo os dados extraídos.
    """
    settings = load_settings()

    # Criar a string de conexão com base nas configurações
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    # Criar engine de conexão
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
            df_crm = pd.read_sql(query, conn)

    return df_crm

def set_column_types(df, json_file_path):
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
        
        # Convert the JSON column types to pandas types and apply to DataFrame
        for column, col_type in column_types.items():
            if col_type == 'int':
                df[column] = df[column].astype(int)
            elif col_type == 'float':
                df[column] = df[column].astype(float)
            elif col_type in ['text', 'string']:
                df[column] = df[column].astype(str)
            elif col_type == 'bool':
                df[column] = df[column].astype(bool)
            else:
                print(f"Warning: Unknown type '{col_type}' for column '{column}'")
        
        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {json_file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: The JSON file is improperly formatted.")
    except KeyError as e:
        print(f"Error: Column {e} not found in DataFrame.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def camel_to_snake(column_name):
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


def create_index_column(df):

    df.insert(0, 'id', df.index + 1)
    return df

def rename_columns(df):
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

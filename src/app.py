import pandas as pd
from utils import rename_columns, load_csv_to_dataframe, set_column_types, decode_dataframe, extrair_do_sql
import os
from sqlalchemy import create_engine

df = load_csv_to_dataframe('assets/drugLibTrain_raw.csv')
# Convert all string columns in your DataFrame to UTF-8 and handle decoding errors
df = set_column_types(df, 'config/column_types.json')

df = pd.DataFrame(df)
print("Before renaming:")
print(df)

df = rename_columns(df)
print("\nAfter renaming:")
print(df)

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/patient_ratings_identifying_drugs")

df.to_sql('reviews_all', con=engine, if_exists='append', index=False)

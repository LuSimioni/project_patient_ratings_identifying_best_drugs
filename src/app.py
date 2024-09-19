import os
import pandas as pd
import pandera as pa

from utils import (exportar_df_para_sql, load_csv_to_dataframe, rename_columns,
                   set_column_types)

df = load_csv_to_dataframe('assets/drugLibTrain_raw.csv')
    # Convert all string columns in your DataFrame to UTF-8 and handle decoding errors
df = set_column_types(df, 'config/column_types.json')
df = rename_columns(df)
exportar_df_para_sql(df)

'''
schema_crm = pa.infer_schema(df)

with open("schema_crm.py", "w", encoding="utf-8") as arquivo:
    arquivo.write(schema_crm.to_script())
    
print(schema_crm)

'''
from utils import export_df_raw_to_sql, export_df_work_to_sql

if __name__ == "__main__":
    
    export_df_raw_to_sql()
    export_df_work_to_sql()
'''
schema_crm = pa.infer_schema(df)

with open("schema_crm.py", "w", encoding="utf-8") as arquivo:
    arquivo.write(schema_crm.to_script())
    
print(schema_crm)

'''
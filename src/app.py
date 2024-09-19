from utils import exportar_df_para_sql

if __name__ == "__main__":
    
    df = exportar_df_para_sql()
'''
schema_crm = pa.infer_schema(df)

with open("schema_crm.py", "w", encoding="utf-8") as arquivo:
    arquivo.write(schema_crm.to_script())
    
print(schema_crm)

'''
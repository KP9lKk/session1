import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel('export.xlsx')

df.info()
print(df.describe())
engine = create_engine('s')
df.to_sql(name="data", con=engine, if_exists="append")
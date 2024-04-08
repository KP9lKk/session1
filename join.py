
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
df_hh = pd.read_excel('hh_for_join.xlsx')
df_ros = pd.read_excel('rosnav_for_join.xlsx')

df = pd.concat([df_hh, df_ros])
df["description"] = df["description"].map(lambda x: BeautifulSoup(x, features="html.parser").get_text())
df = df.map(lambda x: str(x).lower() if isinstance(x, str) else x)
replace_dict = {
    "3-6": "от 3 до 6 лет",
    "0": "нет опыта",
    "1-3": "от 1 года до 3 лет",
    "6-": "более 6 лет"
}
df = df.drop_duplicates(subset="description")
df["experience"] = df["experience"].map(lambda x: replace_dict[x] if x in replace_dict.keys() else x)
df["published_at"] = df["published_at"].map(lambda x: datetime.fromisoformat(str(x)).date())

df.info()
df.to_excel("export.xlsx")
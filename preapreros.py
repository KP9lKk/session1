import pandas as pd
import base64

from numpy import NaN

df_ros = pd.read_excel("rosnav.xlsx")
rename_ros = {
    "Дата публикации": "published_at",
    "Описание вакансии": "description",
    "Отрасль деятельности":"industry",
    "Ключевые навыки":"key_skills",
    "Название региона":"area",
    "График работы": "schedule",
    "Опыт работы": "experience",
    "Заработная плата":"salary",
    "Вид трудоустройства":"employment",
    "Наличие тестового задания": "has_test"
}

df_ros.rename(columns=rename_ros, inplace=True)

df_ros["has_test"] = [True if "true" in has_test else False for has_test in df_ros["has_test"]]
df_ros["salary"] = [NaN if salary == 0 else salary for salary in  df_ros["salary"]]
mean = df_ros["salary"].mean()
df_ros["salary"] = df_ros["salary"].fillna(mean)

df_ros = df_ros.map(lambda x: str(x).lower() if isinstance(x, str) else x)

df_ros.to_excel("rosnav_for_join.xlsx")
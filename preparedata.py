import pandas as pd
import requests
import json

from numpy import NaN

from uttils import to_json_str, get_salary_value

df_hh = pd.read_excel("hh.xlsx")

# rename_ros = {
#     "Дата публикации": "published_at",
#     "Описание вакансии": "description",
#     "Отрасль деятельности":"industry",
#     "Ключевые навыки":"key_skills",
#     "Название региона":"area",
#     "График работы": "experience",
#     "Опыт работы": "experience",
#     "Заработная плата":"salary",
#     "Вид трудоустройства":"employment",
#     "Наличие тестового задания": "has_test"
# }

df_hh = df_hh[[
    "area",
    "salary",
    "published_at",
    "url",
    "snippet",
    "schedule",
    "experience",
    "employment",
    "employer",
    "has_test"
]]
df_hh["description"] = [json.loads(requests.get(url).text)["description"] for url in df_hh["url"]]
df_hh["industry"] = [json.loads(requests.get(url).text)["description"] for url in df_hh["url"]]
df_hh["employer"] = [
    json.loads(to_json_str(employer))
    for employer in df_hh["employer"]]
df_hh["industry"] = [
    json.loads(requests.get(employer_url["url"]).text)["industries"] if "url" in employer_url else None
    for employer_url in df_hh["employer"]
]
df_hh.to_excel("hh_with_industry.xlsx")
df_hh["description"] = [json.loads(requests.get(url).text)["description"] for url in df_hh["url"]]
df_hh.to_excel("hh_with_desc.xlsx")
df_hh = pd.read_excel("hh_with_desc.xlsx")
df_hh_ind = pd.read_excel("hh_with_industry.xlsx")
df_hh["industry"] = df_hh_ind["industry"]
df_hh.drop(columns=["employer", "url", "snippet"], inplace=True)
df_hh.rename(columns={"snippet": "key_skills"})

#можно заменить на массовый map
#df[["area", "schedule","employment","experience"]].map()
df_hh["area"] = [json.loads(to_json_str(area))["name"] for area in df_hh["area"]]
df_hh["schedule"] = [json.loads(to_json_str(schedule))["name"] for schedule in df_hh["schedule"]]
df_hh["employment"] = [json.loads(to_json_str(employment))["name"] for employment in df_hh["employment"]]
df_hh["experience"] = [json.loads(to_json_str(experience))["name"] for experience in df_hh["experience"]]

df_hh["industry"] = [";".join(map(lambda ind: ind["name"],json.loads(to_json_str(industry)))) if industry is not NaN else [] for industry in df_hh["industry"]]

df_hh["salary"] = [json.loads(to_json_str(salary)) if salary is not NaN else NaN for salary in df_hh["salary"]]

df_hh["salary"] = [get_salary_value(salary["to"], salary["from"]) if salary is not NaN else NaN for salary in df_hh["salary"]]
mean_salary = df_hh["salary"].mean()
df_hh["salary"] = df_hh["salary"].fillna(mean_salary)

df_hh.to_excel("hh_for_join.xlsx")


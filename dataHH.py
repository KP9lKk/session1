import requests
import pandas as pd
import json

hh_source = "https://api.hh.ru/vacancies"
params = {"page": 0,
          "per_page":100,
          "professional_role":
              "150",
          "date_from":"2024-01-07",
          "date_to":"2024-04-07",
          "area": "113"}
array_vacancy = []
result_query = json.loads(requests.get(hh_source, params).text)

pages = result_query["pages"]
array_vacancy.extend(result_query["items"])
for i in range(1, pages):
    params["page"] = i
    array_vacancy.extend(json.loads(
        requests.get(hh_source, params).text
    )["items"])

df = pd.DataFrame.from_dict(array_vacancy)
df.to_excel("hh.xlsx")
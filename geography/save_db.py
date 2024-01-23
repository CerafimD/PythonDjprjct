from collections import Counter

import pandas as pd

from hello.models import wage_amount_by_area_all


def SaveDataByArea():
    vacancies = reader_with_filters()

    wages_by_city = (vacancies.groupby("area_name")["salary"].mean().astype(int).to_frame().sort_values(
        by=["salary", "area_name"], ascending=[False, True]))["salary"]

    raw_amount_by_city = dict(count_amount_of_each_value("area_name", vacancies))
    raw_amount_by_city = dict([v for v in sorted(raw_amount_by_city.items(), key=lambda kv: (-kv[1], kv[0]))])
    total = sum(raw_amount_by_city.values(), 0.0)
    amount_by_city = {}
    s = 0
    for k, v in raw_amount_by_city.items():
        if round(v / total, 4) >= 0.01:
            s += v
            amount_by_city[k] = round(v / total, 4)
        else:
            wages_by_city = wages_by_city.drop(labels=k);
    amount_by_city["Другие"] = round(1 - (s / total), 4)

    wage_amount_by_area_all.objects.all().delete()
    wages_by_city = wages_by_city.to_dict()
    for city in wages_by_city.keys():
        wg = wage_amount_by_area_all(area_name=city, amount=amount_by_city[city], wage=wages_by_city[city])
        wg.save()
    sg = wage_amount_by_area_all(area_name="Другие", amount=amount_by_city["Другие"], wage=0)
    sg.save()

def reader_with_filters():
    vacancies = pd.read_csv('resources/vacancies.csv')
    vacancies = vacancies[vacancies["salary_currency"].str.contains("RUR", na=False)]
    vacancies["published_at"] = vacancies["published_at"].str[:4].astype(int)
    vacancies["salary_from"] = vacancies["salary_from"].fillna(vacancies["salary_to"])
    vacancies["salary_to"] = vacancies["salary_to"].fillna(vacancies["salary_from"])
    vacancies["salary"] = ((vacancies["salary_from"] + vacancies["salary_to"]) / 2)
    return vacancies

def count_amount_of_each_value(value_name, vacanciesname):
    values = vacanciesname[value_name]
    all_values = [value for value in values]
    counter = Counter(all_values)
    if value_name != "area_name":
        for i in range(2003, 2023):
            if i not in counter:
                counter[i] = 0
    return dict(sorted(counter.items()))

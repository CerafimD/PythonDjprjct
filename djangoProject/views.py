from django.shortcuts import render
from hello.models import new_vacancy
import pandas as pd
import sqlite3
# import matplotlib

#nmatplotlib.use('Agg')

#


def index_page(request):
    new_vacancy.objects.all().delete()
    return render(request, 'index.html')






def filter_name(vacancies):
    name = "java|ява|джава"
    vacancies_by_name = vacancies[vacancies["name"].str.contains(name, na=False, case=False, regex=True)]
    return vacancies_by_name


def download_from_db(table_name):
    try:
        conn = sqlite3.connect("db.sqlite3")
    except Exception as e:
        print(e)

    # Now in order to read in pandas dataframe we need to know table name
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
    conn.close()
    return df


def count_wage_by_value(vacanciesname, value):
    vacanciesname = vacanciesname[~vacanciesname.salary.isnull()]
    vacancies_years = (
        vacanciesname.groupby(value)["salary"].mean().astype(int).to_frame().sort_values(by="published_at",
                                                                                         ascending=True))[
        "salary"].to_dict()
    for i in range(2003, 2023):
        if i not in vacancies_years:
            vacancies_years[i] = 0
    return dict(sorted(vacancies_years.items()))


# def piechart(request):
#     return render(request, 'piechart.html')

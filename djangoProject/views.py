from django.shortcuts import render
from djangoProject import create_bargraph
from hello.models import wage_amount_by_years, SimpleTable, wage_amount_by_years_all, CitiesTable, new_vacancy
from hello.models import wage_amount_by_area_named, wage_amount_by_area_all
import pandas as pd
import sqlite3
import matplotlib

matplotlib.use('Agg')

from matplotlib import pyplot as plt
import numpy as np


def index_page(request):
    new_vacancy.objects.all().delete()
    return render(request, 'index.html')


def index_years(request):
    create_bargraph.create_bargraph("barchart")
    table = SimpleTable(wage_amount_by_years_all.objects.all(),
                        template_name="django_tables2/bootstrap-responsive.html")
    table2 = SimpleTable(wage_amount_by_years.objects.all())
    return render(request, 'востребованность.html', {"table": table, "table2": table2})


def index_geography(request):
    wage_amount_area_all = download_from_db("hello_wage_amount_by_area_all")
    wage_amount_area_named = download_from_db("hello_wage_amount_by_area_named")

    # breakpoint()

    # wage_by_year_by_name = count_wage_by_value(vacancies_by_name, "published_at")

    # amount_by_year = dict(count_amount_of_each_value("published_at", vacancies))
    # amount_by_year_by_name = dict(count_amount_of_each_value("published_at", vacancies_by_name))

    y_pos = np.arange(len(wage_amount_area_all.loc[:, "amount"]))

    fig, ax = plt.subplots(3, 1, sharex=False, sharey=False, constrained_layout=True)
    fig.set_figheight(10)
    fig.set_figwidth(7)

    ax[0].bar(y_pos + 0.2, wage_amount_area_all.loc[:, "wage"], width=0.4, align='center', alpha=0.5,
              label="средняя зп")
    ax[0].bar(y_pos - 0.2, wage_amount_area_named.loc[:, "wage"], width=0.4, align='center', alpha=0.5,
              label="cредняя зп Java разработчика")
    ax[0].set_xticks(y_pos, wage_amount_area_all.loc[:, "area_name"], rotation=90)
    ax[0].legend(fontsize=8)
    ax[0].set_ylabel("Средняя зарплата")
    ax[0].set_title("Средняя зарплата по городам")
    ax[1].pie(wage_amount_area_named.loc[:, "amount"], labels=wage_amount_area_named.loc[:, "area_name"],
              textprops={'fontsize': 8},
              shadow=True, startangle=90)
    ax[1].set_title("Процент вакансий Java разработчика по городам")
    ax[2].pie(wage_amount_area_all.loc[:, "amount"], labels=wage_amount_area_all.loc[:, "area_name"],
              textprops={'fontsize': 8},
              shadow=True, startangle=0)
    ax[2].set_title("Процент вакансий по городам")
    plt.tight_layout()
    plt.savefig(f'media/piechart.png')

    table = CitiesTable(wage_amount_by_area_all.objects.all(),
                        template_name="django_tables2/bootstrap-responsive.html")
    table2 = CitiesTable(wage_amount_by_area_named.objects.all())

    return render(request, 'География.html', {"table": table, "table2": table2})


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


def piechart(request):
    return render(request, 'piechart.html')

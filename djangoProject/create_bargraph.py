import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def create_bargraph(filename):
    wage_amount_all = download_from_db('hello_wage_amount_by_years_all')
    wage_amount_name = download_from_db('hello_wage_amount_by_years')
    # breakpoint()

    # wage_by_year_by_name = count_wage_by_value(vacancies_by_name, "published_at")

    # amount_by_year = dict(count_amount_of_each_value("published_at", vacancies))
    # amount_by_year_by_name = dict(count_amount_of_each_value("published_at", vacancies_by_name))

    y_pos = np.arange(len(wage_amount_all.loc[:, "amount"]))

    fig, ax = plt.subplots(2, 1, sharex=False, sharey=False)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    ax[0].bar(y_pos + 0.2, wage_amount_all.loc[:, "wage"], width=0.4, align='center', alpha=0.5, label="средняя зп")
    ax[0].bar(y_pos - 0.2, wage_amount_name.loc[:, "wage"], width=0.4, align='center', alpha=0.5,
              label="cредняя зп Java разработчика")
    ax[0].set_xticks(y_pos, wage_amount_all.loc[:, "year"], rotation=30)
    ax[0].legend(fontsize=8)
    ax[0].set_ylabel("Средняя зарплата")
    ax[0].set_title("Средняя зарплата по годам")
    ax[1].bar(y_pos + 0.2, wage_amount_all.loc[:, "amount"], width=0.4, align='center', alpha=0.5,
              label="Общее количество вакансий")
    ax[1].bar(y_pos - 0.2, wage_amount_name.loc[:, "amount"], width=0.4, align='center', alpha=0.5,
              label="Количество вакансий java разработчика")
    ax[1].set_xticks(y_pos, wage_amount_all.loc[:, "year"], rotation=30)
    ax[1].set_ylabel("Количество вакансий")
    ax[1].legend(fontsize=8)
    ax[1].set_title("Количество вакансий по годам")
    plt.tight_layout()
    plt.savefig(f'media/{filename}.png')


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

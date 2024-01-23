from collections import Counter

from django.shortcuts import render

from hello.models import CitiesTable, wage_amount_by_area_all, wage_amount_by_area_named


# Create your views here.
def index_geography(request):
    #wage_amount_area_all = download_from_db("hello_wage_amount_by_area_all")
    #wage_amount_area_named = download_from_db("hello_wage_amount_by_area_named")

    # breakpoint()
    #
    # wage_by_year_by_name = count_wage_by_value(vacancies_by_name, "published_at")
    #
    # amount_by_year = dict(count_amount_of_each_value("published_at", vacancies))
    # amount_by_year_by_name = dict(count_amount_of_each_value("published_at", vacancies_by_name))
    #
    # y_pos = np.arange(len(wage_amount_area_all.loc[:, "amount"]))
    #
    # fig, ax = plt.subplots(3, 1, sharex=False, sharey=False, constrained_layout=True)
    # fig.set_figheight(10)
    # fig.set_figwidth(7)
    #
    # ax[0].bar(y_pos + 0.2, wage_amount_area_all.loc[:, "wage"], width=0.4, align='center', alpha=0.5,
    #           label="средняя зп")
    # ax[0].bar(y_pos - 0.2, wage_amount_area_named.loc[:, "wage"], width=0.4, align='center', alpha=0.5,
    #           label="cредняя зп Java разработчика")
    # ax[0].set_xticks(y_pos, wage_amount_area_all.loc[:, "area_name"], rotation=90)
    # ax[0].legend(fontsize=8)
    # ax[0].set_ylabel("Средняя зарплата")
    # ax[0].set_title("Средняя зарплата по городам")
    # ax[1].pie(wage_amount_area_named.loc[:, "amount"], labels=wage_amount_area_named.loc[:, "area_name"],
    #           textprops={'fontsize': 8},
    #           shadow=True, startangle=90)
    # ax[1].set_title("Процент вакансий Java разработчика по городам")
    # ax[2].pie(wage_amount_area_all.loc[:, "amount"], labels=wage_amount_area_all.loc[:, "area_name"],
    #           textprops={'fontsize': 8},
    #           shadow=True, startangle=0)
    # ax[2].set_title("Процент вакансий по городам")
    # plt.tight_layout()
    # plt.savefig(f'media/piechart.png')

    table = CitiesTable(wage_amount_by_area_all.objects.all(),
                        template_name="django_tables2/bootstrap-responsive.html")
    table2 = CitiesTable(wage_amount_by_area_named.objects.all())

    return render(request, 'География.html', {"table": table, "table2": table2})


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

def count_amount_of_each_value(value_name, vacanciesname):
    values = vacanciesname[value_name]
    all_values = [value for value in values]
    counter = Counter(all_values)
    if value_name != "area_name":
        for i in range(2003, 2023):
            if i not in counter:
                counter[i] = 0
    return dict(sorted(counter.items()))
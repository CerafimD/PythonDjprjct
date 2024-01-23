from django.shortcuts import render

from hello.models import SimpleTable, wage_amount_by_years_all, wage_amount_by_years
from relevance import create_bargraph


# Create your views here.
def index_years(request):
    create_bargraph.create_bargraph("barchart")
    table = SimpleTable(wage_amount_by_years_all.objects.all(),
                        template_name="django_tables2/bootstrap-responsive.html")
    table2 = SimpleTable(wage_amount_by_years.objects.all())
    return render(request, 'востребованность.html', {"table": table, "table2": table2})

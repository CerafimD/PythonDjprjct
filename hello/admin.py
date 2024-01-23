from django.contrib import admin

# Register your models here.
from django.contrib import admin
from hello.models import new_vacancy, wage_amount_by_area_named, wage_amount_by_area_all, wage_amount_by_years_all, \
    wage_amount_by_years

admin.site.register(new_vacancy)
admin.site.register(wage_amount_by_area_named)
admin.site.register(wage_amount_by_area_all)
admin.site.register(wage_amount_by_years_all)
admin.site.register(wage_amount_by_years)
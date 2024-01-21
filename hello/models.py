from django.db import models
import django_tables2 as tables


class new_vacancy(models.Model):
    name = models.CharField(max_length=64)
    salary = models.IntegerField(null=True, blank=True)
    area_name = models.CharField(max_length=64)
    published_at = models.DateTimeField("время публикации", max_length=64)
    salary_currency = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class wage_amount_by_years(models.Model):
    year = models.IntegerField()
    wage = models.IntegerField()
    amount = models.IntegerField()


class wage_amount_by_years_all(models.Model):
    year = models.IntegerField()
    wage = models.IntegerField()
    amount = models.IntegerField()


class wage_amount_by_area_all(models.Model):
    area_name = models.CharField(max_length=64)
    wage = models.IntegerField()
    amount = models.FloatField()


class wage_amount_by_area_named(models.Model):
    area_name = models.CharField(max_length=64)
    wage = models.IntegerField()
    amount = models.FloatField()


class SimpleTable(tables.Table):
    year = tables.Column(attrs={"th": {"background-color": "#00FFFF"}})
    wage = tables.Column(attrs={"cell": {" background-color": "#00FFFF"}})
    amount = tables.Column(attrs={"cell": {" background-color": "#00FFFF"}})

    class Meta:
        attrs = {"class": "paleblue"}
        model = wage_amount_by_years
        template_name = "django_tables2/table.html"
        fields = ("year", "wage", "amount")
        row_attrs = {"style": lambda record: "border-width: 100px;"}


class CitiesTable(tables.Table):
    class Meta:
        model = wage_amount_by_area_all
        fields = ("area_name", "wage", "amount")
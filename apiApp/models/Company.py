from django.db import models


class Company(models.Model):
    company_id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

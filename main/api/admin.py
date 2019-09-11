from django.contrib import admin
from . import models

admin.site.register(models.Name)                # Названия
admin.site.register(models.Dorm)                # Общежития
admin.site.register(models.Floor)               # Этажи общежитий
admin.site.register(models.Room)                # Комнаты этажей
admin.site.register(models.Gender)              # Человеческий пол
admin.site.register(models.Status)              # Статус отчета
admin.site.register(models.Orphanage)           # Приюты
admin.site.register(models.Guardian)            # Опекуны
admin.site.register(models.Parent)              # Родители
admin.site.register(models.EducationalForm)     # Форма обучения
admin.site.register(models.Account)             # Аккаунты
admin.site.register(models.Report)              # Отчеты
admin.site.register(models.Request)             # Заявления

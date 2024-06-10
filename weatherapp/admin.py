from django.contrib import admin

from .models import Day
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("date", "temperature", "humidity", "wind_speed", "weather_description", "weather_image")
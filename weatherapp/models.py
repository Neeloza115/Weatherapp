from django.db import models

from django.db import models

class Day(models.Model):
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    uv_index = models.DecimalField(max_digits=5, decimal_places=2)
    weather_description = models.CharField(max_length=100)
    weather_image = models.CharField(max_length=100)
    
    
    def __str__(self) -> str:
        return f"{self.date} - Temperature: {self.temperature}°C, Humidity: {self.humidity}%, Wind Speed: {self.wind_speed} m/s, Description: {self.weather_description}, {self.weather_image}"
from django.db import models

# Create your models here.
class TempHum(models.Model):
    id = models.AutoField(primary_key=True)
    device_type = models.CharField(max_length=128, blank=True)
    temperature = models.FloatField(blank=False)
    humidity = models.FloatField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"TempHum (id={self.id}, t={self.temperature}, h={self.humidity}, ts={self.timestamp.strftime("%d-%m-%YT%H:%M:%S")})"
    
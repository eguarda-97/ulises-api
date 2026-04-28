import json
import datetime
import traceback

from django.shortcuts import render
from django.db.models import Max, Min
from django.db.models.functions import TruncDay
from django.http import JsonResponse, HttpRequest, HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey

from .models import TempHum
from .charts import temperature_24h_chart, temperature_weekly_chart, humidity_24h_chart, humidity_weekly_chart

# Create your views here.

# .../temp_hum/
def main_page(request: HttpRequest):
    try:
        if request.method == "GET":
            # Get weekly and last 24h data
            now = datetime.datetime.now()
            readings = TempHum.objects.filter(timestamp__gte=now.replace(hour=0, minute=0, second=0)-datetime.timedelta(hours=7*24)).order_by("timestamp")
            stats_weekly = (
                readings
                .annotate(day=TruncDay("timestamp"))
                .values("day")
                .annotate(
                    temp_max=Max("temperature"), 
                    temp_min=Min("temperature"), 
                    humi_max=Max("humidity"), 
                    humi_min=Min("humidity")
                )
                .order_by("day")
            )
            # for i in range(len(stats_weekly)):
            #     stats_weekly[i]["day"] = stats_weekly[i]["day"].strftime("%d-%m-%Y")
                

            readings_last_24h = readings.filter(timestamp__gte=now - datetime.timedelta(hours=24))
            last_24h_by_temp = readings_last_24h.order_by("-temperature")
            max_ts = last_24h_by_temp.first().timestamp - datetime.timedelta(hours=4)
            min_ts = last_24h_by_temp.last().timestamp - datetime.timedelta(hours=4)
            stats_24h = readings_last_24h.values("timestamp", "temperature", "humidity")
            # for i in range(len(stats_24h)):
            #     stats_24h[i]["timestamp"] = stats_24h[i]["timestamp"].strftime("%H:00")

            # Get plots for weekly and 24h
            timestamps_24h = [i["timestamp"]-datetime.timedelta(hours=4) for i in stats_24h]
            temp_24h = [i["temperature"] for i in stats_24h]
            humi_24h = [i["humidity"] for i in stats_24h]
            
            timestamps_weekly = [i["day"] for i in stats_weekly]
            temp_max = [i["temp_max"] for i in stats_weekly]
            temp_min = [i["temp_min"] for i in stats_weekly]
            humi_max = [i["humi_max"] for i in stats_weekly]
            humi_min = [i["humi_min"] for i in stats_weekly]

            temp_chart_24h = temperature_24h_chart(data=[temp_24h], timestamps=timestamps_24h)
            humi_chart_24h = humidity_24h_chart(data=[humi_24h], timestamps=timestamps_24h)
            temp_chart_weekly = temperature_weekly_chart(data=[temp_max, temp_min], timestamps=timestamps_weekly)
            humi_chart_weekly = humidity_weekly_chart(data=[humi_max, humi_min], timestamps=timestamps_weekly)
  
            return render(request, template_name="temp_hum/sensor_dashboard.html", 
                           context = {
                                "node_name": "Ulises 1",
                                "node_location": "Patio",
                                "node_id": "SN-0001",
                                "last_reading_time": (readings_last_24h.last().timestamp-datetime.timedelta(hours=4)).strftime("%d-%m-%Y %H:%M"),
                                "current_temp": round(temp_24h[-1], 1),
                                "current_humi": round(humi_24h[-1], 1),
                                "temp_max_24h": round(max(temp_24h), 1),
                                "temp_min_24h": round(min(temp_24h), 1),
                                "temp_max_time": max_ts.strftime("%H:%M"),
                                "temp_min_time": min_ts.strftime("%H:%M"),
                                "temp_chart_24h_json": temp_chart_24h,
                                "temp_chart_weekly_json": temp_chart_weekly,
                                "humi_chart_24h_json": humi_chart_24h,
                                "humi_chart_weekly_json": humi_chart_weekly,
                                "reading_interval": "20 min",
                            }
            )
        
    except:
        print(traceback.format_exc())
        return HttpResponse("An error ocurred >:(")

@api_view(["POST"])
@permission_classes([HasAPIKey])
def save_data(request: HttpRequest):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            
            print(data)
            temp_hum = TempHum(temperature=data["t"], humidity=data["h"])
            temp_hum.save()

            return JsonResponse({"result": "OK"})
        
        else:
            return JsonResponse({"result": "NOK", "msg": "Only POST method is allowed."})
    
    except:
        print(traceback.format_exc())
        return JsonResponse({"result": "NOK"})

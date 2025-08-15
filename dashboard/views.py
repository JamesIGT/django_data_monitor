from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    latitude = 19.4326
    longitude = -99.1332
    tz = "America/Mexico_City"
    tzEncoded = tz.replace("/", "%2F")
    api_url = settings.API_URL.format(
        latitude=latitude,
        longitude=longitude,
        tzEncoded=tzEncoded
    )
    try:
        response = requests.get(api_url, timeout=5)
        data_api = response.json()
        current = data_api.get("current", {})
        hourly = data_api.get("hourly", {})
        horas = hourly.get("time", [])[:24]
        temperaturas = hourly.get("temperature_2m", [])[:24]
        # Indicadores
        indicadores = []
        for ind in [
            {'nombre': 'Temperatura', 'clave': 'temperature_2m', 'umbral': 30, 'unidad': '°C'},
            {'nombre': 'Humedad relativa', 'clave': 'relative_humidity_2m', 'umbral': 70, 'unidad': '%'},
            {'nombre': 'Temperatura aparente', 'clave': 'apparent_temperature', 'umbral': 32, 'unidad': '°C'},
            {'nombre': 'Viento', 'clave': 'wind_speed_10m', 'umbral': 20, 'unidad': 'km/h'},
        ]:
            valor = current.get(ind['clave'], 'N/A')
            try:
                es_ok = float(valor) >= ind['umbral']
            except (ValueError, TypeError):
                es_ok = False
            indicadores.append({
                'nombre': ind['nombre'],
                'valor': valor,
                'umbral': ind['umbral'],
                'unidad': ind['unidad'],
                'es_ok': es_ok,
            })
        # Emparejar hora y temperatura para la tabla
        tabla_temp = list(zip(horas, temperaturas))
    except Exception:
        indicadores = [
            {'nombre': 'Temperatura', 'valor': 'Error', 'umbral': 30, 'unidad': '°C', 'es_ok': False},
            {'nombre': 'Humedad relativa', 'valor': 'Error', 'umbral': 70, 'unidad': '%', 'es_ok': False},
            {'nombre': 'Temperatura aparente', 'valor': 'Error', 'umbral': 32, 'unidad': '°C', 'es_ok': False},
            {'nombre': 'Viento', 'valor': 'Error', 'umbral': 20, 'unidad': 'km/h', 'es_ok': False},
        ]
        tabla_temp = []

    context = {
        'title': "Dashboard de Clima",
        'indicadores': indicadores,
        'horas': horas,
        'temperaturas': temperaturas,
        'tabla_temp': tabla_temp,
    }
    return render(request, 'dashboard/index.html', context)
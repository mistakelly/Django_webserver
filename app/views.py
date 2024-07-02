# HELP ME GOD.
from django.http import HttpRequest, JsonResponse
from ipware import get_client_ip
import requests
from django.conf import settings

def simpleserver(request: HttpRequest):
    # Get the client IP address
    client_ip, is_routable = get_client_ip(request)

    if client_ip is None or client_ip == '127.0.0.1':
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            client_ip = response.json().get('ip')

    if client_ip is None:
        return JsonResponse({"error": "Unable to get client IP"}, status=400)

    # get the client name
    client_name = request.GET.get("visitor_name", "Guest")

    # strip of quotation marks from the client name
    if client_name.startswith('"') and client_name.endswith('"'):
        client_name = client_name[1:-1]
        

    response = requests.get(f"https://get.geojs.io/v1/ip/geo/{client_ip}.json")

    if response.status_code != 200:
        return JsonResponse({"error": "Unable to get location"}, status=400)

    geo_data = response.json()
    client_city = geo_data.get("city", "Unknown location")

    # openweather API config
    weather_api_key = settings.OPENWEATHER_API_KEY
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = client_city
    API_KEY = weather_api_key

    weather_api_url = f"{BASE_URL}q={CITY}&appid={API_KEY}"
    weather_response = requests.get(weather_api_url).json()

    if "main" not in weather_response:
        return JsonResponse({"error": "Unable to get weather"}, status=400)

    client_city_temp = weather_response["main"].get("temp", "Unknown temperature")

    return JsonResponse(
        {
            "client_ip": client_ip,
            "location": client_city,
            "greeting": f"Hello, {client_name}!, the temperature is {str(client_city_temp)} degrees Celsius in {client_city}",
        },
        json_dumps_params={"indent": 4}
    )

# custom errors
def custom_404(request, exception):
    return JsonResponse({
        "error": "Page not found",
        "status_code": 404
    }, status=404)

def custom_500(request):
    return JsonResponse({
        "error": "Server error",
        "status_code": 500
    }, status=500)

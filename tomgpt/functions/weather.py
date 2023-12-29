"""
WeatherFunction provides current weather information by making API calls to a weather service. It supports various query parameters for flexible weather data retrieval.
"""

import os
from typing import Dict
from tomgpt.functions.chatfunction import ChatFunction
import json 
import requests

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

class WeatherFunction(ChatFunction):
    # https://www.weatherapi.com/
    @property
    def name(self) -> str:
        return "get_current_weather"

    @property
    def description(self) -> str:
        return "Get the current weather"

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Pass US Zipcode, UK Postcode, \
                        Canada Postalcode, IP address, Latitude/Longitude \
                        (decimal degree) or city name.",
                },
            }
        }
    
    def execute(self, **kwargs) -> Dict:
        params = {
            "q": kwargs["q"],
            "aqi": "yes",
            "key": WEATHER_API_KEY
        }

        response = requests.get(WEATHER_API_URL,
                                params=params)

        if response.status_code == 200:
            results = response.json()
            return {"weather": results}
        else:
            return {"error":
                    f"Request failed with status code: {response.status_code}"}

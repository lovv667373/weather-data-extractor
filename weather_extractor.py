import re
import requests
import unittest
from typing import List, Dict, Optional

class WeatherDataExtractor:
    def __init__(self):
        self.weather_pattern = re.compile(
            r'(?:температура|temp|t)[:\s]*([+-]?\d{1,3}(?:\.\d{1,2})?)\s*°?[CF]?'
            r'(?:.*?(?:влажность|humidity|hum)[:\s]*(\d{1,3})\s*%)?'
            r'(?:.*?(?:давление|pressure|press)[:\s]*(\d{3,4})\s*(?:hPa|мм|mm))?'
            r'(?:.*?(?:ветер|wind)[:\s]*(\d{1,3}(?:\.\d{1,2})?)\s*(?:м/с|km/h|mph))?'
            r'(?:.*?(?:описание|description|weather)[:\s]*([а-яА-Яa-zA-Z\s]+))?',
            re.IGNORECASE
        )
    
    def extract_weather_data(self, text: str) -> Optional[Dict[str, str]]:
        match = self.weather_pattern.search(text)
        if not match:
            return None
        
        groups = match.groups()
        weather_data = {}
        
        if groups[0]: weather_data['temperature'] = groups[0]
        if len(groups) > 1 and groups[1]: weather_data['humidity'] = groups[1]
        if len(groups) > 2 and groups[2]: weather_data['pressure'] = groups[2]
        if len(groups) > 3 and groups[3]: weather_data['wind_speed'] = groups[3]
        if len(groups) > 4 and groups[4]: weather_data['description'] = groups[4].strip()
        
        return weather_data if weather_data else None

if __name__ == "__main__":
    extractor = WeatherDataExtractor()
    test_text = "Температура: 25°C, влажность: 65%"
    result = extractor.extract_weather_data(test_text)
    print(f"Результат: {result}")
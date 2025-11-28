import unittest
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_extractor import WeatherDataExtractor


class TestWeatherExtractor(unittest.TestCase):
    """
    Unit-тесты для проверки корректности работы регулярного выражения
    """
    
    def setUp(self):
        self.extractor = WeatherDataExtractor()
    
    def test_temperature_extraction(self):
        """Тест извлечения температуры"""
        text = "Температура: 25°C"
        result = self.extractor.extract_weather_data(text)
        self.assertIsNotNone(result)
        self.assertEqual(result['temperature'], '25')
    
    def test_complete_data(self):
        """Тест извлечения полных данных о погоде"""
        text = "Температура: 22°C, влажность: 65%, давление: 1013 hPa, ветер: 5 м/с, ясно"
        result = self.extractor.extract_weather_data(text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['temperature'], '22')
        self.assertEqual(result['humidity'], '65')
        self.assertEqual(result['pressure'], '1013')
        self.assertEqual(result['wind_speed'], '5')
        self.assertEqual(result['description'], 'ясно')
    
    def test_multiple_entries(self):
        """Тест множественных записей"""
        text = """
        Утром: температура 18°C, влажность 75%
        Днем: температура 25°C, влажность 50%, ветер 3 м/с
        """
        results = self.extractor.extract_multiple_weather_data(text)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['temperature'], '18')
        self.assertEqual(results[1]['temperature'], '25')
    
    def test_negative_temperature(self):
        """Тест отрицательной температуры"""
        text = "Температура: -15°C, влажность 80%"
        result = self.extractor.extract_weather_data(text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['temperature'], '-15')
        self.assertEqual(result['humidity'], '80')
    
    def test_no_weather_data(self):
        """Тест отсутствия данных о погоде"""
        text = "Сегодня был прекрасный день для прогулки в парке."
        result = self.extractor.extract_weather_data(text)
        self.assertIsNone(result)
    
    def test_english_text(self):
        """Тест английского текста"""
        text = "Weather: temperature 72°F, humidity 60%"
        result = self.extractor.extract_weather_data(text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['temperature'], '72')
        self.assertEqual(result['humidity'], '60')
    
    def test_file_loading(self):
        """Тест загрузки данных из файла"""
        # Создадим временный файл для тестирования
        test_content = "Температура: 20°C, влажность: 70%"
        test_filename = "test_temp_file.txt"
        
        try:
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            results = self.extractor.load_and_analyze_file(test_filename)
            self.assertGreater(len(results), 0)
            self.assertEqual(results[0]['temperature'], '20')
            
        finally:
            # Удаляем временный файл
            if os.path.exists(test_filename):
                os.remove(test_filename)
    
    def test_alternative_formats(self):
        """Тест альтернативных форматов данных"""
        test_cases = [
            ("t: 25°C", "25"),
            ("temp: -5", "-5"),
            ("температура +30.5", "30.5"),
        ]
        
        for text, expected_temp in test_cases:
            with self.subTest(text=text):
                result = self.extractor.extract_weather_data(text)
                self.assertIsNotNone(result)
                self.assertEqual(result['temperature'], expected_temp)


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_extractor import WeatherDataExtractor

class TestWeatherExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = WeatherDataExtractor()
    
    def test_temperature_extraction(self):
        text = "Температура: 25°C"
        result = self.extractor.extract_weather_data(text)
        self.assertIsNotNone(result)
        self.assertEqual(result['temperature'], '25')
    
    def test_complete_data(self):
        text = "Температура: 22°C, влажность: 65%, давление: 1013 hPa, ветер: 5 м/с, ясно"
        result = self.extractor.extract_weather_data(text)
        self.assertEqual(result['temperature'], '22')
        self.assertEqual(result['humidity'], '65')
        self.assertEqual(result['pressure'], '1013')
        self.assertEqual(result['wind_speed'], '5')
        self.assertEqual(result['description'], 'ясно')

if __name__ == '__main__':
    unittest.main()
    class WeatherCLI:
    def __init__(self):
        self.extractor = WeatherDataExtractor()
    
    def run(self):
        print("=== Анализатор данных о погоде ===")
        print("1. Ввод текста вручную")
        print("2. Загрузить из файла")
        print("3. Выход")
        
        while True:
            choice = input("\nВыберите опцию (1-3): ").strip()
            
            if choice == '1':
                self.handle_manual_input()
            elif choice == '2':
                self.handle_file_input()
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def handle_manual_input(self):
        text = input("Введите текст с данными о погоде: ")
        result = self.extractor.extract_weather_data(text)
        
        if result:
            print("\nНайдены данные о погоде:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("Данные о погоде не найдены.")

def main():
    cli = WeatherCLI()
    cli.run()

if __name__ == "__main__":
    main()
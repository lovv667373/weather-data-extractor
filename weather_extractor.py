import re
import requests
import unittest
from typing import List, Dict, Optional

class WeatherDataExtractor:
    """
    Класс для извлечения данных о погоде с использованием регулярных выражений
    """
    
    def __init__(self):
        # Регулярное выражение для поиска данных о погоде
        self.weather_pattern = re.compile(
            r'(?:температура|temp|t)[:\s]*([+-]?\d{1,3}(?:\.\d{1,2})?)\s*°?[CF]?'  # температура
            r'(?:.*?(?:влажность|humidity|hum)[:\s]*(\d{1,3})\s*%)?'  # влажность
            r'(?:.*?(?:давление|pressure|press)[:\s]*(\d{3,4})\s*(?:hPa|мм|mm))?'  # давление
            r'(?:.*?(?:ветер|wind)[:\s]*(\d{1,3}(?:\.\d{1,2})?)\s*(?:м/с|km/h|mph))?'  # скорость ветра
            r'(?:.*?(?:описание|description|weather)[:\s]*([а-яА-Яa-zA-Z\s]+))?',  # описание
            re.IGNORECASE
        )
    
    def extract_weather_data(self, text: str) -> Optional[Dict[str, str]]:
        """
        Извлекает данные о погоде из текста
        """
        match = self.weather_pattern.search(text)
        
        if not match:
            return None
        
        groups = match.groups()
        weather_data = {}
        
        if groups[0]:
            weather_data['temperature'] = groups[0]
        if len(groups) > 1 and groups[1]:
            weather_data['humidity'] = groups[1]
        if len(groups) > 2 and groups[2]:
            weather_data['pressure'] = groups[2]
        if len(groups) > 3 and groups[3]:
            weather_data['wind_speed'] = groups[3]
        if len(groups) > 4 and groups[4]:
            weather_data['description'] = groups[4].strip()
        
        return weather_data if weather_data else None
    
    def extract_multiple_weather_data(self, text: str) -> List[Dict[str, str]]:
        """
        Извлекает все упоминания о погоде из текста
        """
        matches = self.weather_pattern.finditer(text)
        results = []
        
        for match in matches:
            groups = match.groups()
            weather_data = {}
            
            if groups[0]:
                weather_data['temperature'] = groups[0]
            if len(groups) > 1 and groups[1]:
                weather_data['humidity'] = groups[1]
            if len(groups) > 2 and groups[2]:
                weather_data['pressure'] = groups[2]
            if len(groups) > 3 and groups[3]:
                weather_data['wind_speed'] = groups[3]
            if len(groups) > 4 and groups[4]:
                weather_data['description'] = groups[4].strip()
            
            if weather_data:
                results.append(weather_data)
        
        return results
    
    def load_and_analyze_file(self, filename: str) -> List[Dict[str, str]]:
        """
        Загружает файл и анализирует данные о погоде
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return self.extract_multiple_weather_data(content)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

class WeatherCLI:
    """
    Класс для пользовательского интерфейса
    """
    
    def __init__(self):
        self.extractor = WeatherDataExtractor()
    
    def run(self):
        """Запуск интерфейса командной строки"""
        print("=== Анализатор данных о погоде ===")
        print("1. Ввод текста вручную")
        print("2. Загрузить из файла")
        print("3. Выход")
        
        while True:
            try:
                choice = input("\nВыберите опцию (1-3): ").strip()
                
                if choice == '1':
                    self.handle_manual_input()
                elif choice == '2':
                    self.handle_file_input()  # Вот этот метод!
                elif choice == '3':
                    print("Выход из программы.")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    
            except KeyboardInterrupt:
                print("\nВыход из программы.")
                break
            except Exception as e:
                print(f"Произошла ошибка: {e}")
    
    def handle_manual_input(self):
        """Обработка ручного ввода текста"""
        print("\n--- Ручной ввод ---")
        text = input("Введите текст с данными о погоде: ")
        
        if not text.strip():
            print("Текст не может быть пустым.")
            return
        
        results = self.extractor.extract_multiple_weather_data(text)
        
        if results:
            print(f"\nНайдено {len(results)} записей о погоде:")
            for i, data in enumerate(results, 1):
                print(f"\nЗапись {i}:")
                for key, value in data.items():
                    print(f"  {key}: {value}")
        else:
            print("Данные о погоде не найдены.")
    
    def handle_file_input(self):
        """
        Обработка ввода из файла
        Этот метод позволяет пользователю загрузить файл и проанализировать его содержимое
        """
        print("\n--- Загрузка из файла ---")
        filename = input("Введите имя файла: ").strip()
        
        if not filename:
            print("Имя файла не может быть пустым.")
            return
        
        # Анализируем файл
        results = self.extractor.load_and_analyze_file(filename)
        
        if results:
            print(f"\nНайдено {len(results)} записей о погоде в файле '{filename}':")
            for i, data in enumerate(results, 1):
                print(f"\nЗапись {i}:")
                for key, value in data.items():
                    print(f"  {key}: {value}")
        else:
            print(f"Данные о погоде не найдены в файле '{filename}'.")


def main():
    """Основная функция программы"""
    cli = WeatherCLI()
    cli.run()


if __name__ == "__main__":
    main()
    
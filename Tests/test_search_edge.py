from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from Utils.logger_setup import Logger


class TestSearchFunctionalityEdge:
    @pytest.fixture(scope="class")
    def driver(self):
        # Настройка опций для Edge
        options = Options()
        
        # Инициализация WebDriver
        Logger.add_message("Инициализация WebDriver для Microsoft Edge")
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        yield driver
        Logger.add_message("Закрытие WebDriver")
        driver.quit()

    def test_search(self, driver):
        """Шаг 1: Открытие веб-сайта"""

        url = "https://www.python.org/"
        Logger.add_message(f"Открытие веб-сайта: {url}")
        driver.get(url)

        """Шаг 2: Поиск по ключевому слову"""
        try:
            search_field = driver.find_element(By.NAME, "q")
            keyword = "Selenium"
            Logger.add_message(f"Ввод ключевого слова: {keyword}")
            search_field.send_keys(keyword)
            search_field.send_keys(Keys.RETURN)
        except Exception as e:
            Logger.add_message(f"Ошибка при выполнении поиска: {e}")
            raise

        """Шаг 3: Проверка результатов"""
        try:
            results = driver.find_elements(By.CSS_SELECTOR, '.list-recent-events li')
            num_results = len(results)
            Logger.add_message(f"Найдено результатов: {num_results}")
            assert num_results > 0, "Результаты поиска не найдены."

            for result in results:
                text = result.text.lower()
                Logger.add_message(f"Проверка результата: {text}")
                assert keyword.lower() in text, (
                    f"Ключевое слово '{keyword}' не найдено в результате: '{text}'"
                )

            Logger.add_message("Тест пройден: Все результаты содержат ключевое слово.")
            print("Тест пройден: Все результаты содержат ключевое слово.")
        except AssertionError as e:
            Logger.add_message(f"Тест провален: {e}")
            raise
        except Exception as e:
            Logger.add_message(f"Ошибка при проверке результатов: {e}")
            raise

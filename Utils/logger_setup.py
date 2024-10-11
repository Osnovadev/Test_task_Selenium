import datetime
import os
""" Создание логов"""
class Logger:

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(base_dir, 'logs')

    file_name = os.path.join(logs_dir, f'log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

    @classmethod
    def create_log_dir(cls):
        if not os.path.exists(cls.logs_dir):
            os.makedirs(cls.logs_dir)

    @classmethod
    def write_log_to_file(cls, data: str):
        cls.create_log_dir()
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def get_current_test_name(cls):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')
        if test_name:
            test_name = test_name.split(' ')[0]
        else:
            test_name = 'Unknown Test'
        return test_name

    @classmethod
    def add_message(cls, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = cls.get_current_test_name()
        data_to_add = f'[{timestamp}] [{test_name}] {message}\n'
        cls.write_log_to_file(data_to_add)

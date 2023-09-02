import csv
import os
from enum import Enum
from weatherman_records import WeatherRecord


class Month(Enum):
    Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec = range(1, 13)


class DataReader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.file_names = None
        self.discover_text_files()

    def read_year_data(self, year):
        for i in range(1, 13):
            month_name = Month(i).name
            monthly_data = self.read_monthly_data(year, month_name)

            for data in year_data:
                yield data

    def read_monthly_data(self, year, month_name):
        file_name = f"Murree_weather_{year}_{month_name}.txt"

        if file_name in self.file_names:
            month_data = self.read_file(file_name)

            for data in month_data:
                yield data

    def read_file(self, file_name):
        file_path = self.data_path + "/" + file_name

        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                yield WeatherRecord.from_dict(row)

    def discover_text_files(self):
        self.file_names = [
            file_name
            for file_name in os.listdir(self.data_path)
            if file_name.endswith(".txt")
        ]


def get_month_name(index):
    try:
        if index[0] == "0":
            index = index[1:]

        month_name = Month(int(index)).name
        return month_name
    except ValueError:
        print("Invalid month")
        return None

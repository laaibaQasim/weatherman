from abc import ABC, abstractmethod
from weatherman_results import draw_bar_chart
from weatherma_reader import DataReader, get_month_name
from weatherman_calculator import (
    StatsCollector,
    BarChartCalculator,
    MaxTempCalculator,
    MinTempCalculator,
    MaxHumidityCalculator,
    AvgMaxTempCalculator,
    AvgMinTempCalculator,
    AvgMeanHumidityCalculator,
)


class WeathermanCommands(ABC):
    def __init__(self, year, month=None):
        self.month = month
        self.year = year

    @abstractmethod
    def execute(self, data_path):
        pass

    @abstractmethod
    def data_found(self, data):
        pass


class YearlyReportCommand(WeathermanCommands):
    def data_found(self, data):
        return data.value is not None

    def execute(self, data_path):
        print("\n", self.year)
        sc_year = StatsCollector(
            MaxTempCalculator, MinTempCalculator, MaxHumidityCalculator
        )
        reader = DataReader(data_path)
        records = reader.read_year_data(self.year)

        for record in records:
            sc_year.update_stats(record)

        if not self.data_found(sc_year.calculators["MaxTempCalculator"]):
            print("no data found")
            return

        stats = sc_year.get_stats()
        print("highest: ", stats["MaxTempCalculator"])
        print("lowest: ", stats["MinTempCalculator"])
        print("humidity: ", stats["MaxHumidityCalculator"])


class MonthlyReportCommand(WeathermanCommands):
    def data_found(self, data):
        return data.count != 0

    def execute(self, data_path):
        print("\n", self.year)
        sc_monthly = StatsCollector(
            AvgMeanHumidityCalculator, AvgMaxTempCalculator, AvgMinTempCalculator
        )
        reader = DataReader(data_path)
        records = reader.read_monthly_data(self.year, get_month_name(self.month))

        for record in records:
            sc_monthly.update_stats(record)

        if not self.data_found(sc_monthly.calculators["AvgMaxTempCalculator"]):
            print("no data found")
            return

        stats = sc_monthly.get_stats()
        print("Highest Average: ", stats["AvgMaxTempCalculator"], "C")
        print("Lowest Average: ", stats["AvgMinTempCalculator"], "C")
        print("Average Mean Humidity: ", stats["AvgMeanHumidityCalculator"], "%")


class DailyReportCommand(WeathermanCommands):
    def data_found(self, data):
        return data.max_temperature != []

    def execute(self, data_path):
        print("\n", self.year)
        sc_daily = StatsCollector(BarChartCalculator)
        reader = DataReader(data_path)
        records = reader.read_monthly_data(self.year, get_month_name(self.month))

        for record in records:
            sc_daily.update_stats(record)

        if not self.data_found(sc_daily.calculators["BarChartCalculator"]):
            print("no data found")
            return

        stats = sc_daily.get_stats()

        draw_bar_chart(stats["BarChartCalculator"], "one")
        draw_bar_chart(stats["BarChartCalculator"], "two")

class StatsCollector:
    def __init__(self, *calculator_classes):
        self.calculators = dict()

        for class_ in calculator_classes:
            self.calculators[class_.__name__] = class_()

    def update_stats(self, record):
        for calculator in self.calculators.values():
            calculator.update(record)

    def get_stats(self):
        stats = {
            stats_class_name: sc_calc.get_answer()
            for stats_class_name, sc_calc in self.calculators.items()
        }
        return stats


class AvgCalculator:
    def __init__(self, key):
        self.sum_ = 0
        self.count = 0
        self.get_value_from_record = key

    def update(self, record):
        new_sum = self.get_value_from_record(record)
        if new_sum is not None:
            self.sum_ += new_sum
            self.count += 1

    def get_answer(self):
        return self.sum_ // self.count if self.count != 0 else 0


class Calculator:
    def __init__(self, keys):
        self._value = None
        self._timestamp = None
        self._get_values_from_record = keys

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            if self._value is not None:
                comparison_lambda = self._get_values_from_record[1](
                    self._value, new_value
                )
                if comparison_lambda:
                    self._value = int(new_value)
            else:
                self._value = int(new_value)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if timestamp is not None:
            self._timestamp = timestamp

    def update(self, record):
        new_value = self._get_values_from_record[0](record)
        self.value = new_value
        if self.value == new_value:
            self.timestamp = record.timestamp

    def get_answer(self):
        return f"{self.value} at {self.timestamp.date()}"


class BarChartCalculator:
    def __init__(
        self, key=lambda record: (record.max_temperature, record.min_temperature)
    ):
        self._day = []
        self._max_temperature = []
        self._min_temperature = []
        self._key = key

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, timestamp):
        self._day.append(timestamp.day)

    @property
    def max_temperature(self):
        return self._max_temperature

    @max_temperature.setter
    def max_temperature(self, max_temp):
        self._max_temperature.append(max_temp)

    @property
    def min_temperature(self):
        return self._min_temperature

    @min_temperature.setter
    def min_temperature(self, min_temp):
        self._min_temperature.append(min_temp)

    def update(self, record):
        self.day.append(record.timestamp.day)
        max_value, min_value = self._key(record)
        self.max_temperature.append(max_value)
        self.min_temperature.append(min_value)

    def get_answer(self):
        return {
            "Day": self._day,
            "MaxTemp": self._max_temperature,
            "MinTemp": self._min_temperature,
        }


class AvgMaxTempCalculator(AvgCalculator):
    def __init__(self):
        super().__init__(key=lambda record: record.max_temperature)


class AvgMinTempCalculator(AvgCalculator):
    def __init__(self):
        super().__init__(key=lambda record: record.min_temperature)


class AvgMeanHumidityCalculator(AvgCalculator):
    def __init__(self):
        super().__init__(key=lambda record: record.mean_humidity)


class MaxTempCalculator(Calculator):
    def __init__(self):
        super().__init__(
            keys=[
                lambda record: record.max_temperature,
                lambda old_value, new_value: old_value < int(new_value),
            ]
        )


class MinTempCalculator(Calculator):
    def __init__(self):
        super().__init__(
            keys=[
                lambda record: record.min_temperature,
                lambda old_value, new_value: old_value > int(new_value),
            ]
        )


class MaxHumidityCalculator(Calculator):
    def __init__(self):
        super().__init__(
            keys=[
                lambda record: record.max_humidity,
                lambda old_value, new_value: old_value < int(new_value),
            ]
        )

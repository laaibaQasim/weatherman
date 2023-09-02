from datetime import datetime


class WeatherRecord:
    __slots__ = (
        "_timestamp",
        "_max_temperature",
        "_min_temperature",
        "_max_humidity",
        "_mean_humidity",
    )

    def __init__(self, timestamp, max_temp, min_temp, max_humidity, mean_humidity):
        self.timestamp = timestamp
        self.max_temperature = max_temp
        self.min_temperature = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if timestamp != "":
            self._timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        else:
            self._timestamp = None

    @property
    def max_temperature(self):
        return self._max_temperature

    @max_temperature.setter
    def max_temperature(self, max_temp):
        if max_temp != "":
            self._max_temperature = int(max_temp)
        else:
            self._max_temperature = None

    @property
    def min_temperature(self):
        return self._min_temperature

    @min_temperature.setter
    def min_temperature(self, min_temp):
        if min_temp != "":
            self._min_temperature = int(min_temp)
        else:
            self._min_temperature = None

    @property
    def max_humidity(self):
        return self._max_humidity

    @max_humidity.setter
    def max_humidity(self, humidity):
        if humidity != "":
            self._max_humidity = int(humidity)
        else:
            self._max_humidity = None

    @property
    def mean_humidity(self):
        return self._mean_humidity

    @mean_humidity.setter
    def mean_humidity(self, humidity):
        if humidity != "":
            self._mean_humidity = int(humidity)
        else:
            self._mean_humidity = None

    @classmethod
    def from_dict(cls, row):
        key = "PKT" if "PKT" in row else "PKST"
        return cls(
            row[key],
            row["Max TemperatureC"],
            row["Min TemperatureC"],
            row["Max Humidity"],
            row[" Mean Humidity"],
        )

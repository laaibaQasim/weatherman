from enum import Enum


class Color(Enum):
    BLUE = 34
    RED = 31


def colored_print(color_code, statement, end=""):
    print(f"\033[{color_code}m{statement}\033[0m", end=end)


def draw_bar_chart(stats, number):
    print(f"---------{number} bar chart---------")
    key = "Day"

    for i in range(len(stats[key])):
        print(stats[key][i], end=" ")

        if not stats["MaxTemp"][i]:
            print("no data found")
            continue

        for j in range(stats["MaxTemp"][i]):
            colored_print(Color.RED.value, "+")

        if number == "two":
            print(f" {stats['MaxTemp'][i]}C")
            print(stats[key][i], end=" ")

        for j in range(stats["MinTemp"][i]):
            colored_print(Color.BLUE.value, "+")

        if number == "one":
            print(f" {stats['MaxTemp'][i]}C - ", end="")

        print(f" {stats['MinTemp'][i]}C")

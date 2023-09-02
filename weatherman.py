import argparse
from weatherman_commands import (
    YearlyReportCommand,
    MonthlyReportCommand,
    DailyReportCommand,
)


def read_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--data_path", help="your data path")
    arg_parser.add_argument("-c", "--c_date", help="date in format year/month")
    arg_parser.add_argument("-e", "--year", help="year")
    arg_parser.add_argument("-a", "--a_date", help="date in format year/month")

    args = arg_parser.parse_args()
    data_path = args.data_path

    if args.c_date:
        try:
            year, month = args.c_date.split("/")
            command = DailyReportCommand(year, month)
            command.execute(data_path)
        except ValueError or AttributeError:
            print("no month given")
            return

    if args.year:
        command = YearlyReportCommand(args.year)
        command.execute(data_path)

    if args.a_date:
        try:
            year, month = args.a_date.split("/")
            command = MonthlyReportCommand(year, month)
            command.execute(data_path)
        except ValueError or AttributeError:
            print("no month given")
            return


if __name__ == "__main__":
    read_arguments()

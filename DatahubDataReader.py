import csv
from Reader import Reader


class DatahubDataReader(Reader):
    def __init__(self):
        self.DATA_FILE_NAME = "datahub-countries-aggregated-data.csv"
        self.DATES_DATA_FILE_NAME = "dates-data(datahub-data).csv"

        with open(self.DATA_FILE_NAME, "r") as csv_read_file:
            self.country_data = list(csv.DictReader(csv_read_file))

    def get_start_end_dates(self):
        """Gets the country start dates."""

        self.countries_dates_data = []
        first_country = self.country_data[0]["Country"]

        for country_num, country_data in enumerate(self.country_data):
            date = country_data["Date"]
            country = country_data["Country"]

            data = {
                "Country": country,
                "Start-Date": date,
            }

            if country == first_country and country_num != 0:
                break

            else:
                self.countries_dates_data.append(data)

        for country_num, country_data in enumerate(self.country_data[-len(self.countries_dates_data):]):
            date = country_data["Date"]
            self.countries_dates_data[country_num]["End-Date"] = date


if __name__ == "__main__":
    Reader = DatahubDataReader()
    Reader.make_csv_file()

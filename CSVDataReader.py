import csv
import json


class CSVDataReader:
    def __init__(self):
        self.FILE_PATH = "datahub-countries-aggregated-data.csv"
        self.DATES_DATA_FILE_NAME = "dates-data.csv"

        with open(self.FILE_PATH, "r") as csv_read_file:
            self.country_data = list(csv.DictReader(csv_read_file))

    def get_start_dates(self):
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


    def get_end_dates(self):
        """Returns a dictionary of the start and the end date of the different countries."""
        for country_num, country_data in enumerate(self.country_data[-len(self.countries_dates_data):]):
            self.countries_dates_data[country_num]["End-Date"] = country_data["Date"]

    def make_csv_file(self):
        """Writes the dates data into the csv file."""
        self.get_start_dates()
        self.get_end_dates()

        with open(self.DATES_DATA_FILE_NAME, "w") as csv_write_file:
            csv_write_file.write('"Country","Start Date","End Date"\n')
            for country_data in self.countries_dates_data:
                country = country_data["Country"]
                start_date = country_data["Start-Date"]
                end_date = country_data["End-Date"]

                line = f'"{country}","{start_date}","{end_date}"\n'
                csv_write_file.write(line)


if __name__ == "__main__":
    Reader = CSVDataReader()
    Reader.make_csv_file()
import csv
import pycountry
from datetime import datetime


class DataCompiler:
    def __init__(self):
        self.OWID_DATA_FILE_NAME = "dates-data(OWID-data).csv"
        self.DATAHUB_DATA_FILE_NAME = "dates-data(datahub-data).csv"
        self.COMMON_DATES_FILE_NAME = "dates-data(common).csv"

    def get_country_sets(self, file):
        """Returns a set of the countries."""
        countries_list = []
        with open(file, "r") as data_file:
            data = data_file.read().strip()
            data = data.split("\n")
            del data[0]

        for country_data in data:
            country_data = country_data[1:-1]
            country = country_data.split('","')[0]
            countries_list.append(country)

        countries_set = set(countries_list)
        return countries_set

    def remove_uncommon_countries(self, file, common_countries):
        """Removes the uncommon countries data."""
        with open(file, "r") as data_file:
            data = list(csv.DictReader(data_file))

        for country_num, country_data in enumerate(data):
            if country_data["Country"] not in common_countries:
                del data[country_num]

        return data

    def get_common_countries_data(self):
        """Gets the common countries data from the 2 data sources."""
        owid_countries = self.get_country_sets(self.OWID_DATA_FILE_NAME)
        datahub_countries = self.get_country_sets(self.DATAHUB_DATA_FILE_NAME)
        common_countries = sorted(owid_countries.intersection(datahub_countries))

        # print(f"Number of countries in datahub: {len(datahub_countries)}")
        # print(f"Number of countries in owid: {len(owid_countries)}\n\n")

        datahub_data = self.remove_uncommon_countries(self.DATAHUB_DATA_FILE_NAME, common_countries)
        owid_data = self.remove_uncommon_countries(self.OWID_DATA_FILE_NAME, common_countries)

        # print(f"Number of common countries: {len(common_countries)}")
        # print(f"Number of countries data in datahub: {len(datahub_data)}")
        # print(f"Number of countries data in owid: {len(owid_data)}")

        return {
            "datahub-data": datahub_data,
            "owid-data": owid_data,
        }

    def find_oldest_newest_date(self, comparing_dates):
        """Identifies and returns the oldest and newest date."""

        for index, date in enumerate(comparing_dates):
            year = int(date.split("-")[0])
            month = int(date.split("-")[1])
            day = int(date.split("-")[2])

            date = datetime(year, month, day)
            comparing_dates[index] = date

        newer_date = str(max(comparing_dates).date())
        older_date = str(min(comparing_dates).date())

        return {
            "newer": newer_date,
            "older": older_date,
        }

    def get_common_dates(self):
        """Calls the get_common_countries_data() and changes the start and end dates do that they are common."""

        dates_data = self.get_common_countries_data()
        datahub_data = dates_data["datahub-data"]
        owid_data = dates_data["owid-data"]

        common_dates_data = []

        for data_num in range(len(owid_data)):
            owid_start_date = owid_data[data_num]["Start Date"]
            datahub_start_date = datahub_data[data_num]["Start Date"]

            owid_end_date = owid_data[data_num]["End Date"]
            datahub_end_date = datahub_data[data_num]["End Date"]

            start_date = self.check_older_newer_date([owid_start_date, datahub_start_date])["newer"]
            end_date = self.check_older_newer_date([owid_end_date, datahub_end_date])["older"]

            # print(f"Start Date: {start_date.date()} from {owid_start_date} and {datahub_start_date}")
            # print(f"End Date: {end_date.date()} from {owid_end_date} and {datahub_end_date}")

            date_data = {
                "Country": owid_data[data_num]["Country"],
                "Start Date": start_date,
                "End Date": end_date,
            }

            common_dates_data.append(date_data)

        return common_dates_data

    def make_csv(self):
        """Makes csv file of the common dates."""
        dates_data = self.get_common_dates()

        with open(self.COMMON_DATES_FILE_NAME, "w") as csv_write_file:
            csv_write_file.write('"Country","Start Date","End Date"\n')
            for country_date in dates_data:
                country = country_date["Country"]
                start_date = country_date["Start Date"]
                end_date = country_date["End Date"]
                line = f'"{country}","{start_date}","{end_date}"\n'
                csv_write_file.write(line)


if __name__ == "__main__":
    Compiler = DataCompiler()
    sources_data = Compiler.make_csv()

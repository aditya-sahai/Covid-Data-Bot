import csv
import pycountry
from datetime import datetime


class DataCompiler:
    def __init__(self):
        self.OWID_DATA_FILE_NAME = "dates-data(OWID-data).csv"
        self.DATAHUB_DATA_FILE_NAME = "dates-data(datahub-data).csv"

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

    def check_older_newer_date(self, owid_date, datahub_date):
        """Identifies and returns the older and newer date."""

        owid_start_year = int(owid_date.split("-")[0])
        owid_start_month = int(owid_date.split("-")[1])
        owid_start_day = int(owid_date.split("-")[2])

        datahub_start_year = int(datahub_date.split("-")[0])
        datahub_start_month = int(datahub_date.split("-")[1])
        datahub_start_day = int(datahub_date.split("-")[2])

        owid_start_date = datetime(owid_start_year, owid_start_month, owid_start_day)
        datahub_start_date = datetime(datahub_start_year, datahub_start_month, datahub_start_day)

        newer_date = str(max([owid_start_date, datahub_start_date]).date())
        older_date = str(min([owid_start_date, datahub_start_date]).date())

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

            start_date = self.check_older_newer_date(owid_start_date, datahub_start_date)["newer"]
            end_date = self.check_older_newer_date(owid_end_date, datahub_end_date)["older"]

            # print(f"Start Date: {start_date.date()} from {owid_start_date} and {datahub_start_date}")
            # print(f"End Date: {end_date.date()} from {owid_end_date} and {datahub_end_date}")

            date_data = {
                "Country": owid_data[data_num]["Country"],
                "Start Date": start_date,
                "End Date": end_date,
            }

            common_dates_data.append(date_data)


if __name__ == "__main__":
    Compiler = DataCompiler()
    sources_data = Compiler.get_common_dates()

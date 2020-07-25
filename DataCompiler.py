import csv
import pycountry


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

        print(f"Number of common countries: {len(common_countries)}")
        print(f"Number of countries data in datahub: {len(datahub_data)}")
        print(f"Number of countries data in owid: {len(owid_data)}")

        return {
            "datahub-data": datahub_data,
            "owid-data": owid_data,
        }


if __name__ == "__main__":
    Compiler = DataCompiler()
    sources_data = Compiler.get_common_countries_data()

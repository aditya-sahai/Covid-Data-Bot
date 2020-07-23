class DataCompiler:
    def __init__(self):
        self.OWID_DATA_FILE_NAME = "dates-data(OWID-data).csv"
        self.DATAHUB_DATA_FILE_NAME = "dates-data(datahub-data).csv"

    def get_country_sets(self, file):
        """Returns a set of the countries."""

        countries_list = []
        with open(self.DATAHUB_DATA_FILE_NAME, "r") as data_file:
            data = data_file.read().strip()
            data = data.split("\n")
            del data[0]

        for country_data in data:
            country_data = country_data[1:-1]
            country = country_data.split('","')[0]
            countries_list.append(country)

        countries_set = set(countries_list)
        return countries_set

    def get_common_countries(self):
        """Gets the common countris from the 2 data sources."""
        owid_countries = self.get_country_sets(self.OWID_DATA_FILE_NAME)
        datahub_countries = self.get_country_sets(self.DATAHUB_DATA_FILE_NAME)
        common_countries = sorted(owid_countries.intersection(datahub_countries))

        print(common_countries)
        print(len(common_countries))


if __name__ == "__main__":
    Compiler = DataCompiler()
    Compiler.get_common_countries()

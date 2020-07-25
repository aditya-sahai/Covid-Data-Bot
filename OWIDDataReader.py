import json
from Reader import Reader


class OWIDDataReader(Reader):
    def __init__(self):
        self.DATA_FILE_NAME = "covid-data.json"
        self.DATES_DATA_FILE_NAME = "dates-data(OWID-data).csv"

        with open(self.DATA_FILE_NAME, "r") as data_file:
            self.data = json.load(data_file)

    def get_start_end_dates(self):
        """Makes a dictionary of country start and end date."""
        self.countries_dates_data = []

        for country_data in self.data:
            country = self.data[country_data]["location"]
            start_date = self.data[country_data]["data"][0]["date"]
            end_date = self.data[country_data]["data"][-1]["date"]

            dates_dict = {
                "Country": country,
                "Start-Date": start_date,
                "End-Date": end_date,
            }
            self.countries_dates_data.append(dates_dict)


if __name__ == "__main__":
    Reader = OWIDDataReader()
    Reader.make_csv_file()

import json


class OWIDDataReader:
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

    def make_csv_file(self):
        """Writes the dates data into the csv file."""
        self.get_start_end_dates()

        with open(self.DATES_DATA_FILE_NAME, "w") as csv_write_file:
            csv_write_file.write('"Country","Start Date","End Date"\n')
            for country_data in self.countries_dates_data:
                country = country_data["Country"]
                start_date = country_data["Start-Date"]
                end_date = country_data["End-Date"]

                line = f'"{country}","{start_date}","{end_date}"\n'
                csv_write_file.write(line)


if __name__ == "__main__":
    Reader = OWIDDataReader()
    Reader.make_csv_file()

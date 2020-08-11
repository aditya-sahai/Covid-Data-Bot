import csv
import pycountry
from datetime import datetime
import json


class DataCompiler:
    def __init__(self):
        self.OWID_DATES_FILE_NAME = "dates-data(OWID-data).csv"
        self.DATAHUB_DATES_FILE_NAME = "dates-data(datahub-data).csv"
        self.COMMON_DATES_FILE_NAME = "dates-data(common).csv"
        self.DATAHUB_DATA_FILE_NAME = "datahub-countries-aggregated-data.csv"
        self.OWID_DATA_FILE_NAME = "covid-data.json"
        self.COMPILED_DATA_FILE_NAME = "compiled-covid-data.json"
        self.get_common_dates()
        self.remove_new_countries()
        self.get_all_countries_start_end_date()
        self.get_compiled_dict()

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

    def remove_new_countries(self):
        """Removes country from the dates data which are newer than 2020-04"""
        common_new_dates = []
        
        for country in self.common_dates_data:
            if not ("2020-04" in country["Start Date"] or "2020-05" in country["Start Date"]):
                common_new_dates.append(country)

        self.common_dates_data = common_new_dates[:]
        
    def get_common_country_dates(self, data, file_name):
        """Returns a list with the dates data of the commmon countries"""
        output_data = []

        with open(file_name, "r") as data_file:
            file_data = list(csv.DictReader(data_file))

        for country in data:
            for dates_data in file_data:
                if dates_data["Country"] == country:
                    output_data.append(dates_data)
        
        return output_data

    def get_common_countries_dates_data(self):
        """Gets the common countries data from the 2 data sources."""
        owid_countries = self.get_country_sets(self.OWID_DATES_FILE_NAME)
        datahub_countries = self.get_country_sets(self.DATAHUB_DATES_FILE_NAME)
        common_countries = sorted(owid_countries.intersection(datahub_countries))

        self.datahub_dates_data = self.get_common_country_dates(common_countries, self.DATAHUB_DATES_FILE_NAME)
        self.owid_dates_data = self.get_common_country_dates(common_countries, self.OWID_DATES_FILE_NAME)

        print(f"\nNumber of common countries: {len(common_countries)}")
        print(f"Number of countries data in datahub: {len(self.datahub_dates_data)}")
        print(f"Number of countries data in owid: {len(self.owid_dates_data)}")

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

        self.get_common_countries_dates_data()
        self.common_dates_data = []

        for data_num in range(len(self.datahub_dates_data)):
            owid_start_date = self.owid_dates_data[data_num]["Start Date"]
            datahub_start_date = self.datahub_dates_data[data_num]["Start Date"]
            owid_end_date = self.owid_dates_data[data_num]["End Date"]
            datahub_end_date = self.datahub_dates_data[data_num]["End Date"]

            start_date = self.find_oldest_newest_date([owid_start_date, datahub_start_date])["newer"]
            end_date = self.find_oldest_newest_date([owid_end_date, datahub_end_date])["older"]

            # print(f"Start Date: {start_date.date()} from {owid_start_date} and {datahub_start_date}")
            # print(f"End Date: {end_date.date()} from {owid_end_date} and {datahub_end_date}")

            country = self.owid_dates_data[data_num]["Country"]

            date_data = {
                "Country": country,
                "Start Date": start_date,
                "End Date": end_date,
            }

            self.common_dates_data.append(date_data)

    def get_all_countries_start_end_date(self):
        """Returns a start and end date which is true for all countries."""
        with open(self.COMMON_DATES_FILE_NAME, "r") as csv_dates_file:
            dates_data = list(csv.DictReader(csv_dates_file))

        start_dates, end_dates = [], []
        for country_date in self.common_dates_data:
            start_dates.append(country_date["Start Date"])
            end_dates.append(country_date["End Date"])

        self.start_date = self.find_oldest_newest_date(start_dates)["newer"]
        self.end_date = self.find_oldest_newest_date(end_dates)["older"]
        print(f"\nStart Date: {self.start_date}\nEnd Date: {self.end_date}")

    def get_valid_country_codes(self):
        """Reads the dates-data(common).csv file and returns a list of the unique countries."""
        self.valid_countries = []

        with open(self.COMMON_DATES_FILE_NAME, "r") as common_dates_file:
            dates_data = list(csv.DictReader(common_dates_file))
        
        for country in dates_data:
            self.valid_countries.append(country["Country"])
        
        print(len(self.valid_countries))


    def get_owid_data(self):
        """Returns a dictionary containing the cases, deaths data along with the date."""
        self.owid_data_dict = {}

        with open(self.OWID_DATA_FILE_NAME, "r") as owid_data_file:
            owid_data = json.load(owid_data_file)

        for country_iso in owid_data:
            for data in owid_data[country_iso]["data"]:
                date = data["date"]

                if "2020-01" in date or "2020-02" in date or "2020-03-0" in date or "2020-03-1" in date or "2020-03-2" in date:
                    continue

                if country_iso not in self.valid_countries:
                    continue
                
                else:
                    if country_iso in list(self.owid_data_dict.keys()):
                        self.owid_data_dict[country_iso]["data"].append(
                        {
                            "date": date,
                            "total-cases": data["total_cases"],
                            "new-cases": data["new_cases"],
                            "total-deaths": data["total_deaths"],
                            "new-deaths": data["new_deaths"],
                        }
                    )
                    
                    else:
                        self.owid_data_dict[country_iso] = {
                            "data": [
                                {
                                    "date": date,
                                    "total-cases": data["total_cases"],
                                    "new-cases": data["new_cases"],
                                    "total-deaths": data["total_deaths"],
                                    "new-deaths": data["new_deaths"],
                                }
                            ],
                        }

    def get_datahub_data_dict(self):
        """Returns a dictionary containing the recovered data along with the date."""
        self.datahub_data_dict = {}
        exceptions = {
            "US": "USA",
            "Bolivia": "BOL",
            "Brunei": "BRN",
            "Iran": "IRN",
            "Russia": "RUS",
            "Vietnam": "VNM",
            "Venezuela": "VEN",
            "South Korea": "KOR",
            "Korea, South": "KOR",
        }     

        with open(self.DATAHUB_DATA_FILE_NAME, "r") as datahub_data_file:
            datahub_data = datahub_data_file.read().strip().split("\n")[1:]

        for country in datahub_data:
            country = country.split(",")
            date = country[0]
            country_name = country[1]
            recovered = country[3]

            if "2020-01" in date or "2020-02" in date or "2020-03-0" in date or "2020-03-1" in date or "2020-03-2" in date:
                continue

            try:
                country_iso = pycountry.countries.get(name=country_name).alpha_3

            except AttributeError:
                if country[1] in list(exceptions.keys()):
                    country_iso = exceptions[country[1]]
                    
                    self.datahub_data_dict[country_iso] = {
                        "data": [],
                    }
                    self.datahub_data_dict[country_iso]["data"].append(
                        {
                            "date": date,
                            "recovered": recovered,
                        }
                    )

                else:
                    continue
            
            else:                
                if country_iso in list(self.datahub_data_dict.keys()):
                    self.datahub_data_dict[country_iso]["data"].append(
                        {
                            "date": date,
                            "recovered": recovered,
                        }
                    )
                
                else:
                    self.datahub_data_dict[country_iso] = {
                        "data": [],
                    }
                    self.datahub_data_dict[country_iso]["data"].append(
                        {
                            "date": date,
                            "recovered": recovered,
                        }
                    )

    def get_compiled_dict(self):
        self.get_valid_country_codes()
        self.get_owid_data()
        # self.get_datahub_data_dict()

        self.data_dict = {}

        # for country in self.all_countries_data_dict:
        #     have_recovered_data = self.all_countries_data_dict[country]["data"][0].get("recovered")

        #     if not have_recovered_data:            
        #         self.data_dict[country] = self.all_countries_data_dict[country]

        print(f"\nNumber of countries in owid source with data: {len(self.owid_data_dict)}")
        # print(f"Number of countries in datahub source with data: {len(self.datahub_data_dict)}")

    def make_data_json(self):
        """Writes the data to the json file."""
        with open(self.COMPILED_DATA_FILE_NAME, "w") as json_compiled_file:
            json.dump(self.data_dict, json_compiled_file, indent=4)

    def make_csv(self):
        """Makes csv file of the common dates."""
        with open(self.COMMON_DATES_FILE_NAME, "w") as csv_write_file:
            csv_write_file.write('"Country","Start Date","End Date"\n')
            
            for country_date in self.common_dates_data:
                country = country_date["Country"]
                start_date = country_date["Start Date"]
                end_date = country_date["End Date"]
                line = f'"{country}","{start_date}","{end_date}"\n'
                csv_write_file.write(line)


if __name__ == "__main__":
    Compiler = DataCompiler()
    Compiler.make_data_json()

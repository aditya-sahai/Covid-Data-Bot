import json
import pycountry
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.DATA_FILE_NAME = "compiled-covid-data.json"
        
        self.DATA_KEYS = {
            "1": "total-cases",
            "2": "new-cases",
            "3": "total-deaths",
            "4": "new-deaths",
            "5": "recovered",
            "6": "all",
        }

        self.fig, self.ax = plt.subplots()

    def get_user_data(self):
        """Gets the iso codes and data the user wants from the user."""
        exceptions = {
            "us": "USA",
            "united states of america": "USA",
            "usa": "USA",
            "bolivia": "BOL",
            "brunei": "BRN",
            "iran": "IRN",
            "russia": "RUS",
            "vietnam": "VNM",
            "venezuela": "VEN",
            "south korea": "KOR",
        }

        print("1)  Total Cases\n2)  New Cases\n3)  Total Deaths\n4)  New Deaths\n5)  Recovered\n6)  Country Detailed (which would show the deaths cases and recovered of a single country in one graph)")
        countries_iso_list = []
        required_data = "string"
        print()

        while not required_data.isdigit():
            required_data = input("Enter the number of the data you are looking for: ").strip()
            
            if required_data.lower() == "q":
                exit()
                
        if int(required_data) > 6 or int(required_data) < 1:
            print("Enter a number between 1 and 6.")
            return self.get_user_data()

        if required_data != "6":
            countries_num = "string"
            print()
            while not countries_num.isdigit():
                countries_num = input("Enter the number of countries you wish to see the data for: ").strip()
                
                if countries_num.lower() == "q":
                    exit()

            countries_num = int(countries_num)

            print()
            for n in range(countries_num):
                country = input("Enter the country: ").lower().strip()
                if country.lower() == "q":
                    exit()
                
                try:
                    country_iso = pycountry.countries.get(name=country).alpha_3
                
                except AttributeError:
                    if country in list(exceptions.keys()):
                        country_iso = exceptions[country]
                        countries_iso_list.append(country_iso)
                    
                    else:
                        print(f"Could not find country for {country}")
                
                else:
                    countries_iso_list.append(country_iso)

        elif required_data == "6":
            while countries_iso_list == []:
                country = input("\nEnter the country: ").lower().strip()
                if country.lower() == "q":
                    exit()
                
                try:
                    country_iso = pycountry.countries.get(name=country).alpha_3
                
                except AttributeError:
                    if country in list(exceptions.keys()):
                        country_iso = exceptions[country]
                        countries_iso_list.append(country_iso)
                    
                    else:
                        print(f"Could not find country for {country}")
                
                else:
                    countries_iso_list = [country_iso]
        
        number_of_days = "string"
        print()

        while not number_of_days.isdigit():
            number_of_days = input("Enter the number of days for which you want to see the data for: ").strip()
            
            if number_of_days.lower() == "q":
                exit()
        
        number_of_days = int(number_of_days)

        self.user_requirement_dict = {
            "countries": countries_iso_list,
            "number-of-days": number_of_days,
            "required-data": self.DATA_KEYS[required_data],
        }
    
    def get_data(self):
        """Gets the data user wants."""
        with open(self.DATA_FILE_NAME, "r") as data_file:
            self.covid_data = json.load(data_file)
        
        self.output_data = {}

        for country in self.user_requirement_dict["countries"]:
            self.output_data[country] = {
                "data": self.covid_data[country]["data"][-self.user_requirement_dict["number-of-days"]:]
            }
        
    def plot_country_data(self):
        """Plots the data of the country the user wants BUT DOES NOT SHOW THE GRAPH."""

        # list of dates for x-axis
        # data for y axis

        dates_list = []
        recovered_data_dict = {}
        user_data_dict = {}

        for country in self.user_requirement_dict["countries"]:
            recovered_data_dict[country] = {
                "data": []
            }
            for data in self.output_data[country]["data"]:
                dates_list.append(data["date"])
                recovered_data_dict[country]["data"].append(data["recovered"])
        
        if self.user_requirement_dict["required-data"] != "all":
            for country in self.user_requirement_dict["countries"]:
                user_data_dict[country] = {
                    "data": []
                }
                for data in self.output_data[country]["data"]:
                    user_data_dict[country]["data"].append(data[self.user_requirement_dict["required-data"]])
            
            
        elif self.user_requirement_dict["required-data"] == "all":
            country = self.user_requirement_dict["countries"][0]
            user_data_dict[country] = {}
            
            for required_data in list(self.DATA_KEYS.values())[:-2]:
                user_data_dict[country][required_data] = []
                for data in self.output_data[country]["data"]:
                    user_data_dict[country][required_data].append(data[required_data])

        # print(json.dumps(user_data_dict, indent=4))
    
    def plot_country_detailed_data(self):
        """Plots the detailed data of the country that is the deaths recovered etc. of a single country."""

    def format_and_show_graph(self):
        """Formats and shows the graph."""


if __name__ == "__main__":
    GraphPlotter = Plotter()
    GraphPlotter.get_user_data()
    GraphPlotter.get_data()
    # print(json.dumps(GraphPlotter.output_data, indent=4))
    GraphPlotter.plot_country_data()
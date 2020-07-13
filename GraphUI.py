import matplotlib.pyplot as plt
import numpy as np
import json
import pycountry as pyc


class GraphUI:

    def __init__(self):
        """Initialize the DataReceiver class."""

        self.DATAFILENAME = "covid-data.json"

        with open(self.DATAFILENAME, "r") as data_file:
            self.covid_data = json.load(data_file)

        self.fig, self.ax = plt.subplots()

    def get_country_iso_codes(self):
        """Returns a list of the iso codes of the countries entered by the user."""

        number_of_countries = input("\nEnter the number of countries: ").strip()

        if number_of_countries.isdigit():
            number_of_countries = int(number_of_countries)

            iso_codes = []
            print()

            for x in range(number_of_countries):
                country = input("Enter the name of the country: ").strip().lower()
                iso_code = pyc.countries.get(name=country)

                if iso_code:
                    iso_codes.append(iso_code.alpha_3)

                else:
                    print(f"Could not find country with the name '{country}'.")

            return iso_codes

        else:
            print("Please enter a number.")

    def show_multiple_countries_total_deaths(self):
        """Asks the user for the countries names and plots a graph."""
        iso_codes = self.get_country_iso_codes()
        number_of_days = int(input("\nEnter the number of days: "))

        for iso_code in iso_codes:
            self.plot_single_country_deaths(iso_code, (0, 0, 0), number_of_days=number_of_days)

        self.format_and_show_graph()

    def plot_single_country_deaths(self, country_abbr, color, number_of_days=21):
        """Plots the deaths data of a single country BUT DOES NOT CALL SHOW FUNCTION."""

        country_deaths_list, dates_list = [], []

        for country_data in self.covid_data[country_abbr.strip().upper()]["data"][-number_of_days:]:
            country_deaths_list.append(int(country_data["total_deaths"]))
            dates_list.append(country_data["date"])

        self.ax.plot(dates_list, country_deaths_list)

    def format_and_show_graph(self):
        """Rotates, sets the x and y labels and shows the graph."""

        plt.xlabel(f"Date")
        plt.ylabel("Number Of Deaths")

        plt.xticks(rotation=30, size=10)
        plt.show()


if __name__ == "__main__":
    GraphObj = GraphUI()
    GraphObj.show_multiple_countries_total_deaths()

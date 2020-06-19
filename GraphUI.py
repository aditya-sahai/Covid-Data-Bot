from datetime import date
from calendar import month_name
import matplotlib.pyplot as plt
import numpy as np
import json


class GraphUI:

    def __init__(self):
        """Initialize the DataReceiver class."""

        self.day_today = date.today().day
        self.current_month = month_name[date.today().month]
        self.current_year = date.today().year
        self.DATAFILENAME = "covid-data.json"

        with open(self.DATAFILENAME, "r") as data_file:
            self.covid_data = json.load(data_file)

    def show_total_deaths_single_country(self, country_abbr):
        """Displays the total deaths of a single country."""

        plt.xlabel(f"Date({self.current_year}-{self.current_month})")
        plt.ylabel("Number Of Deaths")

        deaths_list = []
        dates_list = []

        for data in self.covid_data[country_abbr.upper().strip()][-7:]:
            deaths_list.append(int(data["total_deaths"]))
            dates_list.append(int(data["date"].split("-")[-1]))


        deaths_array = np.array(deaths_list)
        date_array = np.array(dates_list)

        y_min = (deaths_array.min() // 100) * 100
        y_max = (deaths_array.max() // 100 + 1) * 100

        plt.axis([self.day_today - 7, self.day_today - 0.5, y_min, y_max])

        plt.plot(date_array, deaths_array, color="red")
        plt.show()


if __name__ == "__main__":
    GraphObj = GraphUI()
    GraphObj.show_total_deaths_single_country("IND")

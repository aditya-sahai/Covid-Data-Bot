import pycountry


class Reader:
    def make_csv_file(self):
        """Writes the dates data into the csv file."""
        self.get_start_end_dates()

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

        with open(self.DATES_DATA_FILE_NAME, "w") as csv_write_file:
            csv_write_file.write('"Country","Start Date","End Date"\n')
            for country_data in self.countries_dates_data:

                try:
                    country = pycountry.countries.get(name=country_data["Country"]).alpha_3

                except AttributeError:
                    if country_data["Country"] in list(exceptions.keys()):
                        country = exceptions[country_data["Country"]]
                        start_date = country_data["Start-Date"]
                        end_date = country_data["End-Date"]

                        line = f'"{country}","{start_date}","{end_date}"\n'
                        csv_write_file.write(line)

                    else:
                        print(f"Could not find iso code for: {country_data['Country']}")

                else:
                    start_date = country_data["Start-Date"]
                    end_date = country_data["End-Date"]

                    line = f'"{country}","{start_date}","{end_date}"\n'
                    csv_write_file.write(line)

import csv


class power_model:

    def __init__(self, reader_name, output_name):
        """
        Constructor for power_model class

        Args:
            reader_name (string): file name for reader csv
            output_name (string): file name for output csv
        """
        self.reader_name = reader_name  # Input csv file name
        self.output_name = output_name  # Output csv file name
        self.reader = None  # Placeholder for the csv reader object
        self.writer = None  # Placeholder for the csv reader object
        self.cur_line = [0]  # Placeholder for the current line of the csv
        self.prev_nuc = 0  # Previous nuclear power
        self.season = None  # Current season for pricing
        self.current_price = None  # Current price based on season and time
        self.needed_power = None  # The power required
        self.prev_diff = None

        # O_name indicates a variable used for OUTPUT

        self.O_power = {  # Empty dictionary for output power
            "state": "0",
            "time": 0,
            "total": 0,
            "solar": 0,
            "nuclear": 0,
            "wind": 0,
            "hydro": 0,
            "gas": 0,
            "biofuel": 0,
            "neighbour": 0,
            "power_diff": 0,
            "green_power": 0,
            "bought": 0,
            "sold": 0,
            "CO2_gen": 0,
            "sell_price": 0,
            "cost_to_make": 0,
            "margin": 0,
            }

        self.cur_pwr = {  # Empty dicitonary fro the current power information
            "time": 0,
            "demand": 0,
            "solar": 0,
            "nuclear": 0,
            "wind": 0,
            "hydro": 0,
            "gas": 0,
            "biofuel": 0,
            "neighbour": 0,
            "temps": [],
            "solar_coef": 0,
            "wind_coef": 0,
            "hydro_coef": 0,
            "neighbour_demand": 0,
            "neighbour_sell_price": 0,
            "previous_power_values": []
            }

        self.run()

    def run(self):
        """
        Function used to run the main loop of the program
        """

        # Open the csv files
        reader_csv = open(self.reader_name, newline="")
        output_csv = open(self.output_name, "w", newline="")

        fieldnames = [  # Declare fieldnames
            "state",
            "time",
            "total",
            "solar",
            "nuclear",
            "wind",
            "hydro",
            "gas",
            "biofuel",
            "neighbour",
            "power_diff",
            "green_power",
            "bought",
            "sold",
            "CO2_gen",
            "sell_price",
            "cost_to_make",
            "margin"]

        # Create the reader and writer objects and write the headers
        self.reader = csv.reader(reader_csv)
        self.writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        self.writer.writeheader()

        try:
            while True:
                self.U_line()  # Update the current line in csv
                self.U_state() # Update the current state of the power model
                self.O_to_spreadsheet()  # Write the output to the spreadsheet
        except StopIteration:  # Wait for iteration complete
            # Close the reader and output csv
            reader_csv.close()
            output_csv.close()

    def U_line(self):
        """

        A function used to move to the next line in the csv. A generator is used to increase program efficiency to ensure the entire csv
        is not being read into memory. This allows for years of data to be computed without overloading the memory and allows for scalability of the design.

        Note that this function starts with a U meaning that this function is an UPDATE function.
        """
        self.cur_line = next(self.reader)  # Call the generator to move to the next line in the csv

        # If we reach a line with no INPUT format raise a StopIteration error.
        if self.cur_line[0] == "":
            raise StopIteration

        # Reset the output values
        self.O_power["state"] = 0
        self.O_power["time"] = 0
        self.O_power["total"] = 0
        self.O_power["solar"] = 0
        self.O_power["nuclear"] = 0
        self.O_power["wind"] = 0
        self.O_power["hydro"] = 0
        self.O_power["gas"] = 0
        self.O_power["biofuel"] = 0
        self.O_power["neighbour"] = 0
        self.O_power["power_diff"] = 0
        self.O_power["green_power"] = 0
        self.O_power["bought"] = 0
        self.O_power["sold"] = 0
        self.O_power["CO2_gen"] = 0
        self.O_power["sell_price"] = 0
        self.O_power["cost_to_make"] = 0
        self.O_power["margin"] = 0

    def U_state(self):
        """
        UPDATE state function used to compute if the line is an initial condition or an input condition.
        This function will call other methods to process the various data assuming it is an input stage.
        """

        if self.cur_line[0] == '0':
            self.U_starting_conditions()  # Parse based on an initial condition

        elif self.cur_line[0] == '1':
            self.C_nuclear_power()  # Calculate the new value for nuclear power
            self.U_input_conditions()  # Parse based on an input condition

            # Calculate volume of each supply to use
            self.C_gas()
            self.C_hydro()
            self.C_wind()
            self.C_solar()
            self.C_nuclear()
            self.C_biofuel()
            self.C_neighbour()

            self.C_season()  # Calculate current season
            self.C_price()  # Calculate the current rate
            self.C_diff()  # Calculate the difference between power produced and demand
            self.C_green()  # Calculate the amount of green power produced
            self.C_normalized_cost()  # Calculate the normalized cost to produce
            self.C_profit_margin()  # Calulate the kwh profit margin
            self.C_sold()  # Calculate the amount of power to sell


    def O_to_spreadsheet(self):
        """
        OUTPUT function to write a row to the spreadsheet
        """
        self.writer.writerow(self.O_power)

    def U_input_conditions(self):
        """
        UPDATE function to parse the an input condition row of the csv
        """
        # Modify the output power
        self.O_power["state"] = "2"
        self.O_power["time"] = self.cur_line[1]

        # Modify the cur power
        self.cur_pwr["time"] = self.cur_line[1]
        self.cur_pwr["demand"] = self.cur_line[2]
        self.cur_pwr["solar"] = self.cur_line[3]
        self.cur_pwr["nuclear"] = self.cur_line[4]
        self.cur_pwr["wind"] = self.cur_line[5]
        self.cur_pwr["hydro"] = self.cur_line[6]
        self.cur_pwr["gas"] = self.cur_line[7]
        self.cur_pwr["biofuel"] = self.cur_line[8]
        self.cur_pwr["neighbour"] = self.cur_line[9]

        # Aggregate temperatures into a list
        temps = []
        for i in range(10, 15):
            temps.append(float(self.cur_line[i]))
        self.cur_pwr["temps"] = temps

        self.cur_pwr["solar_coef"] = self.cur_line[15]
        self.cur_pwr["wind_coef"] = self.cur_line[16]
        self.cur_pwr["hydro_coef"] = self.cur_line[17]
        self.cur_pwr["neighbour_demand"] = self.cur_line[18]
        self.cur_pwr["neighbour_sell_price"] = self.cur_line[19]

        # Aggregate past power values into a list
        powers = []
        for i in range(20, 26):
            powers.append(float(self.cur_line[i]))
        self.cur_pwr["previous_power_values"] = powers

    def U_starting_conditions(self):
        """
        UPDATE function to parse a starting condition row
        """
        self.O_power["state"] = "0"
        self.O_power["time"] = self.cur_line[1]
        self.O_power["total"] = self.cur_line[2]
        self.O_power["solar"] = self.cur_line[3]
        self.prev_nuc = float(self.cur_line[4])
        self.O_power["nuclear"] = self.cur_line[4]
        self.O_power["wind"] = self.cur_line[5]
        self.O_power["hydro"] = self.cur_line[6]
        self.O_power["gas"] = self.cur_line[7]
        self.O_power["biofuel"] = self.cur_line[8]
        self.O_power["neighbour"] = self.cur_line[9]
        self.O_power["power_diff"] = self.cur_line[10]
        self.prev_diff = float(self.cur_line[10])
        self.O_power["green_power"] = self.cur_line[11]
        self.O_power["bought"] = self.cur_line[12]
        self.O_power["sold"] = self.cur_line[13]
        self.O_power["CO2_gen"] = self.cur_line[14]
        self.O_power["sell_price"] = self.cur_line[15]
        self.O_power["cost_to_make"] = self.cur_line[16]
        self.O_power["margin"] = self.cur_line[17]

    def C_nuclear_power(self):
        """
        CALCULATION function to calculate the amount of nuclear power available
        """

        if float(self.cur_line[4]) < 0:  # If we have a negative nuclear value (-999999)

            # If we didnt have over 100 MW of extra power power last time
            if self.prev_diff < 100:
                nuclear = self.prev_nuc + 0.01 * self.prev_nuc  # Incrase nuclear production by 1%

            # If we had over 400 MW of extra power
            elif self.prev_diff > 400:
                nuclear = self.prev_nuc - 0.01 * self.prev_nuc  # Decrease nuclear production by 1%
            else:
                nuclear = self.prev_nuc

            self.cur_line[4] = str(nuclear)  # Set the new nuclear power available
            self.prev_nuc = nuclear  # Set the current nuclear value to the previous value

    def C_hydro(self):
        """
        CALCULATION function to calculate the amount of hydro electricity to use
        """
        hydro = float(self.cur_pwr["hydro"])
        carbon_emissions_grams = hydro * 1000 * 4
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = hydro * 57

        self.O_power["total"] += hydro
        self.O_power["hydro"] = hydro
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_wind(self):
        """
        CALCULATION function to calculate the amount of wind power to use
        """
        wind = float(self.cur_pwr["wind"])
        carbon_emissions_grams = wind * 1000 * 13
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = wind * 133

        self.O_power["total"] += wind
        self.O_power["wind"] = wind
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_solar(self):
        """
        CALCULATION function to calculate the amount of solar power to use
        """

        solar = float(self.cur_pwr["solar"])
        carbon_emissions_grams = solar * 1000 * 105
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = solar * 481

        self.O_power["total"] += solar
        self.O_power["solar"] = solar
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_nuclear(self):
        """
        CALCULATION function to calculate the amount of nuclear power to use
        """
        nuclear = round(float(self.cur_pwr["nuclear"]), 0)
        carbon_emissions_grams = nuclear * 1000 * 6
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = nuclear * 68

        self.O_power["total"] += nuclear
        self.O_power["nuclear"] = nuclear
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_biofuel(self):
        """
        CALCULATION function to calculate the amount of biofuel to use
        """

        biofuel = float(self.cur_pwr["biofuel"])
        carbon_emissions_grams = biofuel * 1000 * 58
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = biofuel * 131

        self.O_power["total"] += biofuel
        self.O_power["biofuel"] = biofuel
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_neighbour(self):
        """
        CALCULATION function to calculate the amount of power to buy from the neighbour
        """

        neighbour = float(self.cur_pwr["neighbour"])

        self.needed_power = float(self.O_power["total"]) - float(self.cur_pwr["demand"])

        if self.needed_power < 0:
            if abs(self.needed_power) > neighbour:
                neighbour = float(self.cur_pwr["neighbour"])
                self.needed_power = self.needed_power - neighbour
            else:
                neighbour = abs(self.needed_power)
                self.needed_power = self.needed_power - neighbour
        else:
            neighbour = 0

        carbon_emissions_grams = neighbour * 1000 * 258
        carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        cost = neighbour * 160

        self.O_power["total"] += neighbour
        self.O_power["bought"] = neighbour
        self.O_power["neighbour"] = neighbour
        self.O_power["CO2_gen"] += carbon_emissions_tonnes
        self.O_power["cost_to_make"] += cost

    def C_gas(self):
        """
        CALCULATION function to calculate the amount of gas/oil to use.
        NOTE: that we no longer use coal in our model for sustainbability reasons.
        The code below is left commented for process however all values are simply set to 0.
        """
        # gas = float(self.cur_pwr["gas"])
        # carbon_emissions_grams = gas * 1000 * 909
        # carbon_emissions_tonnes = carbon_emissions_grams / (10**6)

        # cost = gas * 140

        # self.O_power["total"] += gas
        # self.O_power["gas"] = gas
        # self.O_power["CO2_gen"] += carbon_emissions_tonnes
        # self.O_power["cost_to_make"] += cost

        self.O_power["gas"] = 0

    def C_diff(self):
        """
        CALCULATION function to calculate the difference between the demand and the produced power
        """

        desired = float(self.cur_pwr["demand"])  # Get the desired power

        # Produced power
        nuclear = self.O_power["nuclear"]
        hydro = self.O_power["hydro"]
        solar = self.O_power["solar"]
        wind = self.O_power["wind"]
        biofuel = self.O_power["biofuel"]
        gas = self.O_power["gas"]
        neighbour = self.O_power["neighbour"]

        produced = nuclear + hydro + solar + wind + biofuel + gas + neighbour

        self.O_power["power_diff"] = produced - desired
        self.prev_diff = produced - desired

    def C_green(self):
        """
        CALCULATION function to calculate the amount of green power utilized
        """

        # Green energy sources
        hydro = self.O_power["hydro"]
        solar = self.O_power["solar"]
        wind = self.O_power["wind"]
        biofuel = self.O_power["biofuel"]

        green_power = hydro + solar + wind + biofuel

        self.O_power["green_power"] = green_power

    def C_normalized_cost(self):
        """
        CALCULATION function to detemine the cost to generate power for that hour.
        """
        cost = self.O_power["cost_to_make"]
        self.O_power["cost_to_make"] = cost / (self.O_power["total"] * 1000)

    def C_price(self):
        """
        CALCULATION function to determine the kwh rate based off the time and the season
        """
        if self.season == "Winter":
            if self.O_power["time"] in ["8:00", "9:00", "10:00", "18:00", "19:00"]:
                self.price = 13.4
            elif self.O_power["time"] in ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]:
                self.price = 9.4
            else:
                self.price = 6.5

        else:
            if self.O_power["time"] in ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]:
                self.price = 13.4
            elif self.O_power["time"] in ["7:00", "8:00", "9:00", "10:00", "17:00", "18:00"]:
                self.price = 9.4
            else:
                self.price = 6.5

        self.O_power["sell_price"] = self.price

    def C_season(self):
        """
        CALCULATION function to determin the current season based of the temperature reading
        """
        # Get the average of the temperatures
        if sum(self.cur_pwr["temps"])/len(self.cur_pwr["temps"]) < 4:
            self.season = "Winter"
        else:
            self.season = "Summer"

    def C_profit_margin(self):
        """
        CALCULATION function to detemrine the profit per kwh sold for the current hour.
        """
        self.O_power["margin"] = self.O_power["sell_price"] - self.O_power["cost_to_make"]

    def C_sold(self):
        """
        CALCULATION function to determine the excess power to be sold to the neighbour
        """
        if self.needed_power > 0:
            self.O_power["sold"] = self.needed_power
        else:
            self.O_power["sold"] = 0

if __name__ == "__main__":
    power_model("inputFile2.csv", "main-output.csv")

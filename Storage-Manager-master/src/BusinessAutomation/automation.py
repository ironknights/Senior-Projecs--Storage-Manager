"""Code written by Jacquesne Jones unless otherwise specified."""

import datetime
from src.DatabaseModel.format import date_object, get_months_between_dates


class OperationsModel:
    """This class holds any automated functions designed to maintain business rent, fees, and other operations."""
    def __init__(self, database):
        self.database = database
        self.last_time_check = datetime.datetime.now()

    def charge_units(self, month_start):
        """Loops through all units in database and adds any charges if necessary"""
        units = self.database.UnitModel.get_list()
        month = int(month_start) # Convert to integer for function
        # Go through each unit, get the number of months, and charge it based on delinquencies
        for unit in units:
            charge_months = self.__num_months_to_charge(unit, month)
            if charge_months > 0:
                for charge in range(charge_months):
                    self.database.TransactionModel.add_rent_charge(unit, unit.size.price)

    def check_hourly_events(self):
        """Checks to see if an hour has passed since the last time check for periodic program operations"""
        now = datetime.datetime.now()
        seconds = (now - self.last_time_check).total_seconds()
        if seconds > 3600:
            self.last_time_check = now
            return True
        return False

    def __num_months_to_charge(self, unit, month_start):
        """Returns the number of months to charge a unit

        :return Number of months a charge is needed for, zero indicates unit does not need to be charged"""
        # Get the date of the latest charge
        last_charge = self.database.TransactionModel.get_last_charge(unit)
        # Check to make sure an initial charge was created, if not, return -1 to indicate an error
        if not last_charge:
            return -1
        last_charge_date = date_object(last_charge.created)

        # If the unit isn't occupied no reason to continue checking
        if unit.status != "Occupied":
            return 0
        # Find the number of months between the last charge date and now
        now = datetime.date.today()
        month_difference = get_months_between_dates(last_charge_date, now, month_start)
        return month_difference

"""This module has various formatting code and utility functions that are used throughout the system.

Code written by Jacquesne Jones unless otherwise specified.
"""
import datetime


# Utility functions for states
def get_state_list():
    """Returns a state description from a number value"""
    return {
        1: ["AL", "Alabama"],
        2: ["AK", "Alaska"],
        3: ["AZ", "Arizona"],
        4: ["AR", "Arkansas"],
        5: ["CA", "California"],
        7: ["CO", "Colorado"],
        8: ["CT", "Connecticut"],
        9: ["DE", "Delaware"],
        10: ["FL", "Florida"],
        11: ["GA", "Georgia"],
        12: ["HI", "Hawaii"],
        13: ["ID", "Idaho"],
        14: ["IL", "Illinois"],
        15: ["IN", "Indiana"],
        16: ["IA", "Iowa"],
        17: ["KS", "Kansas"],
        18: ["KY", "Kentucky"],
        19: ["LA", "Louisiana"],
        20: ["ME", "Maine"],
        21: ["MD", "Maryland"],
        22: ["MA", "Massachusetts"],
        23: ["MI", "Michigan"],
        24: ["MN", "Minnesota"],
        25: ["MS", "Mississippi"],
        26: ["MO", "Missouri"],
        27: ["MT", "Montana"],
        28: ["NE", "Nebraska"],
        29: ["NV", "Nevada"],
        30: ["NH", "New Hampshire"],
        31: ["NJ", "New Jersey"],
        32: ["NM", "New Mexico"],
        33: ["NY", "New York"],
        34: ["NC", "North Carolina"],
        35: ["ND", "North Dakota"],
        36: ["OH", "Ohio"],
        37: ["OK", "Oklahoma"],
        38: ["OR", "Oregon"],
        39: ["PA", "Pennsylvania"],
        40: ["RI", "Rhode Island"],
        41: ["SC", "South Carolina"],
        42: ["SD", "South Dakota"],
        43: ["TN", "Tennessee"],
        44: ["TX", "Texas"],
        45: ["UT", "Utah"],
        46: ["VT", "Vermont"],
        47: ["VA", "Virginia"],
        48: ["WA", "Washington"],
        49: ["WV", "West Virginia"],
        50: ["WI", "Wisconsin"],
        51: ["WY", "Wyoming"]
    }


def state_list(long=False):
    """Generates a list of states, 2-letter if long is false, otherwise full state name"""
    states = []
    if long:
        index = 1
    else:
        index = 0
    list_states = get_state_list()
    for state in list_states:
        states.append(list_states[state][index])
    return states


def get_state_num(state_text):
    """Gets the integer value based on a state name in text to store in state fields"""
    states = get_state_list()
    for state in states:
        if state_text in states[state]:
            return state
    return 0


def get_state(state_id, long=False):
    """Returns the state name from ID"""
    # First check if state is valid, if not, return empty string
    if state_id < 1 or state_id > 51:
        return ""
    if long:
        index = 1
    else:
        index = 0
    return get_state_list()[state_id][index]


def name_last_first(last, first, middle):
    return f"{last}, {first}{f' {middle[0].upper()}' if middle else ''}"


def price_format(price):
    return f"$ {float(price):.2f}"


def date_object(date):
    """Returns a datetime.date object from a given database date string"""
    date = str(date)
    # Extract string values
    year_str = date[:4]
    month_str = date[5:7]
    day_str = date[8:10]
    # Convert to integers
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    # Return in datetime format
    return datetime.date(year, month, day)


def date_format(date):
    """Returns a formatted string for use in UI.

    :param date The date to format, can be either a date string from database or a datetime.date object.
    """
    # If a string is passed first convert to datetime.date
    if type(date) == str:
        date = date_object(date)
    return f"{date.month}/{date.day}/{date.year}"


def get_months_between_dates(date1, date2, month_start):
    """Returns the number of months between two dates"""
    months = 0
    # date1 = 2/1/2020, date2 = 12/1/2019
    if date1 == date2:
        return 0
    if date1 > date2:
        later_date = date1
        early_date = date2
    else:
        later_date = date2
        early_date = date1
    early_year = early_date.year
    early_month = early_date.month
    # Loop while the earlier date is still months before the later date, adjusting for year changes
    while early_year < later_date.year or early_month < later_date.month:
        months += 1
        early_month += 1
        # Check for year switch
        if early_month > 12:
            early_month = 1
            early_year += 1
    # Check to make sure the month start has already passed
    if months > 0 and later_date.day < month_start:
        months -= 1
    return months

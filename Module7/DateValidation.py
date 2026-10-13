# The problem here was that the original regex was close, but it was missing a few details.
# It did not fully match the MM/DD/YYYY format and could accidentally allow some invalid date values.
#
# I fixed it by using a pattern that requires exactly 2 digits for the month, a slash,
# exactly 2 digits for the day, another slash, and then 4 digits for the year.
# That makes the validation much more accurate and keeps the input in the format the user is supposed to enter.

import re

def validate_date(date_str):
    pattern = r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(\d{4})$"

    if re.match(pattern, date_str):
        print("Valid date format.")
        return True
    else:
        print("Invalid date format. Please enter the date in the format MM/DD/YYYY.")
        return False


date_input = input("Please enter a date in the format MM/DD/YYYY: ")
validate_date(date_input)

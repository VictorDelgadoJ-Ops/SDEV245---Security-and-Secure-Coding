# The issue with the original pattern was that it was too loose.
# It did not clearly restrict the name to a valid file format, so it could accept values that were not real filenames.
#
# I fixed it by using a pattern that only accepts letters, numbers, dots, underscores, and dashes,
# followed by a valid extension like .java, .py, .cs, or .txt.
# That keeps the validation close to what the user is actually expected to enter.

import re

def validate_filename(filename):
    pattern = r"^[A-Za-z0-9_.-]+\.(java|py|cs|txt)$"

    if re.match(pattern, filename):
        print("Valid filename format.")
        return True
    else:
        print("Invalid filename format. Please enter a filename with an extension.")
        return False

filename_input = input("Please enter a filename containing code with one of the following extensions: java, py, cs, txt")
validate_filename(filename_input)

import csv
from datetime import date
import re

file_to_use = 'test.csv'
output_file = 'solution.csv'
state_file = 'state_abbreviations.csv'

# I made this dict in an attempt to convert
# natural language in dates to month numbers
# for the iso date parser.
months = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

# This extra function is pretty ugly but I think it
# generally satisfies the output requirements.
# I am trying to get information from start date field
# and clean it into a format the date parser can read.


def convert_to_date(date_item, list_row):
    # this will allow me to split the string at
    # the various delimiters that are used
    r = '[,;/ -]'
    if date_item:
        date_split = re.split(r, date_item)
        try:
            # Using try here.. if the item can't be parsed to an int
            # it will fail and go to the except block
            # I got empty strings in some of the split items
            # so using the filter to eliminate them.
            date_split = filter(None, date_split)
            date_list = []
            for item in date_split:
                if item in months:
                    # this matches a natural language month
                    # to an int from the months dict above
                    month_int = months[item]
                    date_list.append(month_int)

                else:
                    item = int(item)
                    date_list.append(item)
                if len(date_list) == 3:
                    sorted_date = sorted(date_list, reverse=True)
                    # assumming that the largest number will be the year
                    # which is what the isoformatter needs as the first
                    # argument.
                    if 12 < sorted_date[1] <= 31:
                        # This attempts to verify that
                        # A number that obviously can't be
                        # a month (ie more than 12)
                        # is moved to the end of the array
                        sorted_date[1], sorted_date[
                            2] = sorted_date[2], sorted_date[1]
                    formatted_date = date(
                        sorted_date[0], sorted_date[1], sorted_date[2]).isoformat()
                    return formatted_date
                else:
                    # this attempts to filter out bad dates and move them
                    # to the next column.
                    shift_item = date_item
                    date_item = ''
                    list_row.append(shift_item)
        # this comes up when there is a value
        # that can't be parsed into an int            
        except ValueError:
            if date_item == "start_date":
                # This adds the new column to the csv
                # and makes sure that the 'start_date' field
                # keeps teh correct name
                list_row.append("start_date_description")
                return date_item
            else:
                list_row.append(date_item)


def parse_csv(input_file, output_file, ref_file):
    with open(input_file, 'rb') as csv_in, open(output_file, 'wb') as csv_out, open(ref_file, 'rb') as states:
        reader = csv.reader(csv_in, delimiter=',')
        writer = csv.writer(csv_out, delimiter=',')
        state_ref = csv.reader(states, delimiter=',')
        state_dict = {}

        for row in state_ref:
        # Here I'm creating a dict from the states csv.
        # with state_abbr : state_name
            state_dict[row[0]] = row[1]

        # for state in columns['state']:
        #     if len(state) == 2:
        #         state = state_dict[state]

        for row in reader:
            row[10] = convert_to_date(row[10], row)
            # This removes excess whitespace from the bio string
            row[8] = " ".join(row[8].split())
            if len(row[5]) == 2:
            # This checks if the data item is 2 characters long
            # Basically just to skip the title row.
            # Then using the abbreviation as a key, matches to the state
            # dict
                row[5] = state_dict[row[5]]
            writer.writerow(row)


if __name__ == "__main__":
    parse_csv(file_to_use, output_file, state_file)

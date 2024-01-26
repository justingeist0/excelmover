import csv
import openpyxl


def print_text_colors(file_path, sheet_name, column):
    # Load the workbook and select the specified sheet
    in_red = []
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    for cell in sheet[column]:
        color = cell.font.color
        if color is not None:
            in_red.append(color.rgb != 'FF000000')
    return in_red


# Example usage
file_path = 'utils/justinlist2024.xlsx'  # Replace with your file path
sheet_name = 'SHEET1'               # Replace with your sheet name
column = 'A'                        # Replace with your column letter

text_color = print_text_colors(file_path, sheet_name, column)

print(text_color)


class SexOffender:
    def __init__(self, name, city, facebook_link, in_red):
        self.name = name
        self.city = city
        self.facebook_link = facebook_link
        self.in_red = in_red

    def to_json(self):
        return {
            "name": self.name,
            "city": self.city,
            "facebook_link": self.facebook_link,
            "in_red": self.in_red,
        }


# Open CSV file
with open('utils/csv_copy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    # Read CSV file and create instances of SexOffender
    offenders = []
    row_number = 0
    for row in reader:
        row_number += 1
        if row_number == 1:
            continue # Skip header row

        name = row[3].strip()  # Strip leading/trailing whitespaces
        city = row[2]
        facebook_link = row[0] if len(row) > 2 else None  # In case Facebook link is missing


        if city and name:  # Check if city and name are not None or empty
            offenders.append(SexOffender(name, city, facebook_link, text_color[row_number-2]))
            print(row_number, text_color[row_number])

with open('mamamia.csv', 'w') as file:
    file.write(f'link,in_red,city,name\n')
    for o in offenders:
        file.write(f'"{o.facebook_link}","{o.in_red}","{o.city}","{o.name}"\n')

# Write instances to a new file
with open('../offenders.js', 'w') as output_file:
    output_file.write("const offenders = [\n")
    for offender in offenders:
        mname = offender.name.replace('"', '\\"')
        mcity = offender.city.replace('"', '\\"')
        output_file.write(f'''{{
          "name": "{mname}",
          "city": "{mcity}",
          "facebook": "{offender.facebook_link}",
          "visited": {str(offender.in_red).lower()}
        }},''')
    output_file.write("];\n\n")
    output_file.write("module.exports = offenders")

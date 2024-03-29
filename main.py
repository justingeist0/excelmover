import csv

CSV_FILE_NAME = 'data.csv'

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
with open(CSV_FILE_NAME, newline='') as csvfile:
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
        is_red = row[1]
        facebook_link = row[0] if len(row) > 3 else None  # In case Facebook link is missing

        print(name, "name")
        print(city, "city")

        if city and name:  # Check if city and name are not None or empty
            offenders.append(SexOffender(name, city, facebook_link, is_red))


# Write instances to a new file
with open('offenders.js', 'w') as output_file:
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

import csv
import subprocess

# Run pycodestyle and capture the output
result = subprocess.run(['pycodestyle', './rps.py'],
                        capture_output=True, text=True)

# Parse the output
lines = result.stdout.splitlines()

# Write to result CSV file
with open('result.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['File', 'Line', 'Column', 'Error'])

    if not lines:
        print("This file rps.py is not issue pycodestyle")
    else:
        for line in lines:
            parts = line.split(':')
            if len(parts) >= 4:
                file = parts[0].strip()
                line_number = parts[1].strip()
                column = parts[2].strip()
                error = ':'.join(parts[3:]).strip()
                csvwriter.writerow([file, line_number, column, error])
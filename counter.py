import os

data_dir = './DATA'


total_values = 0
for root, dirs, files in os.walk(data_dir):
    for fn in files:
        file_path = os.path.join(root, fn)
        with open(file_path, 'r') as file:
            # Read the single line of integers from the CSV file
            line = file.readline().strip()
            # Split the line into individual values
            values = [val for val in line.split(',')]
            # Count the values and add to the total
            total_values += len(values)


print(f"Total vals: {total_values}")

for root, dirs, files in os.walk(data_dir):
    for fn in files:
        file_path = os.path.join(root, fn)
        with open(file_path, 'r') as file:
            # Read the single line of integers from the CSV file
            line = file.readline().strip()
            # Split the line into individual values
            values = [val for val in line.split(',')]
            # Count the values
            count_values = len(values)
            print(f"File: {file_path}, Count of Values: {count_values}")

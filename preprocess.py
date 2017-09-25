"""
Preprocess dataset from import.io to prepare for graphing
"""
import csv

BATTERY_SIZES = [75, 100, 60, 70, 85, 90]
MODEL_NAMES = {}
for battery_size in BATTERY_SIZES:
    for perf in 'P', '':
        for drive in 'D', '+', '':
            MODEL_NAMES[perf +
                        str(battery_size) +
                        drive] = (perf == 'P', battery_size, drive == 'D')


def guess_battery(row):
    """Try to guess the battery kwh size"""
    title = row['text_link/_title']
    description = row['text_description']
    for model in MODEL_NAMES:
        if model in title.upper().upper():
            return MODEL_NAMES[model][1]
        if model in description.upper():
            return MODEL_NAMES[model][1]
    for bsize in BATTERY_SIZES:
        if str(bsize) in title:
            return bsize
        if str(bsize) + "kwh" in description.lower():
            return bsize
        if str(bsize) + ' kwh' in description.lower():
            return bsize
    for bsize in BATTERY_SIZES:
        if str(bsize) in description:
            return bsize


def guess_performance(row):
    """Try to guess whether the car is a performance (P) model"""
    title = row['text_link/_title']
    description = row['text_description']
    for model in MODEL_NAMES:
        if model in title.upper().upper():
            return MODEL_NAMES[model][0]
        if model in description.upper():
            return MODEL_NAMES[model][0]
    if 'performance' in title.lower():
        return True
    return False


def guess_awd(row):
    """Try to guess whether the car is an AWD (D) model"""
    title = row['text_link/_title']
    description = row['text_description']
    for model in MODEL_NAMES:
        if model in title.upper().upper():
            return MODEL_NAMES[model][2]
        if model in description.upper():
            return MODEL_NAMES[model][2]
    return False


NAME_MAP = {
    'year': 'text_value_1_numbers',
    'miles': 'col_value_numbers',
    'price': 'listunstyledh4_value_prices',
    'battery': guess_battery,
    'performance': guess_performance,
    'awd': guess_awd
}

OUTPUT_KEYS = NAME_MAP.keys()


def process_row(row):
    """Process only one row"""
    output_row = {}
    for name, value in NAME_MAP.items():
        if isinstance(value, str):
            output_row[name] = row[value]
        else:
            output_row[name] = value(row)
    return output_row


def process_file():
    """Do all the things"""
    output = []
    with open('dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            output.append(process_row(row))

    with open('dataset.processed.csv', 'w') as outputfile:
        writer = csv.DictWriter(outputfile, NAME_MAP.keys())
        writer.writeheader()
        for output_row in output:
            writer.writerow(output_row)


if __name__ == '__main__':
    process_file()

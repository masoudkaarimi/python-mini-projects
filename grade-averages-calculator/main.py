import csv
from statistics import mean


def get_average(students):
    try:
        these_grades = [int(grade) for grade in students[1:] if grade.isdigit()]
        average = mean(these_grades)
    except ValueError:
        average = None
    except IndexError:
        average = None

    return students[0], average


with open('grades.csv', newline='') as file:
    reader = csv.reader(file)
    names = []
    averages = []
    max_average = None
    max_name = None
    for row in reader:
        if row:
            name, average = get_average(row)
            if average is not None:
                names.append(name)
                averages.append(average)
                print('Average of %s is: %2.2f' % (name, average))
                # Check and update max average and associated name
                if max_average is None or average > max_average:
                    max_average = average
                    max_name = name
            else:
                print(f"Failed to calculate average for {name}, due to invalid data.")

    if max_average is not None:
        print(f'\nMax average is: {max_average:2.2f} by {max_name}\n')
    else:
        print("No valid averages available.")

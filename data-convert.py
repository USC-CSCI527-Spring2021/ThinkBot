import csv
import shutil


csv_file_name = '/Users/rishabhgandhewar/Desktop/pics/M-train-2021-03-07/training_data.csv'
with open(csv_file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        from_dir = '/Users/rishabhgandhewar/Desktop/pics/M-train-2021-03-07/train_pics/' + row[0].split('/')[-1]
        to_dir = '/Users/rishabhgandhewar/Desktop/pics/M-train-2021-03-07/' + row[1].split()[0] + '/m' + row[0].split('/')[-1]
        shutil.move(from_dir,to_dir)
        line_count += 1
    print(f'Processed {line_count} lines.')

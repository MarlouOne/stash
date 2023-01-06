

# INSERT INTO "main"."Answers"
# ("id", "id_questions", "text", "status")
# VALUES (1, 2, '3', 4);
import csv

file_name = ''

with open(file_name, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
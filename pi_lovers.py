from Database import Database
from ProcessLines import ProcessLines


'''
    gender:
    male = 0
    female = 1
'''
gender = 0


def main():
    global gender
    database = Database()
    database.gender = gender
    process_lines = ProcessLines()
    while True:
        line = database.get_line()
        line_processed = process_lines.process_line(line)
        print(line)
        print(line_processed)
        if line != line_processed:
            database.insert_post(line_processed)


if __name__ == '__main__':
    main()

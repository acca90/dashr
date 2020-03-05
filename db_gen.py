import mysql.connector
from random import seed, random, choice, randint
import datetime
import string

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rfgejgyso1XQ3",
    database='cache_this'
)


def gen_data(seed_number):
    seed(seed_number)
    return (
        ''.join(choice(string.ascii_lowercase) for _ in range(25)),
        datetime.datetime.strptime('{} {}'.format(randint(1, 366), randint(1990, 2020)), '%j %Y'),
        datetime.datetime.strptime('{} {}'.format(randint(1, 366), randint(1990, 2020)), '%j %Y'),
        round((random() * randint(0, 10)), 2),
        round((random() * randint(0, 10)), 2),
        randint(0, 10),
        randint(0, 10),
        randint(0, 10),
        randint(1000000, 9999999)
    )


print('==== STARTING')
i = 1
while i <= 100000:
    sql = " INSERT INTO cache_this.prety_large_table " \
          " (field02, field03, field04, field05, field06, field07, field08, field09, field10) " \
          " VALUES  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " \
          % gen_data(i)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        i += 1
    except Exception as e:
        print(sql, str(e), sep='\n')


conn.close()
print('==== FINISHED')



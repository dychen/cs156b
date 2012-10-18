import psycopg2
import code

def create_data_table(cursor):
    sql_cmd = "CREATE TABLE data (user_id integer NOT NULL, movie_id integer NOT NULL, date integer NOT NULL, rating float, index integer, PRIMARY KEY (user_id, movie_id));"
    cursor.execute(sql_cmd)
    print "Table data created"

def insert_data_table(cursor):
    input_filename = 'all.dta'
    f = open('../mu/' + input_filename, 'r')
    i = 0
    sql_cmd = "INSERT INTO data (user_id, movie_id, date, rating) VALUES "
    insert_values = []
    for line in f:
        user_id, movie_id, date, rating = line.split()
        insert_values.append("(%s, %s, %s, %s)" % (user_id, movie_id, date, rating))
        i += 1
        if i % 1000000 == 0 and i != 0:
            cursor.execute(sql_cmd + ','.join(insert_values))
            connection.commit()
            insert_values = []
            print i
    cursor.execute(sql_cmd + ','.join(insert_values))
    f.close()
    print "%i values inserted into table data." % i

def main():
    conn_str = "host='localhost' dbname='cs156b'"
    connection = psycopg2.connect(conn_str)
    cursor = connection.cursor()
    create_data_table(cursor)
    insert_data_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
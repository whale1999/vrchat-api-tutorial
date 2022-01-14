import psycopg2

from config import DATABASE_URL


def load_table(table_name):
    
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM ' + table_name + ';')
            result =curs.fetchall()
    return result


def insert_loggined_friends(friends):
     with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                for display_name in friends:
                    display_name.replace('"', '')
                    curs.execute(
                        "INSERT INTO loggined_friends (name) VALUES ('" + display_name + "');")


def delete_table_contents(table_name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute('delete FROM ' + table_name + ';')

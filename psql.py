import psycopg2

from config import DATABASE_URL
from slack import send_slack_message

error_message = 'An error has occurred in the database processing..'


def load_table(table_name):
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                curs.execute('SELECT * FROM ' + table_name + ';')
                result =curs.fetchall()
        return result
    except:
        send_slack_message(error_message)


def insert_loggined_friends(friends):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as curs:
                    for display_name in friends:
                        display_name.replace('"', '')
                        curs.execute(
                            "INSERT INTO loggined_friends (name) VALUES ('" + display_name + "');")
    except:
        send_slack_message(error_message)


def delete_table_contents(table_name):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                curs.execute('delete FROM ' + table_name + ';')
    except:
        send_slack_message(error_message)
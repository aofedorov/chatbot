import sqlite3, os
import pymysql


def connection_mysql():
    return pymysql.connect(
        user="u51313",
        password="shegaeth",
        host="78.108.80.76",
        database="b51313_librarybot",
        charset='utf8mb4'
    )

def initiate():
    # table 'users'
    try:
        connection = connection_mysql()
        conn = connection.cursor()
        conn.execute("SELECT * FROM users;")
        print("[database]: users [+]")
        conn.close()
    except:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, chat_id TEXT, store TEXT);")
        print("[database]: users was create")
        conn.close()

    # table 'books'
    try:
        connection = connection_mysql()
        conn = connection.cursor()
        conn.execute("SELECT * FROM books;")
        print("[database]: books [+]")
        conn.close()
    except:
        conn.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, link TEXT);")
        print("[database]: books was create")
        conn.close()

    # table 'faq'
    try:
        connection = connection_mysql()
        conn = connection.cursor()
        conn.execute("SELECT * FROM faq;")
        print("[database]: faq [+]")
        conn.close()
    except:
        conn.execute("CREATE TABLE faq(id INTEGER PRIMARY KEY, faq_text TEXT);")
        conn.execute(
            f"INSERT INTO faq(faq_text) VALUES('FAQ');"
        )
        connection.commit()
        print("[database]: faq was create")
        conn.close()

class data_base():
    def __init__(self):
        self.connection = connection_mysql()

    # def create_book(self, title, author, isbn, link):
    #     self.connection.cursor().execute(
    #         f"INSERT INTO book(title, author, isbn, link) VALUES({title}, {author}, {isbn}, {link});"
    #     )
    #     self.connection.commit()    

    # books
    def get_books(self):
        with connection_mysql() as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                "SELECT * FROM books;"
            )
            connection.commit()
            
            return cursor.fetchall()

    def get_book(self, bid):
        with connection_mysql() as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                f"SELECT * FROM books WHERE id='{bid}';"
            )

            return cursor.fetchone()

    # faq
    def update_faq(self, faq_text):
        with connection_mysql() as connection:
            cursor = connection.cursor().execute(
                f"UPDATE faq SET faq_text='{faq_text}' WHERE id='0';"
            )
            connection.commit()

    def get_faq(self):
        with connection_mysql() as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                f"SELECT * FROM faq WHERE id='0';"
            )

            return cursor.fetchone()[1]


    # users
    def create_user(self, chat_id):
        with connection_mysql() as connection:
            users = self.get_users()
            print(users)
            for i in users:
                print(i)
                if int(i[1]) == int(chat_id):
                    return 0

            connection.cursor().execute(
                f"INSERT INTO users(chat_id, store) VALUES('{chat_id}', '');"
            )
            connection.commit()

    def get_users(self):
        with connection_mysql() as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                "SELECT * FROM users;"
            )
            users = cursor.fetchall()

            print(users)

            return users

    def get_user(self, chat_id):
        with connection_mysql() as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                f"SELECT * FROM users WHERE chat_id='{chat_id}';"
            )
            connection.commit()

            return cursor.fetchone()

    def update_store(self, chat_id, store):
        with connection_mysql() as connection:
            cursor = connection.cursor().execute(
                f"UPDATE users SET store='{store}' WHERE chat_id='{chat_id}';"
            )
            connection.commit()



    # def delete_event(self, event_id):
    #     cursor = self.connection.cursor().execute(
    #         f"DELETE FROM event WHERE id='{event_id}';"
    #     )
    #     self.connection.commit()


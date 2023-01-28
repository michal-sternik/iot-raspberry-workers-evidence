import sqlite3
import os

def create_database():
    if os.path.exists("./workers.db"):
        os.remove("./workers.db")
        print("An old database removed.")
    connection = sqlite3.connect("./workers.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE PRACOWNIK(
                    pracownik_id INTEGER PRIMARY KEY,
                    imie text not null,
                    nazwisko text not null ,
                    IDKarty text,
                    data_zapisania timestamp
                    )""")
    cursor.execute("""CREATE TABLE ODBICIE_KARTY(
                    odbicie_karty_id INTEGER PRIMARY KEY,
                    data_rozpoczecia timestamp,
                    data_zakonczenia timestamp,
                    pracownik_id INTEGER NOT NULL,
                    FOREIGN KEY (pracownik_id) REFERENCES PRACOWNIK (pracownik_id)
                    )""")
    connection.commit()
    connection.close()
    print("The new database created.")

def get_work_time(card_id):
    connection = sqlite3.connect("./workers.db")
    cursor = connection.cursor()
    cursor.execute("SELECT data_rozpoczecia, data_zakonczenia FROM ODBICIE_KARTY WHERE pracownik_id = ?", (card_id,))
    work_time = cursor.fetchall()
    connection.close()
    return work_time

if __name__ == "__main__":
    create_database()

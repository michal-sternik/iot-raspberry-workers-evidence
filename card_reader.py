#!/usr/bin/env python3

# import paho.mqtt.client as mqtt
# import tkinter
# import tkinter
import datetime
import sqlite3
import time


import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
# from mfrc522 import MFRC522
# import RPi.GPIO as GPIO

# import board
# import RPi.GPIO as GPIO

# from config import * 


# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
# client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
# window = tkinter.Tk()

# def call_worker(worker_name):
#     client.publish("worker/name", worker_name + "." + terminal_id,)




# def connect_to_broker():
#     # Connect to the broker.
#     client.connect(broker)
#     # Send message about conenction.
#     call_worker( card_uid + "." + current_time)


# def disconnect_from_broker():
#     # Send message about disconenction.
#     call_worker("Client disconnected")
#     # Disconnet the client.
#     client.disconnect()


# def run_sender():
#     connect_to_broker()


#     disconnect_from_broker()


def register_card(id_karty):
    connection = sqlite3.connect("./workers.db")
    cursor = connection.cursor()

    # card_id = input("Podaj id karty do zarejestrowania: ")
    cursor.execute("SELECT * FROM PRACOWNIK WHERE IDKarty=?", (id_karty,))    
    result = cursor.fetchone()
    if result:
        print("This card is already registered in the system.")
        return
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    cursor.execute(f"INSERT INTO PRACOWNIK(imie, nazwisko, IDKarty,data_zapisania) VALUES (?,?,?,?)",(name,surname,id_karty,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    connection.commit()
    print("Card registered successfully!")
    connection.close()


# def buzzer(state):
#     GPIO.output(buzzerPin, not state)  # pylint: disable=no-member

def listHours(id_karty):
    # MIFAREReader = MFRC522()
    while True:
        # (status, tag_type) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # if status == MIFAREReader.MI_OK:

        #     (status, uid) = MIFAREReader.MFRC522_Anticoll()
        #     if status == MIFAREReader.MI_OK:
                # global card_uid
                # card_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
                # card_uid = input("Podaj card uid: ")#to zmienic na to wyzsze zeby odczytywalo z karty

                connention = sqlite3.connect("./workers.db")
                cursor = connention.cursor()
                cursor.execute("SELECT * FROM PRACOWNIK WHERE IDKarty=?", (id_karty,))
                odczytKarty = cursor.fetchone()

                if odczytKarty is None:
                    connention.commit()
                    connention.close()
                    print("Nie ma karty - najpierw zarejestruj kartę!")
                    break


                idPracownika = odczytKarty[0]

                cursor.execute("SELECT * FROM ODBICIE_KARTY WHERE pracownik_id=?", (idPracownika,))    
                result = cursor.fetchall()


                
                if result:


                    # convert to string


                    if result:
                        print("\n" + str(odczytKarty[1]) + " " + str(odczytKarty[2]) + " - godziny pracy.")
                        # rows = cursor.fetchall()

                        for row in result:
                            if row[2] is None:
                                actual = "still working"
                            else:
                                actual = row[2].split(" ")[1]
                            print(str(row[0])+". " + str(row[1]) + " - " + str(actual))
                        
                    else:
                        print(str(odczytKarty[1]) + " " + str(odczytKarty[2]) + " nie posiada zarejestrowanych godzin pracy.")

                else:
                    connention.commit()
                    connention.close()

                    # buzzer(True)
                    # time.sleep(1)
                    # buzzer(False)
                    # global current_time
                    # print("Card registered! ID: " + card_uid + " Time: " + current_time)
                    # run_sender()
                    print("Nie ma karty - najpierw zarejestruj kartę!")
                    

                break


def run(id_karty):
    # MIFAREReader = MFRC522()
    while True:
        # (status, tag_type) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # if status == MIFAREReader.MI_OK:

        #     (status, uid) = MIFAREReader.MFRC522_Anticoll()
        #     if status == MIFAREReader.MI_OK:
                # global card_uid
                # card_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
                # card_uid = input("Podaj card uid: ")#to zmienic na to wyzsze zeby odczytywalo z karty

                connention = sqlite3.connect("./workers.db")
                cursor = connention.cursor()
                cursor.execute("SELECT * FROM PRACOWNIK WHERE IDKarty=?", (id_karty,))    
                result = cursor.fetchone()

                
                if result:
                    odczytKarty = result 
                    now = datetime.datetime.now()

                    # convert to string
                    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute("SELECT * FROM ODBICIE_KARTY WHERE pracownik_id=? and data_rozpoczecia is not null and data_zakonczenia is null", (odczytKarty[0],))    
                    result = cursor.fetchone()

                    if result:
                        print("Do widzenia " + str(odczytKarty[1]) + " " + str(odczytKarty[2])) 
                        cursor.execute("UPDATE ODBICIE_KARTY SET data_zakonczenia = ? WHERE pracownik_id = ? and data_zakonczenia is null", (date_time_str, result[3]))
                        connention.commit()
                        connention.close()
                        
                    else:
                        print("Karta się zgadza - witaj " + str(odczytKarty[1]) + " " + str(odczytKarty[2])) 
                        cursor.execute("INSERT INTO ODBICIE_KARTY(data_rozpoczecia, pracownik_id) VALUES (?,?)", (date_time_str, odczytKarty[0]))
                        print('Start pracy:', date_time_str)
                        connention.commit()
                        connention.close()

                else:
                    connention.commit()
                    connention.close()

                    # buzzer(True)
                    # time.sleep(1)
                    # buzzer(False)
                    # global current_time
                    # print("Card registered! ID: " + card_uid + " Time: " + current_time)
                    # run_sender()
                    print("Nie ma karty - najpierw zarejestruj kartę!")
                    

                break


        

def przylozKarte():
    global id_karty
    id_karty = input("Podaj id karty: ")



# if __name__ == '__main__':
#     print("\nProgram started")

#     while 1:
#         przylozKarte()

#         x = input("Wybierz 1 by wejsc/wyjsc, 2 by wpisac karte dla uzytkownika, 3 by wyswietlic liczbe godzin: ")
#         if x == '1':
#             run(id_karty)
#         elif x == '2':
#             register_card(id_karty)
#         elif x == '3':
#             listHours(id_karty)
#         time.sleep(2)

#     print("\nProgram finished")





    #implementacja dla komunikacji:


client = mqtt.Client("ODBIERACZS")

def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    card_id = message_decoded[0]

    connention = sqlite3.connect("./workers.db")
    cursor = connention.cursor()
    cursor.execute("SELECT * FROM PRACOWNIK WHERE IDKarty=?", (card_id,))    
    result = cursor.fetchone()

    if result:
        print("Karta przypisana do " + str(result[1]) + " " + str(result[2])) 
    else:
        print("Karta nie posiada właściciela")



    x = input("MENU:\n 1 - wejscie/wyjscie z pracy,\n 2 - przypisanie karty dla uzytkownika,\n 3 - wyswietlenie liczby godzin przepracowanych,\n   - dowolny przycisk by wyjść: ")
    if x == '1':
        run(card_id)
    elif x == '2':
        register_card(card_id)
    elif x == '3':
        listHours(card_id)
    else: 
        print("=================================")
        return
    print("=================================")
    time.sleep(2)


def print_log_to_window():

    # print_log_window = tkinter.Tk()

    # print_log_window.mainloop()
    pass


def connect_to_broker():
    client.on_message = process_message
    client.connect("192.168.0.111", 1885, 60)#ip drugiej maszyny tu podać
    client.subscribe("test/status") 
    client.loop_forever()



    # Connect to the broker.
    # client.connect(broker, 1885)
    # Send message about conenction.
    # client.on_message = process_message
    # Starts client and subscribe.
    # client.loop_start()
    # client.subscribe("worker/name")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()


    # window.mainloop() to wywalamy chyba bo tkinter
    disconnect_from_broker()


if __name__ == "__main__":
    print("Witaj w systemie ewidencji czasu pracy pracowników. Zeskanuj kartę w odpowiednim miejscu.")
    run_receiver()
    print("XD2")
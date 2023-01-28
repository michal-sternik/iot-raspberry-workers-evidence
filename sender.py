import paho.mqtt.client as paho
import sys
client = paho.Client()

# if client.connect("localhost", 1885, 60) != 0:
#     print("Could not..")
#     sys.exit(-1)

# client.publish("test/status", "Hello world from paho-mqtt!", 0)
# client.loop_forever()

# client.disconnect()


# def call_worker(card_uid):
#     client.publish("test/status", card_uid, 0)




# def connect_to_broker():
#     # Connect to the broker.
#     client.connect("localhost", 1885, 60)
#     # Send message about conenction.
#     call_worker(card_uid)
#     client.loop_start()
#     client.disconnect()



# def disconnect_from_broker():
#     # Send message about disconenction.
#     call_worker("Client disconnected")
#     # Disconnet the client.
#     client.disconnect()


# def run_sender():
#     connect_to_broker()


#     disconnect_from_broker()





# def buzzer(state):
#     GPIO.output(buzzerPin, not state)  # pylint: disable=no-member

def run():
    # MIFAREReader = MFRC522()

    client.connect("localhost", 1885, 60)

    while True:


    #     (status, tag_type) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #     if status == MIFAREReader.MI_OK:

    #         (status, uid) = MIFAREReader.MFRC522_Anticoll()
    #         if status == MIFAREReader.MI_OK:
                global card_uid
                card_uid = input("Podaj id karty do zarejestrowania: ")
                client.publish("test/status", card_uid, 0)
                client.loop_start()

                # # card_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])

                # connention = sqlite3.connect("./workers.db")
                # cursor = connention.cursor()
                # x=cursor.execute(f"SELECT * FROM PRACOWNIK WHERE IDKarty={card_uid}")
                # result = cursor.fetchone()
                
                # if result:
                #     print("karta ma juz pracownika") 
                #     connention.commit()
                #     connention.close()
                #     break

                # connention.commit()
                # connention.close()

                # buzzer(True)
                # time.sleep(1)
                # buzzer(False)
                # global current_time
                # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                # print("Card registered! ID: " + card_uid + " Time: " + current_time)
                # run_sender()
                # print("karta zarejestrowana")
                # break

        


if __name__ == '__main__':
    print("\nProgram started")

    while 1:
        run()
        time.sleep(5)
    print("\nProgram finished")
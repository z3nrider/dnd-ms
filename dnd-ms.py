#!/usr/bin/env python
# consumer
import pika
import json
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f"Message received: {json.loads(body)}.")
        req = json.loads(body)

        if req["queryType"] == "nameSuggestion":
            print('your query type is', req["queryType"])
            print('Here is your character:')
            prompt = {
                "prompt": f"Suggest me a name for a {req['race']} {req['playerClass']}."}
            print(prompt["prompt"])
        elif req["queryType"] == "background":
            print('your query type is background')

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# print("Name: ", req['name'], "Race: ", req['race'],
#                   "Class: ", req['playerClass'], "Homeland: ",
#                   req['homeland'], "Family: ", req['family'],
#                   "Adventure Reason: ", req['adventureReason'],
#                   "Flaw : ", req['flaw'])
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

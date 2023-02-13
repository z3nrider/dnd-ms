#!/usr/bin/env python
# producer
import time
import pika
import json
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='request')

    def callback(ch, method, properties, body):
        print(f"Message received: {json.loads(body)}.")
        req = json.loads(body)
        channel.close()

    # def send(ch, method, properties, body):
    #     messageBody = json.dumps({"queryType": "nameSuggestion"})
    #     print(f"Message sent: {messageBody}")

    #     channel.close()

    print("Making query type: nameSuggestion...")
    time.sleep(2)
    messageBody = json.dumps({
        "queryType": "nameSuggestion",
        "race": "Human",
        "playerClass": "Rogue"
    })
    channel.basic_publish(exchange='', routing_key='hello',
                          body=messageBody)
    print("Message sent: ", messageBody)

    # print("Generating DND Character...")
    # time.sleep(2)
    # messageBody = json.dumps({
    #     "queryType": "background",
    #     "name": "Steve",
    #     "race": "Human",
    #     "playerClass": "Rogue",
    #     "homeland": "Faerun",
    #     "family": "Caitlin and Kenzie",
    #     "adventureReason": "get gold",
    #     "flaw": "greedy"
    # })

    channel.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

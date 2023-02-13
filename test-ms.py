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

    channel.queue_declare(queue='hello')

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
    messageBody = json.dumps({"queryType": "nameSuggestion"})
    channel.basic_publish(exchange='', routing_key='hello',
                          body=messageBody)
    print("Message sent: ", messageBody)

    print("Making query type: background...")
    time.sleep(2)
    messageBody = json.dumps({"queryType": "background"})
    channel.basic_publish(exchange='', routing_key='hello',
                          body=messageBody)
    print("Message sent: ", messageBody)
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

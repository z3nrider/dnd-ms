#!/usr/bin/env python
import pika
import json
import sys
import os


# Connect to RMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='request')

# A function that receives message body from dnd-ms.py
# used to be called "callback"


def receive(ch, method, properties, body):
    print('You just called the receive method.')
    print(f"Message received: {json.loads(body)}.")
    req = json.loads(body)
    # channel.close()

# A function that sends the JSON to dnd-ms.py


def send(ch, method, properties, body):
    print('You just called the send method.')
    channel.basic_publish(exchange='', routing_key='request', body=body)
    # channel.close()


channel.basic_consume(
    queue='request', on_message_callback=receive, auto_ack=True)

if __name__ == '__main__':
    try:
        # Test 1: Sending a nameSuggestion query to dnd-ms.py
        print("Making query type: nameSuggestion...")
        messageBody = json.dumps({
            "queryType": "nameSuggestion",
            "race": "Human",
            "playerClass": "Rogue"
        })
        send(messageBody)
        print("Message sent: ", messageBody)

        # # Consume the response prompt from dnd-ms.py
        # channel.basic_consume(
        #     queue='request', on_message_callback=receive, auto_ack=True)

        # # Test 2: Sends a background query
        # print("Making query type: background...")
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

        # channel.basic_publish(
        #     exchange='', routing_key='request', body=messageBody)
        # print("Message sent: ", messageBody)

        # # Test 3: Making an invalid query type request
        # print("Making query type: fake query type")
        # messageBody = json.dumps({"queryType": "fakeRequest"})
        # channel.basic_publish(
        #     exchange='', routing_key='request', body=messageBody)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

import pika
import json
import sys
import os


# Connect to RMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='request')


def consume():
    '''
    A function that listens for messages from RabbitMQ.
    '''
    channel.basic_consume(
        queue='response', on_message_callback=receive, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def receive(ch, method, properties, body):
    '''
    A function that receives messages from dnd-ms.py
    '''
    print(f"Message received: {json.loads(body)}.")


def send(body):
    '''
    A function that sends the JSON to dnd-ms.py
    '''
    channel.basic_publish(exchange='', routing_key='request', body=body)
    consume()


if __name__ == '__main__':
    # try each test individually by commenting out all
    # other test
    try:
        # Test 1: Sending a nameSuggestion query to dnd-ms.py
        print("Making query type: nameSuggestion...")
        messageBody = json.dumps({
            "queryType": "nameSuggestion",
            "gender": "male",
            "race": "Human",
            "playerClass": "Rogue"
        })
        send(messageBody)

        # Test 2: Sends a background query
        print("Making query type: background...")
        messageBody = json.dumps({
            "queryType": "background",
            "name": "Steve",
            "race": "Human",
            "playerClass": "Rogue",
            "homeland": "Faerun",
            "family": "Caitlin and Kenzie",
            "adventureReason": "get gold",
            "flaw": "greedy",
            "fake": "this is fake"
        })
        send(messageBody)

        # Test 3: Making an invalid query type request
        print("Making query type: fake query type")
        messageBody = json.dumps(
            {"queryType": "fakeQuery", "name": "billy"})
        send(messageBody)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

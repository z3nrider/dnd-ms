import pika
import json
import sys
import os


print('===========================================')
print('    Welcome to the DND Prompt Generator')
print('===========================================\n')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


def consume():
    '''
    A function that listens for messages from RabbitMQ.
    '''
    # declare queue channels request and response
    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')
    channel.basic_consume(
        queue='request', on_message_callback=receive, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def receive(ch, method, properties, body):
    req = json.loads(body)

    if req["queryType"] == "nameSuggestion":
        prompt = json.dumps({
            "prompt": f"Suggest me a name for a {req['race']} {req['playerClass']}."})
        print("Message sent.\nYour prompt is ", prompt[11:-1])
        send(prompt)
        print(' [*] Waiting for messages. To exit press CTRL+C')

    elif req["queryType"] == "background":
        prompt = json.dumps({
            "prompt":
            f"Suggest me a background story for {req['name']}, a {req['race']} {req['playerClass']}. They are from {req['homeland']}. Their family is {req['family']}. Their reason for adventuring is to {req['adventureReason']}. Their flaw is that they are {req['flaw']}."
        })
        print("Message sent.\nYour prompt is ", prompt[11:-1])
        send(prompt)
        print(' [*] Waiting for messages. To exit press CTRL+C')

    else:
        prompt = json.dumps({"error": "invalid queryType"})
        send(prompt)
        print(' [*] Waiting for messages. To exit press CTRL+C')


def send(prompt):
    body = json.dumps(prompt)
    channel.basic_publish(
        exchange='', routing_key='response', body=body)


if __name__ == '__main__':
    try:
        consume()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

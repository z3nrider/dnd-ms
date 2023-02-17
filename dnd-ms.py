#!/usr/bin/env python
import pika
import json
import sys
import os


def main():
    print('===========================================')
    print('    Welcome to the DND Prompt Generator')
    print('===========================================\n')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def receive(ch, method, properties, body):
        # declare queue channels
        channel.queue_declare(queue='request')
        channel.queue_declare(queue='response')
        channel.basic_consume(
            queue='request', on_message_callback=receive, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

        print('You just called the receive method.')
        req = json.loads(body)

        if req["queryType"] == "nameSuggestion":
            prompt = {
                "prompt": f"Suggest me a name for a {req['race']} {req['playerClass']}."}
            print('Your query type is nameSuggestion.')
            print('Here is your character prompt:', prompt)

            prompt = json.dumps(prompt)

            send(prompt)

        elif req["queryType"] == "background":
            prompt = {
                "prompt":
                f"Suggest me a background story for {req['name']}, a {req['race']} {req['playerClass']}. They are from {req['homeland']}. Their family is {req['family']}. Their reason for adventuring is to {req['adventureReason']}. Their flaw is that they are {req['flaw']}."
            }
            print('Your query type is background.')
            print('Here is your background prompt:', prompt)

        else:
            print(
                f'I did not understand your query type {req["queryType"]}. Please choose from nameSuggestion or background in your request and, try again.')

    # TODO: not quite working yet
    def send(ch, method, properties, prompt):
        print('You just called the send method.')
        body = json.dumps(prompt)
        channel.basic_publish(
            exchange='', routing_key='response', body=body)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

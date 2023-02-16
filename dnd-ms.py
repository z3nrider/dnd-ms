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

    channel.queue_declare(queue='request')

    def callback(ch, method, properties, body):
        req = json.loads(body)
        print('===========')
        print(req)
        print(req['queryType'])
        if req["queryType"] == "nameSuggestion":
            print('\nYour query type is', req["queryType"], '\n')
            print('Here is your character prompt:\n')
            prompt = {
                "prompt": f"Suggest me a name for a {req['race']} {req['playerClass']}."}
            print(prompt["prompt"])  # need to send back this
            prompt = json.dumps(prompt)

            channel.basic_publish(exchange='', routing_key='request',
                                  body=prompt)

        elif req["queryType"] == "background":
            print('\nYour query type is', req["queryType"], '.\n')
            prompt = {
                "prompt":
                f"Suggest me a background story for {req['name']}, a {req['race']} {req['playerClass']}. \nThey are from {req['homeland']}. \nTheir family is {req['family']}. \nTheir reason for adventuring is to {req['adventureReason']}. \nTheir flaw is that they are {req['flaw']}."
            }
            print(prompt["prompt"])

        else:
            print(
                f'\nI did not understand your query type {req["queryType"]}.\nPlease choose from nameSuggestion or background\nin your request and, try again.\n')
            print(' [*] Waiting for messages. To exit press CTRL+C\n')

    channel.basic_consume(
        queue='request', on_message_callback=callback, auto_ack=True)

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

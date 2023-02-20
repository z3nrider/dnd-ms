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

    if len(req) < 2:
        prompt = json.dumps({"error": "at least one suggestion is required"})
        send(prompt)

    # sends back a DND character prompt to be passed to ChatGPT for a name suggestion
    if req["queryType"] == "nameSuggestion":
        prompt_str = "Suggest me a name for a(n) "
        if req.get("race") is not None:
            prompt_str += req["race"]
            prompt_str += " "
        if req.get("gender") is not None:
            prompt_str += req["gender"]
            prompt_str += " "
        if req.get("playerClass") is not None:
            prompt_str += req["playerClass"]

        prompt = json.dumps(prompt_str)
        print("Message sent: ", prompt)
        send(prompt)
        print(' [*] Waiting for messages. To exit press CTRL+C')

    # sends back a DND background prompt to be passed to ChatGPT for a name suggestion
    elif req["queryType"] == "background":
        # name is required
        if req.get("name") is None:
            prompt = json.dumps({"error": "name is required"})
            print("Please try again. Name is required.")
            send(prompt)
            print(' [*] Waiting for messages. To exit press CTRL+C')

        # if the only querys are query type and name
        if len(req) == 2:
            prompt_str = f"Suggest me a background story for {req['name']}."
            prompt = json.dumps({"background": prompt_str})
            print("Message sent: ", prompt)
            send(prompt)
            print(' [*] Waiting for messages. To exit press CTRL+C')

        # dynamically builds a prompt from optional values
        else:
            prompt_str = f"Suggest me a background story for {req['name']}, a(n) "
            if req.get("race") is not None:
                prompt_str += req["race"]
                prompt_str += " "
            if req.get("gender") is not None:
                prompt_str += req["gender"]
                prompt_str += " "
            if req.get("playerClass") is not None:
                prompt_str += req["playerClass"]

            prompt_str += "."

            if req.get("homeland") is not None:
                prompt_str += " They are from "
                prompt_str += req["homeland"]
                prompt_str += "."
            if req.get("family") is not None:
                prompt_str += " Their family is "
                prompt_str += req["family"]
                prompt_str += "."
            if req.get("adventureReason") is not None:
                prompt_str += " Their reason for adventuring is to "
                prompt_str += req["adventureReason"]
                prompt_str += "."
            if req.get("flaw") is not None:
                prompt_str += " Their flaw is that they are "
                prompt_str += req["flaw"]
                prompt_str += "."

            prompt = json.dumps({"background": prompt_str})
            print("Message sent.\nYour prompt is", prompt)
            send(prompt)
            print(' [*] Waiting for messages. To exit press CTRL+C')

    else:
        prompt = json.dumps({"error": "invalid queryType"})
        print("Message sent: ", prompt)
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

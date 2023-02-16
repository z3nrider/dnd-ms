CS 361 Course Project
Microservice Communication Contract
UML Diagram source: course textbook, page 56 (created through draw.io)

Installation
1. Download and install RabbitMQ here: https://www.rabbitmq.com/download.html
2. Clone this repo and install pika here: https://pypi.org/project/pika/
3. Start the RabbitMQ server
4. Run dnd-ms.py
5. Run test-ms.py (your project goes here, where you will connect to RMQ)

How To Request Data
1. Messages are sent through the 'request' queue, which must be running prior to execution
2. Messages are sent as JSON objects as one of two query types. For example,
    { "queryType" : "nameSuggestion" },
    { "queryType" : "background" }
3. If you want a DND name suggestion (a prompt that may be passed to ChatGPT (optional)), dnd-ms.py
    will respond with a JSON object with a prompt. 
4. If you want a DND background suggestion, dnd-ms.py will respond similarly.

How To Receive Data
1. Messages will be received as JSON objects, in addition to confirmation messages in the terminal
    { "prompt" : "Suggest me a name for a human male warrior." }, is sent back on the response queue.

<img width="870" alt="Screenshot 2023-02-13 at 1 34 55 PM" src="https://user-images.githubusercontent.com/60510555/218545178-7a260903-7b1a-4629-83ac-28612dcc238f.png">

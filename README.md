CS 361 Course Project
Microservice Communication Contract

Add a README to your GitHub (or update it if you already have one) that contains your communication contract. (Once you define it, don't change it! Your partner is relying on you.) README must contain...

    Clear instructions for how to REQUEST data from the microservice you implemented. Include an example call.
    Clear instructions for how to RECEIVE data from the microservice you implemented
    UML sequence diagram showing how requesting and receiving data work. Make it detailed enough that your partner (and your grader) will understand

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

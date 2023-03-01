import pika
from fastapi import FastAPI

app = FastAPI()

@app.post("/fibonacci")
async def fibonacci(n: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="fibonacci")

    message = str(n)
    channel.basic_publish(exchange="", routing_key="fibonacci", body=message)

    connection.close()

    return {"message": f"Published {message} to RabbitMQ"}

@app.get("/results/{id}")
async def results(id: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    result_queue = f"result-{id}"
    channel.queue_declare(queue=result_queue)

    method, properties, body = channel.basic_get(queue=result_queue, auto_ack=True)

    if not method:
        return {"message": "Result not ready"}

    result = body.decode()

    connection.close()

    return {"result": result}

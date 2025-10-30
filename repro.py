import logging
import threading
from time import sleep
from pika import ConnectionParameters, BlockingConnection, PlainCredentials

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Publisher(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_running = True
        self._name = "Publisher"
        self._queue = "pika-1543"
        plain_credentials = PlainCredentials("guest", "guest")
        self._parameters = ConnectionParameters(
            "localhost", credentials=plain_credentials
        )
        self._open_connection_and_channel()

    def run(self):
        while self._is_running:
            self._connection.process_data_events(time_limit=1)

    def _publish(self, message):
        self._channel.basic_publish(
            "", self._queue, body=message.encode(), mandatory=True
        )

    def publish(self, message):
        if self._is_running == False:
            return
        self._connection.add_callback_threadsafe(lambda: self._publish(message))

    def stop(self):
        self._is_running = False
        self._connection.process_data_events(time_limit=5)
        if self._connection.is_open:
            self._connection.close()

    def _open_connection_and_channel(self):
        self._connection = BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, auto_delete=False, durable=True)
        self._channel.confirm_delivery()


if __name__ == "__main__":
    publisher = Publisher()
    publisher.start()
    try:
        for i in range(9999):
            msg = f"Message {i}"
            logger.info(f"Publishing: {msg!r}")
            publisher.publish(msg)
            sleep(5)
    except KeyboardInterrupt:
        logger.info("Stopping...")
        publisher.stop()
    finally:
        publisher.join()
        logger.info("Stopped")

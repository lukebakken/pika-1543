# [Discussion](https://github.com/pika/pika/discussions/1543)

## Start RabbitMQ

```
docker run --pull always --rm --name rabbitmq --publish 5672:5672 --publish 15672:15672 rabbitmq:management
```

## Repro steps


### Clone and run publisher

```
git clone https://github.com/lukebakken/pika-1543.git
cd pika-1543
pipenv install
pipenv run python ./repro.py
```

Observe messages being published.

### Stop RabbitMQ

```
docker stop rabbitmq
```

### Observed behavior

Connection is closed, as expected. No `UnroutableError` seen.

```
INFO:__main__:Publishing: 'Message 0'
INFO:__main__:Publishing: 'Message 1'
INFO:pika.adapters.utils.io_services_utils:Aborting transport connection: state=1; <socket.socket fd=6, family=2, type=1, proto=6, laddr=('127.0.0.1', 37698), raddr=('127.0.0.1', 5672)>
INFO:pika.adapters.utils.io_services_utils:_AsyncTransportBase._initate_abort(): Initiating abrupt asynchronous transport shutdown: state=1; error=None; <socket.socket fd=6, family=2, type=1, proto=6, laddr=('127.0.0.1', 37698), raddr=('127.0.0.1', 5672)>
INFO:pika.adapters.utils.io_services_utils:Deactivating transport: state=1; <socket.socket fd=6, family=2, type=1, proto=6, laddr=('127.0.0.1', 37698), raddr=('127.0.0.1', 5672)>
INFO:pika.connection:AMQP stack terminated, failed to connect, or aborted: opened=True, error-arg=None; pending-error=ConnectionClosedByBroker: (320) "CONNECTION_FORCED - broker forced connection closure with reason 'shutdown'"
INFO:pika.connection:Stack terminated due to ConnectionClosedByBroker: (320) "CONNECTION_FORCED - broker forced connection closure with reason 'shutdown'"
INFO:pika.adapters.utils.io_services_utils:Closing transport socket and unlinking: state=3; <socket.socket fd=6, family=2, type=1, proto=6, laddr=('127.0.0.1', 37698), raddr=('127.0.0.1', 5672)>
ERROR:pika.adapters.blocking_connection:Unexpected connection close detected: ConnectionClosedByBroker: (320) "CONNECTION_FORCED - broker forced connection closure with reason 'shutdown'"
Exception in thread Publisher:
Traceback (most recent call last):
  File "/home/lrbakken/.asdf/installs/python/3.14.0t/lib/python3.14t/threading.py", line 1081, in _bootstrap_inner
    self._context.run(self.run)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/home/lrbakken/development/lukebakken/pika-1543/./repro.py", line 23, in run
    self._connection.process_data_events(time_limit=1)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/home/lrbakken/.local/share/virtualenvs/pika-1543-YKJmqBUd/lib/python3.14t/site-packages/pika/adapters/blocking_connection.py", line 845, in process_data_events
    self._flush_output(timer.is_ready, common_terminator)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lrbakken/.local/share/virtualenvs/pika-1543-YKJmqBUd/lib/python3.14t/site-packages/pika/adapters/blocking_connection.py", line 523, in _flush_output
    raise self._closed_result.value.error
pika.exceptions.ConnectionClosedByBroker: (320, "CONNECTION_FORCED - broker forced connection closure with reason 'shutdown'")
INFO:__main__:Publishing: 'Message 2'
INFO:__main__:Stopped
Traceback (most recent call last):
  File "/home/lrbakken/development/lukebakken/pika-1543/./repro.py", line 53, in <module>
    publisher.publish(msg)
    ~~~~~~~~~~~~~~~~~^^^^^
  File "/home/lrbakken/development/lukebakken/pika-1543/./repro.py", line 31, in publish
    self._connection.add_callback_threadsafe(lambda: self._publish(message))
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lrbakken/.local/share/virtualenvs/pika-1543-YKJmqBUd/lib/python3.14t/site-packages/pika/adapters/blocking_connection.py", line 742, in add_callback_threadsafe
    raise exceptions.ConnectionWrongStateError(
        'BlockingConnection.add_callback_threadsafe() called on '
        'closed or closing connection.')
pika.exceptions.ConnectionWrongStateError: BlockingConnection.add_callback_threadsafe() called on closed or closing connection.
```

streamcat
=========

Examples
--------

Encoding a JSON iterator into a stream:

.. code-block:: python

    def gen_records():
        yield b'{"foo": "bar"}'
        yield b'{"baz": [1, 2, 3]}'

    stream = streamcat.iterator_to_stream(gen_records())

    # `stream` can then be used just like any other `io.RawIOBase`
    with open('/tmp/jsoncat', 'wb') as destination:
        shutil.copyfileobj(stream, destination)

Decoding a stream into a generator:

.. code-block:: python

    decoder = json.JSONDecoder()
    with open('/tmp/jsoncat', 'rb') as source:
        records = streamcat.stream_to_iterator(source, decoder)
        for record in records:
            print(record)

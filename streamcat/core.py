DEFAULT_CHUNK_SIZE = 1024 * 1024


class Stream:
    def __init__(self, iterator):
        self.iterator = iterator
        self.data = b''

    def read(self, size=-1):
        chunks = []
        data_length = len(self.data)
        try:
            while data_length < size or size == -1:
                chunk = next(self.iterator)
                chunks.append(chunk)
                data_length += len(chunk)
        except StopIteration:
            pass
        self.data += b''.join(chunks)
        if size == -1:
            (result, self.data) = (self.data, b'')
        else:
            (result, self.data) = (self.data[:size], self.data[size:])
        return result


def iterator_to_stream(iterator):
    return Stream(iterator)


def stream_to_iterator(file, decoder, chunk_size=DEFAULT_CHUNK_SIZE):
    data = ''
    while True:
        chunk = file.read(chunk_size).decode()
        data += chunk
        if not data:
            break
        try:
            while True:
                data = data.lstrip()
                (element, position) = decoder.raw_decode(data)
                data = data[position:]
                yield element
        except ValueError:
            if not chunk:
                raise

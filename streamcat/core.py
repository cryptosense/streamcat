import io

DEFAULT_CHUNK_SIZE = 1024 * 1024


class Stream(io.RawIOBase):
    def __init__(self, iterator):
        self.iterator = iterator
        self.data = b''

    def readable(self):
        return True

    def seekable(self):
        return False

    def writable(self):
        return False

    def read(self, size=-1):
        if size == -1:
            return self.readall()
        chunks = []
        data_length = len(self.data)
        if data_length < size:
            try:
                chunk = next(self.iterator)
                chunks.append(chunk)
                data_length += len(chunk)
            except StopIteration:
                pass
        self.data += b''.join(chunks)
        (result, self.data) = (self.data[:size], self.data[size:])
        return result

    def readinto(self, b):
        data = self.read(len(b))
        data_length = len(data)
        b[0:data_length] = data
        return data_length

    def readall(self):
        return b''.join(self.iterator)


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

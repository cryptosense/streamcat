import io
import json

import pytest

import streamcat


class TestStream:
    def test_attributes(self):
        stream = streamcat.core.Stream(iter(()))
        assert stream.readable()
        assert not stream.seekable()
        assert not stream.writable()

    def test_empty(self):
        stream = streamcat.core.Stream(iter(()))
        assert stream.read() == b''
        assert stream.read(1) == b''

    def test_read_size(self):
        stream = streamcat.core.Stream(str(i).encode() for i in range(4))
        assert stream.read(0) == b''
        assert stream.read(1) == b'0'
        assert stream.read(2) == b'1'
        assert stream.read(3) == b'2'
        assert stream.read(4) == b'3'
        assert stream.read(5) == b''

    def test_read(self):
        stream = streamcat.core.Stream(iter(()))
        assert stream.read() == b''

    def test_readall(self):
        stream = streamcat.core.Stream(str(i).encode() for i in range(4))
        assert stream.readall() == b'0123'
        assert stream.readall() == b''


class TestBufferedStream:
    def test_empty(self):
        raw = streamcat.core.Stream(iter(()))
        stream = io.BufferedReader(raw)
        assert stream.read() == b''
        assert stream.read(1) == b''

    def test_read_size(self):
        raw = streamcat.core.Stream(str(i).encode() for i in range(4))
        stream = io.BufferedReader(raw)
        assert stream.read(0) == b''
        assert stream.read(1) == b'0'
        assert stream.read(2) == b'12'
        assert stream.read(3) == b'3'
        assert stream.read(4) == b''

    def test_read(self):
        raw = streamcat.core.Stream(str(i).encode() for i in range(4))
        stream = io.BufferedReader(raw)
        assert stream.read() == b'0123'
        assert stream.read() == b''


class TestIteratorToStream:
    def test(self):
        streamcat.iterator_to_stream(iter(()))


class TestStreamToIterator:
    def check_decode(self, input, expected, chunk_size):
        decoder = json.JSONDecoder()
        gen = streamcat.stream_to_iterator(io.BytesIO(input.encode()), decoder, chunk_size)
        assert list(gen) == expected

    @pytest.mark.parametrize('chunk_size', (1, 2, 1024))
    def test_ok(self, chunk_size):
        self.check_decode('', [], chunk_size)
        self.check_decode('{}', [{}], chunk_size)
        self.check_decode('{}[]', [{}, []], chunk_size)
        self.check_decode('{}\n[]', [{}, []], chunk_size)
        self.check_decode('\n{}\n\n[]\n\n', [{}, []], chunk_size)

    @pytest.mark.parametrize('chunk_size', (1, 2, 1024))
    def test_error(self, chunk_size):
        with pytest.raises(ValueError):
            self.check_decode('{', [], chunk_size)
        with pytest.raises(ValueError):
            self.check_decode('}', [], chunk_size)

import io
import json

import pytest

import streamcat


class TestStream:
    def test_empty(self):
        stream = streamcat.core.Stream(iter(()))
        assert stream.read() == b''
        assert stream.read(1) == b''

    def test_read_size(self):
        stream = streamcat.core.Stream(str(i).encode() for i in range(4))
        assert stream.read(0) == b''
        assert stream.read(1) == b'0'
        assert stream.read(2) == b'12'
        assert stream.read(3) == b'3'
        assert stream.read(4) == b''

    def test_read(self):
        stream = streamcat.core.Stream(str(i).encode() for i in range(4))
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

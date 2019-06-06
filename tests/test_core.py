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


class TestStreamRead:
    def test_empty(self):
        stream = streamcat.core.Stream(iter([]))

        result = stream.read()

        assert result == b""

    def test_size_exact(self):
        iterator = iter([b"0", b"1"])
        stream = streamcat.core.Stream(iterator)

        result = stream.read(1)

        assert result == b"0"
        assert list(iterator) == [b"1"]

    def test_size_more(self):
        iterator = iter([b"0", b"1"])
        stream = streamcat.core.Stream(iterator)

        result = stream.read(2)

        assert result == b"0"
        assert list(iterator) == [b"1"]

    def test_size_more_with_buffered_reader(self):
        iterator = iter([b"0", b"1"])
        stream = io.BufferedReader(streamcat.core.Stream(iterator))

        result = stream.read(2)

        assert result == b"01"
        assert list(iterator) == []

    def test_size_partial_enough(self):
        iterator = iter([b"01", b"2"])
        stream = streamcat.core.Stream(iterator)

        result_0 = stream.read(1)
        result_1 = stream.read(1)

        assert result_0 == b"0"
        assert result_1 == b"1"
        assert list(iterator) == [b"2"]

    def test_size_partial(self):
        iterator = iter([b"01", b"2"])
        stream = streamcat.core.Stream(iterator)

        result_0 = stream.read(1)
        result_1 = stream.read(2)

        assert result_0 == b"0"
        assert result_1 == b"12"
        assert list(iterator) == []

    def test_size_default(self):
        iterator = iter([b"0", b"1"])
        stream = streamcat.core.Stream(iterator)

        result = stream.read()

        assert result == b"01"
        assert list(iterator) == []


class TestStreamReadall:
    def test(self):
        iterator = iter([b"0", b"1"])
        stream = streamcat.core.Stream(iterator)

        result = stream.readall()

        assert result == b"01"
        assert list(iterator) == []


class TestIteratorToStream:
    def test(self):
        streamcat.iterator_to_stream(iter(()))


class TestStreamToIterator:
    @pytest.mark.parametrize("chunk_size", (1, 2, 1024))
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("", []),
            ("{}", [{}]),
            ("{}[]", [{}, []]),
            ("{}\n[]", [{}, []]),
            ("\n{}\n\n[]\n\n", [{}, []]),
        ],
    )
    def test_ok(self, chunk_size, test_input, expected):
        decoder = json.JSONDecoder()

        result = streamcat.stream_to_iterator(
            io.BytesIO(test_input.encode()), decoder, chunk_size
        )

        assert list(result) == expected

    @pytest.mark.parametrize("chunk_size", (1, 2, 1024))
    @pytest.mark.parametrize("test_input", ("{", "}"))
    def test_error(self, chunk_size, test_input):
        decoder = json.JSONDecoder()

        result = streamcat.stream_to_iterator(
            io.BytesIO(test_input.encode()), decoder, chunk_size
        )

        with pytest.raises(ValueError):
            list(result)

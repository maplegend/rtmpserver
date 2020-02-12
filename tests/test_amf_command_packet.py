import struct

from bytes_packet import BytesPacket
from rtmp_packet import AMFCommandPacket
from utils import print_hex


def test_int_parse():
    data = struct.pack('!bq', 0, 100)
    pack = AMFCommandPacket(BytesPacket(data))
    assert pack.fields[0] == 100


def test_bool_parse():
    data = struct.pack('!bb', 1, 1)
    pack = AMFCommandPacket(BytesPacket(data))
    assert pack.fields[0] == True


def test_string_parse():
    data = struct.pack('!bh11s', 2, 11, 'Hello world'.encode('UTF-8'))
    pack = AMFCommandPacket(BytesPacket(data))
    assert pack.fields[0] == "Hello world"


def test_object_end():
    data = struct.pack('!bbb', 0, 0, 9)
    assert AMFCommandPacket.is_object_end(BytesPacket(data))


def test_object_parse():
    data = struct.pack('!bh4sbh4sbbb', 3, 4, 'test'.encode('UTF-8'), 2, 4, 'test'.encode('UTF-8'), 0, 0, 9)
    pack = AMFCommandPacket(BytesPacket(data))
    assert "test" in pack.fields[0] and pack.fields[0]["test"] == "test"
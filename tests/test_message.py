import unittest
from context import message


class TestKeepAlive(unittest.TestCase):
    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x00')
        self.assertTrue(isinstance(msg, message.KeepAlive))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x00')
        self.assertEqual(msg.length, 0)


class TestChoke(unittest.TestCase):
    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x00')
        self.assertTrue(isinstance(msg, message.Choke))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x00')
        self.assertEqual(msg.length, 1)

    def test_get_message_from_bytes__id(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x00')
        self.assertEqual(msg.id, 0)


class TestUnChoke(unittest.TestCase):
    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x01')
        self.assertTrue(isinstance(msg, message.UnChoke))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x01')
        self.assertEqual(msg.length, 1)

    def test_get_message_from_bytes__id(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x01')
        self.assertEqual(msg.id, 1)


class TestInterested(unittest.TestCase):
    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x02')
        self.assertTrue(isinstance(msg, message.Interested))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x02')
        self.assertEqual(msg.length, 1)

    def test_get_message_from_bytes__id(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x02')
        self.assertEqual(msg.id, 2)


class TestNotInterested(unittest.TestCase):
    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x03')
        self.assertTrue(isinstance(msg, message.NotInterested))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x03')
        self.assertEqual(msg.length, 1)

    def test_get_message_from_bytes__id(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x01\x03')
        self.assertEqual(msg.id, 3)


class TestHave(unittest.TestCase):
    def test_get_message_from_bytes__length(self):
        byte_str = b'\x00\x00\x00\x05\x04\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.length, 5)

    def test_get_message_from_bytes__id(self):
        byte_str = b'\x00\x00\x00\x05\x04\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.id, 4)

    def test_get_message_from_bytes__index_zero(self):
        byte_str = b'\x00\x00\x00\x05\x04\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 0)

    def test_get_message_from_bytes__index_max(self):
        ''' Test the hex value 0xFFFFFFFF '''
        byte_str = b'\x00\x00\x00\x05\x04\xFF\xFF\xFF\xFF'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 4294967295)

    def test_get_message_from_bytes__index_bottom(self):
        ''' Test bottom 2 bytes of index '''
        byte_str = b'\x00\x00\x00\x05\x04\x00\x00\xFF\xFF'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 65535)

    def test_get_message_from_bytes__index_upper(self):
        ''' Test upper 2 bytes of index '''
        byte_str = b'\x00\x00\x00\x05\x04\xFF\xFF\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 4294901760)


class TestBitField(unittest.TestCase):
    def test_get_message_from_bytes(self):
        byte_str = b'\x00\x00\x00\x05\x05\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertTrue(isinstance(msg, message.BitField))

    def test_get_message_from_bytes__length(self):
        byte_str = b'\x00\x00\x00\x05\x05\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.length, 5)

    def test_get_message_from_bytes__id(self):
        byte_str = b'\x00\x00\x00\x05\x05\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.id, 5)

    def test_get_message_from_bytes__bitfield_0(self):
        byte_str = b'\x00\x00\x00\x01\x05'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.bitfield, b'')

    def test_get_message_from_bytes__bitfield_1_byte(self):
        byte_str = b'\x00\x00\x00\x02\x05\x01'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.bitfield, b'\x01')

    def test_get_message_from_bytes_bitfield_256_bytes(self):
        byte_str = b'\x00\x00\x01\x01\x05' + (b'\xff' * 256)
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.bitfield, (b'\xff' * 256))


class TestRequest(unittest.TestCase):
    def test_get_message_from_bytes(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertTrue(isinstance(msg, message.Request))

    def test_get_message_from_bytes__length(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.length, 13)

    def test_get_message_from_bytes__id(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.id, 6)

    def test_get_message_from_bytes__index(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 0)

    def test_get_message_from_bytes__max_index(self):
        byte_str = b'\x00\x00\x00\x13\x06\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 4294967295)

    def test_get_message_from_bytes__begin(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.begin, 0)

    def test_get_message_from_bytes__max_begin(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.begin, 4294967295)

    def test_get_message_from_bytes__request_length(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.request_length, 0)

    def test_get_message_from_bytes__max_request_length(self):
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\xFF'
        byte_str += b'\xFF\xFF\xFF'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.request_length, 4294967295)


class TestCancel(unittest.TestCase):
    def test_get_message_from_bytes(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertTrue(isinstance(msg, message.Cancel))

    def test_get_message_from_bytes__length(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.length, 13)

    def test_get_message_from_bytes__id(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.id, 8)

    def test_get_message_from_bytes__index(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 0)

    def test_get_message_from_bytes__max_index(self):
        byte_str = b'\x00\x00\x00\x13\x08\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.index, 4294967295)

    def test_get_message_from_bytes__begin(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.begin, 0)

    def test_get_message_from_bytes__max_begin(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.begin, 4294967295)

    def test_get_message_from_bytes__request_length(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.request_length, 0)

    def test_get_message_from_bytes__max_request_length(self):
        byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\xFF'
        byte_str += b'\xFF\xFF\xFF'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertEqual(msg.request_length, 4294967295)


if __name__ == '__main__':
    unittest.main()

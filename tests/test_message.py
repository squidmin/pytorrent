import unittest
from context import message


class TestKeepAlive(unittest.TestCase):
    def test_get_message(self):
        msg = message.Message.get_message('keep-alive')
        self.assertTrue(isinstance(msg, message.KeepAlive))

    def test_get_message__length(self):
        msg = message.Message.get_message('keep-alive')
        self.assertEqual(msg.length, 0)

    def test_get_message__to_bytes(self):
        msg = message.Message.get_message('keep-alive')
        self.assertEqual(msg.to_bytes(), b'\x00\x00\x00\x00')

    def test_get_message_from_bytes(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x00')
        self.assertTrue(isinstance(msg, message.KeepAlive))

    def test_get_message_from_bytes__length(self):
        msg = message.Message.get_message_from_bytes(b'\x00\x00\x00\x00')
        self.assertEqual(msg.length, 0)


class TestChoke(unittest.TestCase):
    def test_get_message(self):
        msg = message.Message.get_message('choke')
        self.assertTrue(isinstance(msg, message.Choke))

    def test_get_message__to_bytes(self):
        msg = message.Message.get_message('choke')
        self.assertEqual(msg.to_bytes(), b'\x00\x00\x00\x01\x00')

    def test_get_message__length(self):
        msg = message.Message.get_message('choke')
        self.assertEqual(msg.length, 1)

    def test_get_message__id(self):
        msg = message.Message.get_message('choke')
        self.assertEqual(msg.id, 0)

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
    def test_get_message(self):
        msg = message.Message.get_message('unchoke')
        self.assertEqual(isinstance(msg, message.UnChoke), True)

    def test_get_message__to_bytes(self):
        msg_b = message.Message.get_message('unchoke').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x01')

    def test_get_message__length(self):
        msg = message.Message.get_message('unchoke')
        self.assertEqual(msg.length, 1)

    def test_get_message__id(self):
        msg = message.Message.get_message('unchoke')
        self.assertEqual(msg.id, 1)

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
    def test_get_message(self):
        msg = message.Message.get_message('interested')
        self.assertTrue(isinstance(msg, message.Interested))

    def test_get_message__to_bytes(self):
        msg_b = message.Message.get_message('interested').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x02')

    def test_get_message__length(self):
        msg = message.Message.get_message('interested')
        self.assertEqual(msg.length, 1)

    def test_get_message__id(self):
        msg = message.Message.get_message('interested')
        self.assertEqual(msg.id, 2)

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
    def test_get_message(self):
        msg = message.Message.get_message('not interested')
        self.assertTrue(isinstance(msg, message.NotInterested))

    def test_get_message__to_bytes(self):
        msg_b = message.Message.get_message('not interested').to_bytes()
        self.assertEqual(msg_b, b'\x00\x00\x00\x01\x03')

    def test_get_message__length(self):
        msg = message.Message.get_message('not interested')
        self.assertEqual(msg.length, 1)

    def test_get_message__id(self):
        msg = message.Message.get_message('not interested')
        self.assertEqual(msg.id, 3)

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
    def test_get_message(self):
        msg = message.Message.get_message('have', 0)
        self.assertTrue(isinstance(msg, message.Have))

    def test_get_message__to_bytes(self):
        msg = message.Message.get_message('have', 0).to_bytes()
        self.assertEqual(msg, b'\x00\x00\x00\x05\x04\x00\x00\x00\x00')

    def test_get_message__to_bytes__all_maxed(self):
        msg = message.Message.get_message('have', 4294967295)
        byte_str = b'\x00\x00\x00\x05\x04\xFF\xFF\xFF\xFF'
        self.assertTrue(msg.to_bytes, byte_str)

    def test_get_message__length(self):
        msg = message.Message.get_message('have', 0)
        self.assertEqual(msg.length, 5)

    def test_get_message__id(self):
        msg = message.Message.get_message('have', 0)
        self.assertEqual(msg.id, 4)

    def test_get_message__index_zero(self):
        msg = message.Message.get_message('have', 0)
        self.assertEqual(msg.index, 0)

    def test_get_message__index_max(self):
        ''' Test the hex value 0xFFFFFFFF '''
        msg = message.Message.get_message('have', 4294967295)
        self.assertEqual(msg.index, 4294967295)

    def test_get_message__index_bottom(self):
        ''' Test bottom 2 bytes of index '''
        msg = message.Message.get_message('have', 65535)
        self.assertEqual(msg.index, 65535)

    def test_get_message__index_upper(self):
        ''' Test upper 2 bytes of index '''
        msg = message.Message.get_message('have', 4294901760)
        self.assertEqual(msg.index, 4294901760)

    def test_get_message_from_bytes(self):
        byte_str = b'\x00\x00\x00\x05\x04\x00\x00\x00\x00'
        msg = message.Message.get_message_from_bytes(byte_str)
        self.assertTrue(isinstance(msg, message.Have))

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
    def test_get_message(self):
        msg = message.Message.get_message('bitfield',
                                          bitfield=b'\x00\x00\x00\x00')
        self.assertTrue(isinstance(msg, message.BitField))

    def test_get_message__to_bytes(self):
        bitfield = b'\x00\x00\x00\x00'
        byte_str = b'\x00\x00\x00\x05\x05\x00\x00\x00\x00'
        msg = message.Message.get_message('bitfield', bitfield=bitfield)
        self.assertEqual(msg.to_bytes(), byte_str)

    def test_get_message__length(self):
        bitfield = b'\x00\x00\x00\x00'
        msg = message.Message.get_message('bitfield', bitfield=bitfield)
        self.assertEqual(msg.length, 5)

    def test_get_message__id(self):
        bitfield = b'\x00\x00\x00\x00'
        msg = message.Message.get_message('bitfield', bitfield=bitfield)
        self.assertEqual(msg.id, 5)

    def test_get_message__bitfield(self):
        bitfield = b'\x00\x00\x00\x00'
        msg = message.Message.get_message('bitfield', bitfield=bitfield)
        self.assertEqual(msg.bitfield, bitfield)

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
    def test_get_message(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertTrue(isinstance(msg, message.Request))

    def test_get_message__to_bytes(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        byte_str = b'\x00\x00\x00\x13\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        byte_str += b'\x00\x00\x00'
        self.assertTrue(msg.to_bytes, byte_str)

    def test_get_message__to_bytes__all_maxed(self):
        msg = message.Message.get_message('request',
                                          index=4294967295,
                                          begin=4294967295,
                                          length=4294967295)
        byte_str = b'\x00\x00\x00\x13\x06\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
        byte_str += b'\xFF\xFF\xFF'
        self.assertTrue(msg.to_bytes, byte_str)

    def test_get_message__length(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertEqual(msg.length, 13)

    def test_get_message__id(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertEqual(msg.id, 6)

    def test_get_message__index(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertEqual(msg.index, 0)

    def test_get_message__begin(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertEqual(msg.begin, 0)

    def test_get_message__request_length(self):
        msg = message.Message.get_message('request',
                                          index=0,
                                          begin=0,
                                          length=0)
        self.assertEqual(msg.request_length, 0)

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


class TestPiece(unittest.TestCase):
    def test_get_message(self):
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=b'')
        self.assertTrue(isinstance(msg, message.Piece))

    def test_get_message__to_bytes(self):
        byte_str = b'\x00\x00\x00\x0e\x07\x00\x00\x00\x00\x00\x00\x00\x00'
        block = b'\x00\x00\x00\x00\x00'
        byte_str += block
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.to_bytes(), byte_str)

#     @unittest.skip("Takes long to test")
#     def test_get_message__to_bytes__max_length(self):
#         byte_str = b'\xFF\xFF\xFF\xFF\x07\x00\x00\x00\x00\x00\x00\x00\x00'
#         block = (b'\x00' * 4294967286)  # max int - 9
#         byte_str += block
#         msg = message.Message.get_message('piece',
#                                           index=0,
#                                           begin=0,
#                                           block=block)
#         self.assertEqual(msg.to_bytes(), byte_str)
# 
    def test_get_message__length_10(self):
        block = (b'\x00')
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.length, 10)

    def test_get_message__length_265(self):
        block = (b'\x00' * 256)
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.length, 265)

    def test_get_message__id(self):
        block = (b'\x00' * 256)
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.id, 7)

    def test_get_message__index(self):
        block = (b'\x00' * 256)
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.index, 0)

    def test_get_message__begin(self):
        block = (b'\x00' * 256)
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.begin, 0)

    def test_get_message__block(self):
        block = (b'\xFF' * 256)
        msg = message.Message.get_message('piece',
                                          index=0,
                                          begin=0,
                                          block=block)
        self.assertEqual(msg.block, block)


# class TestCancel(unittest.TestCase):
#     def test_get_message(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertTrue(isinstance(msg, message.Cancel))
# 
#     def test_get_message__to_bytes(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         self.assertTrue(msg.to_bytes, byte_str)
# 
#     def test_get_message__to_bytes__all_maxed(self):
#         msg = message.Message.get_message('cancel',
#                                           index=4294967295,
#                                           begin=4294967295,
#                                           length=4294967295)
#         byte_str = b'\x00\x00\x00\x13\x08\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
#         byte_str += b'\xFF\xFF\xFF'
#         self.assertTrue(msg.to_bytes, byte_str)
# 
#     def test_get_message__length(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertEqual(msg.length, 13)
# 
#     def test_get_message__id(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertEqual(msg.id, 8)
# 
#     def test_get_message__index(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertEqual(msg.index, 0)
# 
#     def test_get_message__begin(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertEqual(msg.begin, 0)
# 
#     def test_get_message__request_length(self):
#         msg = message.Message.get_message('cancel',
#                                           index=0,
#                                           begin=0,
#                                           length=0)
#         self.assertEqual(msg.request_length, 0)
# 
#     def test_get_message_from_bytes(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertTrue(isinstance(msg, message.Cancel))
# 
#     def test_get_message_from_bytes__length(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.length, 13)
# 
#     def test_get_message_from_bytes__id(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.id, 8)
# 
#     def test_get_message_from_bytes__index(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.index, 0)
# 
#     def test_get_message_from_bytes__max_index(self):
#         byte_str = b'\x00\x00\x00\x13\x08\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.index, 4294967295)
# 
#     def test_get_message_from_bytes__begin(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.begin, 0)
# 
#     def test_get_message_from_bytes__max_begin(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.begin, 4294967295)
# 
#     def test_get_message_from_bytes__request_length(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#         byte_str += b'\x00\x00\x00'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.request_length, 0)
# 
#     def test_get_message_from_bytes__max_request_length(self):
#         byte_str = b'\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\xFF'
#         byte_str += b'\xFF\xFF\xFF'
#         msg = message.Message.get_message_from_bytes(byte_str)
#         self.assertEqual(msg.request_length, 4294967295)
# 
# 
'''
class TestGetMessage(unittest.TestCase):

    def test_port(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(isinstance(msg, Port), True)

    def test_port__to_bytes(self):
        port_b = b'\x00\x00\x00\x03\t\x00P'
        msg_b = Message.get_message('port', None, None, None, None, 80).to_bytes()
        self.assertEqual(msg_b, port_b)

    def test_port__length(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.length, 3)

    def test_port__id(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.id, 9)

    def test_port__listen_port(self):
        msg = Message.get_message('port', None, None, None, None, 80)
        self.assertEqual(msg.listen_port, 80)
'''

if __name__ == '__main__':
    unittest.main()

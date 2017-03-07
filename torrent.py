from bencode import encode, decode
from hashlib import sha1
from math import ceil
from bitstring import BitArray
import os


"""
References: https://wiki.theory.org/BitTorrentSpecification
To download a torrent the following steps will need to be complete.
1. Parse the torrent file
2. From the announce key in the torrent file connect to the trackers
and retrieve the list of peers.
3. Establish a connection with a peer and send a handshake, make sure
to receive a handshake back
4. Start passing messages
"""


class Piece(object):
    def __init__(self, length, block_length=16384):
        self.length = length
        self.block_length = block_length
        self.bitfield = BitArray(ceil(length / (self.block_length)) * '0b0')

    def add_block(self, offset, block):
        pass

    def __str__(self):
        return str(self.piece)

    def __hash__(self):
        return hash(self.piece)


class Torrent(object):
    def __init__(self,
                 torrent_dict,
                 root_path=None):

        self._dict = torrent_dict
        self._root_path = root_path

    @property
    def pieces(self):
        return self._dict[b'info'][b'pieces']

    @property
    def piece_length(self):
        return self._dict[b'info'][b'piece length']

    @property
    def name(self):
        return self._dict[b'info'][b'name'].decode('utf-8')

    @property
    def info_hash(self):
        return sha1(encode(self._dict[b'info'])).digest()

    @property
    def files(self):
        """Returns the files associated with the torrent in the form
        of a dict. {path: length...}
        ex) {'file1.txt': 128,
             'dir/file2.txt': 256}
        """
        files = []
        if b'length' in self._dict[b'info']:
            path = self._dict[b'info'][b'name'].decode('utf-8')
            length = self._dict[b'info'][b'length']
            files.append({'path': path, 'length': length})
        else:
            for file in self._dict[b'info'][b'files']:
                path = [path.decode('utf-8') for path in file[b'path']]
                length = file[b'length']
                files.append({'path': os.path.join(*path),
                              'length': length})
        return files

    @property
    def length(self):
        """Returns the total size of the torrent files to be downloaded"""
        length = 0
        for file in self.files:
            length += file['length']
        return length

    @property
    def trackers(self):
        """Returns the list of trackers in the order they should be queried"""
        if b'announce' in self._dict:
            return list(self._dict[b'announce'].decode('utf-8'))
        elif b'announce-list' in self._dict:
            return [t.decode('utf-8')
                    for trackers in self._dict[b'announce-list']
                    for t in trackers]

    @property
    def bitfield(self):
        return self._bitfield

    def __eq__(self, other):
        ''' Torrents are considered equal if their info_hashes are the same'''
        return self.info_hash == other.info_hash

    def __hash__(self):
        return hash(self.info_hash)

    def __str__(self):
        return self.name

    def __enter__(self):
        pass

    def __exit__(self):
        pass


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    for file in os.listdir('sample_torrents'):
        with open('sample_torrents/' + file, 'rb') as f:
            torrent_dict = decode(f.read())
            torrent = Torrent(torrent_dict)
            pp.pprint('name: %s' % torrent.name)
            pp.pprint('info_hash: %s' % torrent.info_hash)
            pp.pprint('comment: %s' % torrent.comment)
            pp.pprint('status: %s' % torrent.status)
            # pp.pprint('pieces: %s' % torrent.pieces)
            pp.pprint('piece_length: %s' % torrent.piece_length)
            pp.pprint('created_by: %s' % torrent.created_by)
            pp.pprint('creation_date: %s' % torrent.creation_date)
            pp.pprint('encoding: %s' % torrent.encoding)
            pp.pprint('files: %s' % torrent.files)
            pp.pprint('length: %s' % torrent.length)
            pp.pprint('trackers: %s' % torrent.trackers)
            pp.pprint('total_pieces: %s' % torrent.total_pieces)
            pp.pprint('bitfield: %s' % torrent.bitfield)
        print()

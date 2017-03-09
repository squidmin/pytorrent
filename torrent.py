import asyncio
import tempfile
from bencode import decode, encode
from hashlib import sha1
from math import ceil
from bitstring import BitArray
import os
import tracker


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
                 torrent_dict=None,
                 save_path=None):

        self._dict = torrent_dict
        self._save_path = save_path
        self.loop = asyncio.get_event_loop()
        for t in self.trackers:
            self.loop.create_task(tracker.get_peers(self.loop,
                                                    self._add_peers,
                                                    t,
                                                    self.info_hash))

    @classmethod
    def fromurl(cls, url):
        import requests
        response = requests.get(url)
        return cls(decode(response.content))

    @classmethod
    def fromfile(cls, path):
        with open(path, 'rb') as file:
            return cls(decode(file.read()))

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
        if b'announce-list' in self._dict:
            return [t.decode('utf-8')
                    for trackers in self._dict[b'announce-list']
                    for t in trackers]
        elif b'announce' in self._dict:
            return [self._dict[b'announce'].decode('utf-8')]

    @property
    def bitfield(self):
        """Bitfield object for the pieces we are successfully downloaded
        note that this object should not be set directly. But should be
        set by a call back or some other function
        """
        path = os.path.join(tempfile.gettempdir(), str(self.__hash__()))
        print(path)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                num_pieces = ceil((len(self.pieces) / 20))
                f.write('0b' + '0' * num_pieces)
        with open(path, 'r') as f:
            data = f.read()
            self._bitfield = BitArray(data)
        return self._bitfield

    @property
    def peers(self):
        if not hasattr(self, '_peers'):
            self._peers = []

        return self._peers

    def _add_peers(self, peers):
        for p in peers:
            if p not in self.peers:
                self._peers += peers

    def __eq__(self, other):
        ''' Torrents are considered equal if their info_hashes are the same'''
        return self.info_hash == other.info_hash

    def __hash__(self):
        print(int(sha1(self.info_hash).hexdigest(), 16))
        return int(sha1(self.info_hash).hexdigest(), 16)

    def __str__(self):
        return self.name

    def __enter__(self):
        pass

    def __exit__(self):
        pass


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.read()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        url = ('https://yts.ag/torrent/download/'
               'FFCDCB5312F25DB37034552849843981BD401C9D')
        data = await fetch(session, url)
        torrent = Torrent(decode(data))
        print(torrent)
        # print(torrent.info_hash)

if __name__ == '__main__':
    import aiohttp
    import async_timeout
    url = ('https://yts.ag/torrent/download/'
           'FFCDCB5312F25DB37034552849843981BD401C9D')
    loop = asyncio.get_event_loop()
    # loop.create_task(main(loop))
    torrent = Torrent.fromurl(url)
    loop.run_forever()
    print('asdf')

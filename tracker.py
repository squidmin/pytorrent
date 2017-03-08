import socket
import requests
from bencode import decode
from struct import unpack
from util import generate_peer_id


def make_tracker_request(url, info_hash):
    """ Given a torrent info, and tracker_url, returns the tracker
    response. """
    payload = {'info_hash': info_hash,
                'peer_id': generate_peer_id(),
                'uploaded': 0,
                'downloaded': 0,
                'compact': 1}

    # switch to http protocol if necessary
    if url[:3] == 'udp':
        url = 'http' + url[3:]

    # Send the request
    r = requests.get(url, params=payload, timeout=.5, verify=False)
    return decode(r.content)

def decode_expanded_peers(self, peers):
    """ Return a list of IPs and ports, given an expanded list of
    peers, from a tracker response. """
    return [(p["ip"], p["port"]) for p in peers]

def decode_binary_peers(self, peers):
    """ Return a list of IPs and ports, given a binary list of
    peers, from a tracker response. """
    peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
    return [(socket.inet_ntoa(p[:4]), self.decode_port(p[4:]))
            for p in peers]

def get_peers(self):
    """ Update tracker peers, each call adds new peers. """
    try:
        request = make_tracker_request()
    except Exception:
        return None
    peers = request[b'peers']
    if type(peers) == bytes:
        return decode_binary_peers(peers)
    elif type(peers) == list:
        return decode_expanded_peers(peers)
    return None

def decode_port(self, port):
    """ Given a big-endian encoded port, returns the numerical
    port. """
    return unpack(">H", port)[0]

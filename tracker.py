import asyncio
import aiohttp
import async_timeout
import socket
from urllib.parse import urlencode
from bencode import decode
from struct import unpack
from util import generate_peer_id
import torrent


def decode_expanded_peers(peers):
    """ Return a list of IPs and ports, given an expanded list of
    peers, from a tracker response. """
    return [(p["ip"], p["port"]) for p in peers]


def decode_binary_peers(peers):
    """ Return a list of IPs and ports, given a binary list of
    peers, from a tracker response. """
    peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
    return [(socket.inet_ntoa(p[:4]), decode_port(p[4:]))
            for p in peers]


async def get_peers(loop, callback, url, info_hash):
    """ asyncio Function that will take a url and an info hash and call
    callback with the list if we are able to get peers"""
    try:
        request = await make_tracker_request(loop, url, info_hash)
    except:
        return
    peers = decode(request)[b'peers']
    if type(peers) == bytes:
        callback(decode_binary_peers(peers))
    elif type(peers) == list:
        callback(decode_expanded_peers(peers))
    interval = decode(request)[b'interval']
    print(f'refreshing peers from {url} in {interval} seconds')
    loop.create_task(delay(interval, get_peers(loop,
                                               callback,
                                               url,
                                               info_hash)))


def decode_port(port):
    """ Given a big-endian encoded port, returns the numerical
    port. """
    return unpack(">H", port)[0]


async def make_tracker_request(loop, url, info_hash):
    """ Given a torrent info, and tracker_url, returns the tracker
    response. """
    url = url[:3].replace('udp', 'http') + url[3:]
    async with aiohttp.ClientSession(loop=loop) as session:
        return await fetch_peers(session, url, info_hash)

async def fetch_peers(session, url, info_hash):
    params = {'info_hash': info_hash,
              'peer_id': generate_peer_id(),
              'uploaded': 0,
              'downloaded': 0,
              'compact': 1}
    url = url + '?' + urlencode(params)
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.read()

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.read()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        url = ('https://yts.ag/torrent/download/'
               'FFCDCB5312F25DB37034552849843981BD401C9D')
        data = await fetch(session, url)
        t = torrent.Torrent(decode(data))
        print(t)
        print(t.info_hash)

async def delay(n, coro):
    """Helper to delay a coroutine by n seconds."""
    await asyncio.sleep(n)
    return await coro

if __name__ == '__main__':
    url = ('https://yts.ag/torrent/download/'
           'FFCDCB5312F25DB37034552849843981BD401C9D')
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(delay(5, hello('asdf')))

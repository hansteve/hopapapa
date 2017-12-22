#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''id工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import hashlib
import socket
import sys
import random
import threading
import time

from bson.py3compat import PY3
from src.common.object_id import ObjectId


class Snowflake(object):
    region_id_bits = 2
    worker_id_bits = 10
    sequence_bits = 11

    MAX_REGION_ID = -1 ^ (-1 << region_id_bits)
    MAX_WORKER_ID = -1 ^ (-1 << worker_id_bits)
    SEQUENCE_MASK = -1 ^ (-1 << sequence_bits)

    WORKER_ID_SHIFT = sequence_bits
    REGION_ID_SHIFT = sequence_bits + worker_id_bits
    TIMESTAMP_LEFT_SHIFT = (sequence_bits + worker_id_bits + region_id_bits)

    def __init__(self, worker_id, region_id=0):
        self.twepoch = 1490626202000
        self.last_timestamp = -1
        self.sequence = 0

        # assert 0 <= worker_id <= Snowflake.MAX_WORKER_ID
        # assert 0 <= region_id <= Snowflake.MAX_REGION_ID

        self.worker_id = worker_id
        self.region_id = region_id

        self.lock = threading.Lock()

    def generate(self, bus_id=None):
        return self.next_id(
            True if bus_id is not None else False,
            bus_id if bus_id is not None else 0
        )

    def next_id(self, is_padding, bus_id):
        with self.lock:
            timestamp = self.get_time()
            padding_num = self.region_id

            if is_padding:
                padding_num = bus_id

            if timestamp < self.last_timestamp:
                try:
                    raise ValueError(
                        'Clock moved backwards. Refusing to'
                        'generate id for {0} milliseconds.'.format(
                            self.last_timestamp - timestamp
                        )
                    )
                except ValueError:
                    print(sys.exc_info[2])

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & Snowflake.SEQUENCE_MASK
                if self.sequence == 0:
                    timestamp = self.tail_next_millis(self.last_timestamp)
            else:
                self.sequence = random.randint(0, 9)

            self.last_timestamp = timestamp

            res_id = (
                (timestamp - self.twepoch) << Snowflake.TIMESTAMP_LEFT_SHIFT |
                (padding_num << Snowflake.REGION_ID_SHIFT) |
                (self.worker_id << Snowflake.WORKER_ID_SHIFT) |
                self.sequence
            )

            return "A{}".format(res_id)

    def tail_next_millis(self, last_timestamp):
        timestamp = self.get_time()
        while timestamp <= last_timestamp:
            timestamp = self.get_time()
        return timestamp

    def get_time(self):
        return int(time.time() * 1000)


# ID    shards  table   timestamp   random
#       8       8       32          16
#                                   65535


TIMESTAMP_BEGIN = 1489334528

RANDOM_MIN = 0
RANDOM_MAX = 65535

TIMESTAMP_OFFSET = 16
TABLE_OFFSET = 32 + TIMESTAMP_OFFSET
SHARD_OFFSET = 8 + TABLE_OFFSET

INC = int(random.randint(RANDOM_MIN, RANDOM_MAX))


def generate_id(shard_seed, table_seed):
    '''
    根据设置shard_seed和table_seed来生成id
    :param shard_seed:
    :param table_seed:
    :return:
    '''
    shard = shard_seed << SHARD_OFFSET
    table = table_seed << TABLE_OFFSET
    t = (int(time.time()) - TIMESTAMP_BEGIN) << TIMESTAMP_OFFSET
    _inc = int(random.randint(RANDOM_MIN, RANDOM_MAX))

    id = shard | table | t | _inc

    return id


def _machine_bytes():
    """Get the machine portion of an ObjectId.
    """
    machine_hash = hashlib.md5()
    if PY3:
        # gethostname() returns a unicode string in python 3.x
        # while update() requires a byte string.
        machine_hash.update(socket.gethostname().encode())
    else:
        # Calling encode() here will fail with non-ascii hostnames
        machine_hash.update(socket.gethostname())
    return machine_hash.digest()[0:3]


if __name__ == '__main__':
    Snowflake.generate()

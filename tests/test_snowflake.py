import sys
import random
import threading
import time

from concurrent import futures


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

            return (
                (timestamp - self.twepoch) << Snowflake.TIMESTAMP_LEFT_SHIFT |
                (padding_num << Snowflake.REGION_ID_SHIFT) |
                (self.worker_id << Snowflake.WORKER_ID_SHIFT) |
                self.sequence
            )

    def tail_next_millis(self, last_timestamp):
        timestamp = self.get_time()
        while timestamp <= last_timestamp:
            timestamp = self.get_time()
        return timestamp

    def get_time(self):
        return int(time.time() * 1000)


def main():
    id_set = set()
    snowflake = Snowflake(1)

    def gen_id():
        try:
            _id = snowflake.generate()
            print(_id,type(_id))
        except Exception as e:
            print(e)
        else:
            assert _id not in id_set
            id_set.add(_id)

    with futures.ThreadPoolExecutor(max_workers=16) as executor:
        futs = [executor.submit(gen_id) for _ in range(100)]

    print('{0} IDs in the set'.format(len(id_set)))


if __name__ == '__main__':
    # main()
    print(len('{:b}'.format(1692743523876472836)))

    # snowflake = Snowflake(0)
    # for i in range(1,100):
    #     id = snowflake.generate()
    #     print(id)

    print(Snowflake(0).generate())
    print(Snowflake(1).generate())
    print(Snowflake(2).generate())
    print(Snowflake(2,2).generate())
    print(Snowflake(100,19).generate())
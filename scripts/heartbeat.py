import itertools
import json
import random
import string
import sys
import time
from collections import OrderedDict

sys.path.append('../backend/service')
from app.enums.states import StateEnum
import requests
from argparse import ArgumentParser
import pprint


def generate_random_json(records=5):
    tmp = {}
    data = OrderedDict(foo='bar', a='b', bar='foo', lorem='ipsum')
    for i in range(records):
        for p in itertools.permutations(data.items()):
            tmp[f"{random.choice(string.ascii_letters)}-{random.randrange(1000)}"] = json.loads(
                json.dumps(OrderedDict(p)).replace("'", '"'))
    return tmp


def generate_sensor(sensor, url):
    response = requests.post(f"{url}/sensors/", json={
        "serial_number": sensor,
        "metadata": generate_random_json(2)
    })
    assert response.status_code == 201


def beat(sensor, url, count, offline):
    for i in range(count):
        response = requests.post(f"{url}/heartbeats/", json={
            "serial_number": sensor,
            "state": StateEnum.UP.name if not offline else StateEnum.DOWN.name,
            "people_in_area": random.randint(0, 100) if not offline else 0,
            "timestamp": int(time.time()),
            "metadata": generate_random_json(2)
        })
        assert response.status_code == 201
        print("============== Heartbeat ============== ")
        pprint.pprint(response.json())
        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser(description="Heartbeat Demo")
    parser.add_argument("-s", dest="sensor", required=True,
                        help="serial_number")
    parser.add_argument("-u", dest="url", required=True,
                        help="url")
    parser.add_argument("-c", dest="count", required=True,
                        help="number of seconds", type=int)
    parser.add_argument('--offline', dest='offline', action='store_true')
    args = parser.parse_args()
    generate_sensor(args.sensor, args.url)
    beat(args.sensor, args.url, args.count, args.offline)

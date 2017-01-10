#!/usr/bin/env python

import argparse
import struct
import paho.mqtt.client as mqtt

from RadioSerial import RadioSerial
from RadioGPIO import RadioGPIO

import encryption
import topics

def main():
    parser = argparse.ArgumentParser(description='A serial to mqtt gateway')
    parser.add_argument(
        '-d', '--dev', dest='dev', default='/dev/ttyUSB0', type=str,
        help='The serial device')

    parser.add_argument(
        '-b', '--baud', dest='baud', default=115200, type=int,
        help='The baud rate')

    parser.add_argument(
        '-H', '--host', dest='host', default='localhost', type=str,
        help='The mqtt broker host')

    parser.add_argument(
        '-p', '--port', dest='port', default=1883, type=int,
        help='The mqtt broker port')

    parser.add_argument(
        '-r', '--radio', dest='radio', default='gpio', type=str,
        help='The radio connection (serial|gpio)')

    parser.add_argument(
        '-D', '--debug', dest='debug', action='store_true'
    )

    args = parser.parse_args()
    if args.radio == 'serial':
        radio = RadioSerial(args.dev, args.baud)
    else:
        radio = RadioGPIO()

    mqttc = mqtt.Client()
    mqttc.connect(args.host, args.port)
    mqttc.loop_start()

    while True:
        try:
            msg = radio.readmsg()

        except (KeyboardInterrupt):
            mqttc.loop_stop() 
            break

        if args.debug:
            print "=============="
            print "Message-Length: %d" % (len(msg))

        topicsBase = "sensors/network%d/node%d/" % (radio.networkid(), radio.senderid())
        if args.debug:
            print topicsBase

        mqttc.publish(topicsBase + str('RSSI'), radio.rssi())
        if args.debug:
            print "RSSI: %s" % (radio.rssi())


        pos = 0

        while pos < len(msg):
            tmp = ord(msg[pos])
            key = tmp >> 2
            length = (tmp & 0x03) + 1;

            start = pos + 1
            pos = start + length

            value = msg[start:pos]

            if key not in topics.mapping:
                continue

            topicDef = topics.mapping[key]
            topicName = topicDef[0]

            u1 = str(length) + 'b'
            u2 = topicDef[1]
            p1 = u1 + 'x' * (4 - length)

            x = struct.unpack(u1, value)
            data = struct.unpack(u2, struct.pack(p1, *x))[0]

            if len(topicDef) > 2:
                data = "%.2f" % (data / topicDef[2])

            if args.debug:
                print "%s: %s (%d)" % (topicName, data, length)

            mqttc.publish(topicsBase + topicName, data)


if __name__ == "__main__":
    main()

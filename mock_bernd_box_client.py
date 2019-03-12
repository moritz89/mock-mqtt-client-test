#!/usr/bin/python

import paho.mqtt.client as mqtt
import time
import json


class MockBerndBoxClient(mqtt.Client):
    """ A mock implementation of the BerndBox MQTT interface

    This class subscribes to the same topics a typical BerndBox would subscribe to and has a similar
    publish behavior.

    TBD: The enabled sensors can be passed in the constructor to configure the status message
    """

    def set_report_protocol(self, data):
        print(data)

    def task_report_protocol(self, data):
        print(data)

    def set_pump_state(self, data):
        print(data)

    def mock_disconnect(self, data):
        self.disconnect()

    topic_subscriptions = {
        "task_control/in": task_report_protocol,
        "set/report_protocol/in": set_report_protocol,
        "set/pump_state/in": set_pump_state,
        "mock/disconnect": mock_disconnect,
    }

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        try:
            data = json.loads(msg.payload)
        except json.JSONDecodeError as e:
            print(e)
            return

        self.topic_subscriptions[msg.topic](self, data)

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        return
        # print(string)

    def run(self):
        self.connect("localhost", 1883, 60)
        for topic in self.topic_subscriptions:
            self.subscribe(topic)

        # Non-blocking MQTT loop (without sleep ^^)
        # mqttc.loop_start()
        # time.sleep(60)

        # Blocking MQTT loop
        mqttc.loop_forever()


mqttc = MockBerndBoxClient()
mqttc.run()


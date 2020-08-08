import netsock
import mqttsock
import time
import json
import argparse
import sys

# Stages json to use
stagesString='{"s1":{"aerator":{"active":false,"targetValue":0},"boiler":{"active":false,"targetValue":0},"boilerValve":{"active":false,"targetValue":0},"boilerVolume":{"active":false,"targetValue":0},"controllerInfo":{"active":false,"targetValue":0},"cooler":{"active":false,"targetValue":0},"delayTimer":{"active":true,"targetValue":0.4},"dispenser1":{"active":false,"targetValue":0},"dispenser2":{"active":false,"targetValue":0},"dispenser3":{"active":false,"targetValue":0},"dispenser4":{"active":false,"targetValue":0},"envTemp":{"active":false,"targetValue":0},"hotWaterPump":{"active":false,"targetValue":0},"hwtVolume":{"active":false,"targetValue":0},"mashStirrer":{"active":false,"targetValue":0},"mashTemp":{"active":false,"targetValue":0},"mashVolume":{"active":false,"targetValue":0},"plateValve":{"active":false,"targetValue":0},"waterCirculationPump":{"active":true,"targetValue":1},"waterHeater":{"active":false,"targetValue":95},"wortPump":{"active":false,"targetValue":0}},"s2":{"aerator":{"active":false,"targetValue":0},"boiler":{"active":false,"targetValue":0},"boilerValve":{"active":false,"targetValue":0},"boilerVolume":{"active":false,"targetValue":0},"controllerInfo":{"active":false,"targetValue":0},"cooler":{"active":false,"targetValue":0},"delayTimer":{"active":true,"targetValue":0.1},"dispenser1":{"active":false,"targetValue":0},"dispenser2":{"active":false,"targetValue":0},"dispenser3":{"active":false,"targetValue":0},"dispenser4":{"active":false,"targetValue":0},"envTemp":{"active":false,"targetValue":0},"hotWaterPump":{"active":false,"targetValue":0},"hwtVolume":{"active":false,"targetValue":0},"mashHeater":{"active":false,"targetValue":92},"mashStirrer":{"active":false,"targetValue":0},"mashTemp":{"active":false,"targetValue":0},"mashVolume":{"active":false,"targetValue":0},"plateValve":{"active":false,"targetValue":0},"waterCirculationPump":{"active":true,"targetValue":1},"waterHeater":{"active":false,"targetValue":95},"wortPump":{"active":false,"targetValue":0}}}'

def stateFromStatus(status):
    statusdict = json.loads(status)
    state = statusdict['state']
    if 'status' in statusdict:
        time = statusdict['status']['delayTimer']['actual']
        stage = statusdict['stage']
    else:
        time = '0'
        stage = 'none'
    print('State:{} Stage:{} Time:{}'.format(state,stage,time))

def assertState(data, state):
    statusdict = json.loads(data)
    actualState = statusdict['state']
    if state != actualState:
        print('Expected: {}  Actual: {}'.format(state,actualState))
        sys.exit(1)
    else:
        print('State Assert {} OK'.format(state))

def assertStage(data, stage):
    statusdict = json.loads(data)
    if 'stage' in statusdict:
        actualStage = statusdict['stage']
        if stage != actualStage:
            print('Expected: {}  Actual: {}'.format(stage,actualStage))
            sys.exit(1)
        else:
            print('Stage Assert {} OK'.format(stage))

def testTitle(name):
    print('================================={}'.format(name))

def waitfor_state(client, state, timeout):
    for x in range(timeout):
        time.sleep(1)
        data = client.read_status()
        statusdict = json.loads(data)
        actualState = statusdict['state']
        if actualState == state:
            print('State {} read'.format(state))
            return()

    print('Timeout in waiting for state {}. Actual state: {}'.format(state, actualState))
    sys.exit(1)


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    args = parser.parse_args()

    if args.netsock:
        client = netsock.socketclient()
    if args.mqtt:
        client = mqttsock.socketclient(connection='localhost')
        # Wait for a message to appear
        time.sleep(2)
    if args.aws:
        client = mqttsock.socketclient(connection='aws')
        # Wait for a message to appear
        time.sleep(2)



    testTitle('Test initial state, it should be stop')
    data = client.read_status()
    stateFromStatus(data)
    assertState(data, 'stop')

    testTitle('Start run and pause. Make sure stage does not change')
    assert client.write_command(stagesString) == 'ok'
    assert client.write_command('run') == 'ok'
    time.sleep(1)
    stateFromStatus(client.read_status())
    time.sleep(1)
    assertState(client.read_status(), 'run')
    assertStage(client.read_status(), 's1')
    data = client.write_command('pause')
    waitfor_state(client, 'pause', 6)
    time.sleep(5)
    assertState(client.read_status(), 'pause')
    time.sleep(2)
    assert client.write_command('run') == 'ok'
    time.sleep(2)
    assert client.write_command('run') == 'ok'
    waitfor_state(client, 'run', 10)
    assert client.write_command('stop') == 'ok'
    waitfor_state(client, 'stop', 6)

    testTitle('Load stages, see that it does not start')
    assert client.write_command(stagesString) == 'ok'
    time.sleep(3)
    stateFromStatus(client.read_status())
    assertState(client.read_status(), 'stop')

    testTitle('Start run and see it progresses and stops by itself. It will take time')
    assert client.write_command(stagesString) == 'ok'
    assert client.write_command('run') == 'ok'
    time.sleep(1)
    stateFromStatus(client.read_status())
    time.sleep(1)
    assertState(client.read_status(), 'run')
    assertStage(client.read_status(), 's1')
    waitfor_state(client, 'stop', 60)

    testTitle('Start run and manually stop.')
    assert client.write_command(stagesString) == 'ok'
    assert client.write_command('run') == 'ok'
    time.sleep(1)
    stateFromStatus(client.read_status())
    time.sleep(1)
    assertState(client.read_status(), 'run')
    assertStage(client.read_status(), 's1')
    assert client.write_command('stop') == 'ok'
    waitfor_state(client, 'stop', 6)

    testTitle('Start run and skip. Make sure stage does change and state is run again')
    assert client.write_command(stagesString) == 'ok'
    assert client.write_command('run') == 'ok'
    time.sleep(1)
    stateFromStatus(client.read_status())
    time.sleep(1)
    assertState(client.read_status(), 'run')
    assertStage(client.read_status(), 's1')
    assert client.write_command('skip') == 'ok'
    time.sleep(1)
    waitfor_state(client, 'run', 10)
    assertStage(client.read_status(), 's2')
    assert client.write_command('stop') == 'ok'
    waitfor_state(client, 'stop', 6)

    testTitle('Terminate server and client')
    assert client.write_command('terminate') == 'ok'
    client.stop()
    print("Program should be terminated")
    sys.exit(0)

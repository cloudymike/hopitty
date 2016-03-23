#!/usr/bin/env python
import pika
import time
import sys

def get_command(cmdchannel):
    method_frame, header_frame, cmdbody = cmdchannel.basic_get('commands')
    if method_frame:
        print('----', cmdbody)
        cmdchannel.basic_ack(method_frame.delivery_tag)
    else:
        cmdbody = None
    return(cmdbody)


def runFromQueue(rabbithost='localhost'):

    def callback(ch, method, properties, body):
        """
        Make this nested as we need some globals to be passed in, as the channels
        """
        print "worker started"
    
        pause = False

        # Clear out any commands. This is questionable but keep it like this 
        # to avoid any commands in queue mssing things up.
        while get_command(ch) is not None:
            pass

        # Wait for a start command
        while get_command(ch) != "start":
            pass
    
        worklist = {'A': 'AUTO', 'B': 'BANANA', 'C': 'Cycle'};
        # Do your stuff
        for r_key, settings in sorted(worklist.items()):
            count = 0
            iamdone = False
            while not iamdone:
                cmdbody = get_command(ch)
                if cmdbody == 'die':
                    sys.exit(1)
                if cmdbody == 'pause':
                    pause = not pause
                if cmdbody == 'skip':
                    break
                if cmdbody == 'stop':
                    return

                if not pause:
                    count = count + 1
                    iamdone = count > 9
                
                message = r_key+str(count)
                #print message
                logchannel.basic_publish(exchange='logs',
                              routing_key='',
                              body=message)

                time.sleep(1)
        return


    # Loading up a worker
    workconnection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rabbithost))
    workchannel = workconnection.channel()

    workchannel.queue_declare(queue='workpkg')

    # Control the worker
    cmdconnection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbithost))
    cmdchannel = cmdconnection.channel()

    cmdchannel.queue_declare(queue='commands')

    # log results
    logconnection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbithost))
    logchannel = logconnection.channel()

    logchannel.exchange_declare(exchange='logs',
                             type='fanout')


    workchannel.basic_consume(callback,
                          queue='workpkg',
                          no_ack=True
                          )

    print('Worker is ready and waiting. To exit press CTRL+C')
    workchannel.start_consuming()


if __name__ == '__main__':
    runFromQueue()
    
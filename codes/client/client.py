# coding: utf-8
import time
import threading
import node


class Client(threading.Thread):
    
    def __init__(self):        
        super().__init__(name = 'Client', daemon = True)
        self.node = node.Node()
        self.status = self.node.worker.status
        self.sync_file = self.node.sync_file
        self.reset_workers = self.node.reset_workers

    def request(self, receiver, message):
        try:
            message['receiver'] = receiver
            return self.node.request(**message)
        except Exception as e:
            print(e)

    def run(self):
        self.node.run()
       
    def stop(self):
        self.node.stop()


if __name__ == '__main__':

    the_client = Client()
    the_client.start()
    while not the_client.status['Is connected']:
        time.sleep(1)
        print('Node not ready yet.')

    ## reset workers
    # the_client.reset_workers()
    # time.sleep(15)

    # sync_file
    # the_client.sync_file('tasks.py', load_as_tasks = True)



    from collections import OrderedDict

    messages = OrderedDict()

    messages['read_GPIOs'] = {'message_type': 'command',
                              'command': 'read GPIOs',
                              'kwargs': {'pins': [5, 12, 13, 14, 15, 16]},
                              'need_result': True}

    messages['blink_led'] = {'message_type': 'command',
                             'command': 'blink led',
                             'kwargs': {'times': 3, 'forever': False,
                                        'on_seconds': 0.1, 'off_seconds': 0.1}}

    the_client.node.worker.roll_call()
    time.sleep(2)
    remote_nodes = sorted(the_client.node.worker.contacts.keys())

    print('\n[____________ Connected nodes ____________]\n')
    print('\nConnected nodes:\n{}\n'.format(remote_nodes))

    results = None

    def test1():
        count = 10

        the_client.node.broadcast(messages['blink_led'])
        return  None

    print('********** result:\n', test1(), '\n**********')


    def test2():
        for remote_node in remote_nodes:
            _, result = the_client.request(remote_node, messages['read_GPIOs'])
            print('\nGPIO status for {}: {}\n'.format(remote_node, result.get()))

    print('********** result:\n', test2(), '\n**********')


    def test3():
        return  results

    # print('********** result:\n', test3(), '\n**********')


    def test4():
        return  results

    # print('********** result:\n', test4(), '\n**********')


    def test5():
        return  results

    # print('********** result:\n', test5(), '\n**********')


    def test6():
        return  results

    # print('********** result:\n', test6(), '\n**********')
    

    time.sleep(3)

# coding: utf-8
import os
import sys
import config_mqtt
import config_identity

if config_identity.IS_MICROPYTHON:
    import worker_upython as worker_impl
else:
    import worker_cpython as worker_impl 
    

class Node:

    def __init__(self):
        super().__init__()
        self.worker = worker_impl.Worker(config_mqtt.BROKER_HOST, config_mqtt.HUB_PORT)
        self.worker.set_parent(self)
        self.broadcast = self.worker.broadcast
        
    def run(self):
        self.worker.run()
        
    def stop(self):
        self.worker.stop()
        self.worker.set_parent(None)
        
    def request(self, **message):
        return self.worker.request(message)

    def reset_workers(self):
        message = {'message_type': 'exec',
                   'to_exec': 'import machine;machine.reset()'}
        self.broadcast(message)

    def sync_file(self, file, load_as_tasks = False):
        with open(file) as f:
            content = f.read()

        message = {'message_type': 'file',
                   'kwargs': {'filename': os.path.basename(file),
                              'file':content,
                              'load_as_tasks': load_as_tasks}}
        self.broadcast(message)


def main():
    try:
        node = Node()
        node.run()

    except KeyboardInterrupt:
        print("Ctrl C - Stopping.")
        node.stop()
        node = None
        sys.exit(1)


if __name__ == '__main__':
    main()

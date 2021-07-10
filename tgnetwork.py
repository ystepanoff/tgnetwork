from discover import Observer
from configparser import ConfigParser

config = ConfigParser()
config.read('tgnetwork.config')

session = config['telegram']['session']
api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']

channels = ['doktorvladi']

if __name__ == '__main__':
    observer = Observer(session, api_id, api_hash)
    for channel in channels:
        for message in observer.iter_messages(channel):
            if message.forward:
                print(message.forward.original_fwd)
                print('---')
                print(message)

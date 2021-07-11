from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from configparser import ConfigParser
import csv

config = ConfigParser()
config.read('tgnetwork.config')

session = config['telegram']['session']
api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']


channels_meta = {
    'marinelepen': {
        'name': 'Marine Le Pen',
        'depth': 1,
        'parent': None,
        'total': 1
    }
}
channels = ['marinelepen']
max_depth = 10
out_csv = 'marielepen.csv'


def write_csv():
    global channels
    global channels_meta
    global out_csv
    with open(out_csv, 'wt') as file:
        cw = csv.writer(file)
        cw.writerow(['handle', 'name', 'depth', 'parent', 'total'])
        for ch in channels:
            row = [
                ch,
                channels_meta[ch]['name'],
                channels_meta[ch]['depth'],
                channels_meta[ch]['parent'],
                channels_meta[ch]['total']
            ]
            cw.writerow(row)

            
if __name__ == '__main__':
    with TelegramClient(session, api_id, api_hash) as client:
        for ch in channels:
            if channels_meta[ch]['depth'] >= max_depth:
                continue
            for message in client.iter_messages(ch):
                if message.forward:
                    forward = message.forward
                    if forward.from_id:
                        try:
                            #client(JoinChannelRequest(forward.from_id.channel_id))
                            channel = client.get_entity(forward.from_id.channel_id)
                            if channel.username:
                                if not channel.username in channels:
                                    #print(channel)
                                    channels.append(channel.username)
                                    channels_meta[channel.username] = {
                                        'name': channel.title,
                                        'depth': channels_meta[ch]['depth'] + 1,
                                        'parent': ch,
                                        'total': 1
                                    }
                                    print(channels_meta)
                                    print('----------------------')
                                    write_csv()
                                else:
                                    channels_meta[channel.username]['total'] += 1
                        except AttributeError:
                            pass
                        except:
                            print('Error: ', forward.from_id)

from telethon.sync import TelegramClient

class Observer:
    def __init__(self, session, api_id, api_hash):
        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash

    def iter_messages(self, handle):
        with TelegramClient(self.session, self.api_id, self.api_hash) as client:
            messages = client.iter_messages(handle)
            for message in messages:
                yield message 

#coding=utf-8

from  wxbot import *
from msghandle import *

class MyBot(WXBot):

    def handle_msg_all(self,msg):
        tl = Tulingbot()
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(tl.replay(
                                                    msg['content']['data'],
                                                    msg['user']['id']),
                                msg['user']['id'])

        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            if 'detail' in msg['content']:
                self.send_msg_by_uid(tl.replay(
                                                msg['contact']['data'],
                                                msg['user']['id']
                                            ),
                                msg['user']['id'])


def main():
    b=MyBot()
    b.DEBUG = True
    b.conf['qr'] = 'tty'
    b.run()
    

if __name__ == "__main__":
    main()

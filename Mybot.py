#coding=utf-8

from  wxbot import *
from msghandle import *

import sys
default_encoding='utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
tl = Tulingbot()
mc = MChandle()
mc.log_read()

class MyBot(WXBot):

    
    def handle_msg_all(self,msg):
        '''
        if msg['msg_type_id'] == 3  and msg['content']['type'] == 0:
            self.send_msg_by_uid(tl.replay(
                                                    msg['content']['data'],
                                                    msg['user']['id']),
                                msg['user']['id'])
        '''
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            if msg['content']['data'][0:3] == ':mc':
                mc_msg = mc.command_handle(msg['content']['data'][4::])
                self.send_msg_by_uid(mc_msg,msg['user']['id'])


def main():
    b=MyBot()
    b.DEBUG = True
    b.conf['qr'] = 'tty'
    b.run()
    

if __name__ == "__main__":
    main()

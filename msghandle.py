#coding=utf-8
import requests
import json
import ConfigParser
import os 
import time 

import sys
default_encoding='utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
class Tulingbot():
    def __init__(self):
        self.tuling_key=''
    
        try:
            configfile = ConfigParser.ConfigParser()
            configfile.read('conf.ini')
            self.tuling_key = configfile.get('tuling','key')
        except Exception:
            print 'api key error '
#        print 'tuling key :',self.tuling_key
    
    def replay(self,msg,uid=1):
        if self.tuling_key:
            url = 'http://www.tuling123.com/openapi/api'
            body = {"key":self.tuling_key,
                    "info":msg.encode('utf-8'),
                    "userid":uid,
                   }
            resp = requests.post(url, data=body)
            r = json.loads(resp.text)
         #   print r
            if r['code'] == 40004:  #api请求次数耗尽
                result = "小哥今天不想说话了 (/“≡ _ ≡)/~┴┴"
            elif r['code'] == 200000:  #连接类
                result = r['url']
            elif r['code'] == 302000:  #新闻类
                for k in r['list']:
                    result = result + u'『 ' + k['source'] +u'』' +\
                            k['article'] + '\t' + k['detailurl'] + '\n'
            elif r['code'] == 308000:  #菜谱类
                result = r[u'list'][0][u'detailurl']
            else:
                result = r['text'].replace('<br>', ' ')
                result = result.replace(u'\xa0', u' ')
            return result   
        else:
            return '获取错误'



class MChandle():
    def __init__(self):
        self.mclog = ''
        self.screen = ''
        
        try:
            configfile = ConfigParser.ConfigParser()
            configfile.read('conf.ini')
            self.mclog = configfile.get('MClog','log')
            self.screen = configfile.get('SCREEN','name')
        except Exception:
            print 'log loads  error '
    
    def log_lines(self):  #读取mc日志行数，读取'\n'个数来达到目地
        with open(self.mclog,'r') as f:
            return len(f.readlines())
        '''
        try:
            f = open(self.mclog, 'rb')
            count = 0   
            while True:
                buffer = f.read(8192*1024)
                if not buffer:
                    break
                count += buffer.count('\n')
        except Exception:
            print "log read error"
        finally:
            if f:
                f.close()
            else:
                count = 0
        return count           
        '''
    def log_read(self,start_line,end_line):
        m =0
        line = ''
        with open(self.mclog,'r') as f:
            for i in f:
                m = m+1
                if m > start_line  and m< end_line:
                    line = line +i            
            return line 

    def command_handle(self,msg):
        '''
        screen -S java -p 0 -X stuff "$(printf "help\r")"
        '''
        tmp =self.log_lines()
        time.sleep(1)
        before_command = self.log_lines()
        os.system('screen -S {0} -p 0 -X stuff \"$(printf \"{1}\r\")\"'.format(self.screen,msg))
        tmp = self.log_lines()
        time.sleep(1)
        after_command = self.log_lines()
        if before_command <= after_command:
            return self.log_read(before_command,after_command)
        else:
            return '命令执行失败'


            
            































def main():
    while 1:
        tuling =Tulingbot()
        a = tuling.replay(raw_input())
        print '!!---->',a

if __name__ == "__main__":
    main()

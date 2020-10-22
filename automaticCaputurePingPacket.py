# 抑制scapy导入所出现的报错信息
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


'''
构造ICMP数据包，在Linux系统下能够成功发包，而Windows系统下ICMP数据包发不出去。
参考：https://blog.csdn.net/rootkitylp/article/details/53098832

向多个主机发送自定义ICMP报文并分别抓取数据包
'''

# 导入相应的包
from scapy.all import *
from random import randint
import six
import _thread
import signal
import time

def ping_once(host, payload):

    # 随机产生一个1-65535的icmp的id位
    icmp_id=randint(1,65535)

    # 随机产生一个1-65535的icmp的序列号
    icmp_seq=randint(1,65535)

    packet=IP(dst=host,ttl=64)/ICMP(id=icmp_id,seq=icmp_seq)/payload
    
    # print(packet)
    # 发送数据包
    ping=sr(packet,timeout=2)
    # print(ping[0].res)
    # 如果收到回复则代表ping成功，成功就以退出码3退出(便于后续用来判断此进程是否成功)

def iping(host):
    # 铸造数据包
    payload = b''
    # 多线程，由于tcpdump运行后是阻塞式的，放入子线程，防止阻塞主线程
    _thread.start_new_thread(startCapturePacket, (host,))
    for i in range(0, 100):

        random_byte = randint(1, 255)
        # 将十进制数转换成单个字节
        cur_bytes = six.int2byte(random_byte)

        payload += cur_bytes
        
        ping_once(host, payload)
    # 暂停1s，用来记录所有的ICMP报文
    time.sleep(1)
    pid = os.system("ps -A | grep \"tcpdump\" | awk '{print $1}'")
    print(pid)
    # 关闭tcpdump，才能写入报文 这种写法会终止整个程序
    # os.kill(pid, signal.SIGTERM)
    # 下面这种写法等同于 Ctrl + C
    os.system("kill -2 " + str(pid))

def startCapturePacket(host):
    os.system("sudo tcpdump icmp -U -i ens33 -w test_" + host + ".pcap")


if __name__ == '__main__':
    # host_list = ["10.25.23.5", "10.26.33.233"]
    host_prefix = "10.26.3"
    suffix = ["3.100", "2.143", "3.101", "2.144", "2.145", "2.146"]
    for host in host_list:
        iping(host)
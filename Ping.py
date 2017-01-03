import threading,subprocess
from time import ctime,sleep,time
import Queue
queue=Queue.Queue()
class ThreadUrl(threading.Thread):
        def __init__(self,queue):
                threading.Thread.__init__(self)
                self.queue=queue
        def run(self):
                while True:
                        host=self.queue.get()
                        ret=subprocess.call('ping -c 1 '+host,shell=True,stdout=open('/dev/null'))
                        if ret:
                                print "%s is down" % host
                        else:
                                print "%s is up" % host
                        self.queue.task_done()
def main():
        for i in range(100):
                t=ThreadUrl(queue)
                t.setDaemon(True)
                t.start()
        for host in b:
                queue.put(host)
        queue.join()
b=['192.168.1.'+str(x) for x in range(1,10)] #ping 192.168.3 网段
start=time()
main()
print "Elasped Time:%s" % (time()-start)

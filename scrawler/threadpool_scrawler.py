from queue import Queue
from threading import Thread, Lock
import urllib.parse
import socket
import re
import time

import sys
import multiprocessing.pool

seen_urls = set(['/'])
lock = Lock()

DEBUG = True
TARGET = 'theuselessweb.com'

class Fetcher(Thread):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            url = self.tasks.get()
            print(url)
            sock = socket.socket()
            sock.connect((TARGET, 80))
            get = 'GET {0} HTTP/1.0\r\nHost: {1}\r\n\r\n'.format(url, TARGET)
            sock.send(get.encode('ascii'))
            response = b''
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            
            links = self.parse_links(url, response)

            lock.acquire()
            for link in links.difference(seen_urls):
                self.tasks.put(link)
            seen_urls.update(links)
            lock.release()

            self.tasks.task_done()
    
    def parse_links(self, fetched_url, response):
        if not response:
            print('error: {}'.format(fetched_url))
            return set()
        if not self._is_html(response):
            return set()
        urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                              self.body(response)))
        links = set()
        for url in urls:
            normalized = urllib.parse.urljoin(fetched_url, url)
            parts = urllib.parse.urlparse(normalized)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            host, port = urllib.parse.splitport(parts.netloc)
            if host and host.lower() not in (TARGET):
                continue
            defragmented, frag = urllib.parse.urldefrag(parts.path)
            links.add(defragmented)
        return links
    # the code only deal with urls in domain name, so, normalized = base + relative
    # normalized format: https://wiki.python.org/moin/PythonBooks -> scheme: https, host: wiki.python.org, defragmented: /moin/PythonBooks
    # normalized format: /library/index.html -> scheme: '', host: '', defragmented: /library/index.html

    # urljoin(https://domain/sth/sth/sth, absolute path) -> https://domain/absolute path
    # urljoin(other, absolute path) -> absolute path
    # urljoin(https://domain/sth/sth/sth/path/, relative path) -> https://domain/sth/sth/sth/path/relative path
    # urljoin(https://domain/sth/sth/sth/sth, relative path) -> https://domain/relative path

    def body(self, response):
        body = response.split(b'\r\n\r\n', 1)[1]
        #body is http content, is the whole html
        return body.decode('utf-8')
    
    def _is_html(self, response):
        head, body = response.split(b'\r\n\r\n', 1)
        # head.decode() = http header
        #'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nAccept-Ranges: bytes\r\nCache-Control: public, max-age=0\r\nLast-Modified: Sun, 26 Jun 2016 03:09:20 GMT\r\nETag: W/"2390-1558aaecf00"\r\nContent-Length: 9104\r\nVary: Accept-Encoding\r\nDate: Tue, 27 Mar 2018 05:44:16 GMT\r\nConnection: close'
        headers = dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
        #dict([[key1, value1], [key2, value2]]) -> {key1:value1, key2:value2}
        
        return headers.get('Content-Type', '').startswith('text/html')


class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads):
            Fetcher(self.tasks)
    
    def add_task(self, url):
        self.tasks.put(url)

    def wait_completion(self):
        self.tasks.join()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        #self-defined threadpool
        start = time.time()
        pool = ThreadPool(4)
        pool.add_task('/')
        pool.wait_completion()
        print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls), time.time()-start))
    elif sys.argv[1] == '-s':
        # system threadpool
        start = time.time()
        pool = multiprocessing.pool.ThreadPool()
        tasks = Queue()
        tasks.put('/')
        workers = [Fetcher(tasks) for i in range(4)]
        pool.map_async(lambda w:w.run(), workers)
        tasks.join()
        pool.close()
        print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls), time.time()-start))
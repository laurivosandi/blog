
import os
import urllib
import shutil
import socket
from urllib.parse import urlparse, unquote

class Crawler(object):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19',
        "Accept": "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    class LinkBroken(Exception):
        def __init__(self, url):
            self.url = url
        def __str__(self):
            return self.url

    def __init__(self, cache, blacklist, whitelist):
        self.cache_path = cache
        self._blacklist_path = blacklist
        self._whitelist_path = whitelist
        
        with open(blacklist) as fh:
            self.blacklist_set = set(fh.read().split("\n"))
            
        # Preload URL whitelist
        with open(whitelist) as fh:
            self.whitelist_set = set(fh.read().split("\n"))
            
        self._blacklist_append = open(blacklist, "a")
        self._whitelist_append = open(whitelist, "a")

    def check(self, url):
        print("Checking URL:", url)

        if url in self.blacklist_set:
            raise self.LinkBroken(url)
        req = urllib.request.Request(url, headers=self.HEADERS)
        try:
            with urllib.request.urlopen(req, None, 3) as ih:
                print("Checking URL:", url)
                buf = ih.read(1024)
        except (urllib.error.URLError, socket.timeout):
            self.blacklist(url)
            raise self.LinkBroken(url)
        else:
            self.whitelist(url)

    def cache(self, url):
        """
        Cache file by URL
        """
        o = urlparse(url)
        assert o.netloc, "Excpected URL with hostname"


        # Retain hostname/path structure in cache
        cached_url = os.path.join("cache", o.netloc, unquote(o.path[1:]))
        cached_path = os.path.join(".moar/output", cached_url)
        if url in self.blacklist_set:
            raise self.LinkBroken(url)
        if not os.path.exists(cached_path):
            try:
                os.makedirs(os.path.dirname(cached_path))
            except OSError:
                pass

            req = urllib.request.Request(url, headers=self.HEADERS)
            try:
                with urllib.request.urlopen(req, None, 3) as ih:
                    print("Fetching:", url, "to", cached_path)
                    buf = ih.read()
                with open(cached_path + ".part", "wb") as oh:
                    oh.write(buf)
            except urllib.error.URLError:
                self._blacklist_append.write(url)
                self._blacklist_append.write("\n")
                self._blacklist_append.flush()
                self.blacklist(url)
                raise self.LinkBroken(url)
            else:
                assert os.stat(cached_path + ".part").st_size > 0, "File %s.part has size of 0" % cached_path
                os.rename(cached_path + ".part", cached_path)

            if url not in self.blacklist_set:
                self.whitelist(url)
        return cached_path, "/" + cached_url
        
    def whitelist(self, url):
        if url not in self.whitelist_set:
            self.whitelist_set.add(url)
            if not url.startswith("/"):
                self._whitelist_append.write(url + "\n")
                self._whitelist_append.flush()

    
    def blacklist(self, url):
        assert not url.startswith("/")
        if url not in self.blacklist_set:
            self._blacklist_append.write(url + "\n")
            self._blacklist_append.flush()
            self.blacklist_set.add(url)

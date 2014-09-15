#!/usr/bin/python3
# encoding: utf-8

import sys
import os
import re
import time
import codecs
import jinja2
import bisect
import socket
import unicodedata
import mimetypes
import configparser
import hashlib
import urllib
from urllib.parse import urlparse, unquote
from collections import Counter
from datetime import datetime
from docutils.core import publish_parts
from docutils.parsers.rst import directives
from functools import partial
from numpy import interp as interpolate
from lxml import etree
import svgz
import gzip
import base64
import colors

assert os.path.exists("templates/")
assert os.path.exists("output/"), "No directory 'output' in current directory"
assert os.path.exists("output/cache/"), "No directory 'output/cache' in current directory"
assert os.path.exists("posts/")
assert os.path.exists("pages/")

DEFAULT_AUTHOR = "Lauri Võsandi", "lauri.vosandi@gmail.com"

try:
    from langid import classify
except ImportError:
    print("Warning: failed to import langid, assuming English for unspecified posts")
    def classify(chunk):
        return "en", 1.0

def hash_url(url):
    if "//" in url:
        proto, url = url.split("//", 1)
    if "#" in url:
        url, fragment = url.split("#", 1)
    if url.endswith("/"):
        url += "index.html"
    basename, extension = os.path.splitext(url)
    return unicodedata.normalize('NFKD', basename) + extension


class Crawler(object):
    def __init__(self, cache, blacklist, whitelist):
        pass
        
    def cache(self, url):
        pass
        
    def exists(self, url):
        pass
        
    def whitelist(self, url):
        pass
    
    def blacklist(self, url):
        pass

class Site(object):
    def __init__(self, root, base=""):
        self.base = base
        self.root = root    
        self.tags = Counter()
        self.resources = dict()
        self.cache = os.path.join(root, "output", "cache") # For crawled URL-s
        self.output = os.path.join(root, "output")
        self.javascript = os.path.join(root, "js")
        self.stylesheets = os.path.join(root, "css")
        self.templates = jinja2.FileSystemLoader(os.path.join(root, "templates"))
        self.env = jinja2.Environment(loader=self.templates, extensions=['jinja2.ext.i18n'])
        self.feed = [] # Resources listed 
    
    def _list_stylesheets(self):
        for filename in sorted(os.listdir(self.stylesheets)):
            yield os.path.join(self.stylesheets, filename)
    
    def _list_javascript(self):
        for filename in sorted(os.listdir(self.javascript)):
            yield os.path.join(self.javascript, filename)
            
    def render_stylesheets(self, *args, **kwargs):
        for abspath in self._list_stylesheets():
            with open(abspath) as fh:
                buf = fh.read()
                buf = re.sub("\s*{\s*", "{", buf);
                buf = re.sub("\s*\/\*.*?\*\/\s*", "", buf, flags=re.DOTALL)
                buf = re.sub("^\s+", "", buf, flags=re.MULTILINE)
                buf = re.sub("\s*,\s*\n", ",", buf, flags=re.MULTILINE|re.DOTALL)
                buf = re.sub("\n\s*\n", "\n", buf, flags=re.DOTALL)
                buf = re.sub("\:\s+", ":", buf)
                buf = re.sub("\s*\;\s*", ";", buf)
                yield buf.encode("utf-8")
            
    def render_javascript(self, *args, **kwargs):
        for abspath in self._list_javascript():
            with open(abspath) as fh:
                buf = fh.read()
                buf = re.sub("\s*{\s*",             "{",  buf);
                buf = re.sub("\s*\/\*.*?\*\/\s*",   "",   buf, flags=re.DOTALL)
                buf = re.sub("^\s+",                "",   buf, flags=re.MULTILINE)
                buf = re.sub("\n\s*\n",             "\n", buf, flags=re.DOTALL)
                buf = re.sub("\:\s+",               ":",  buf)
                buf = re.sub("\s*\;\s*",            ";",  buf)
                buf = re.sub(" \/\/.*?$",           "",   buf, flags=re.MULTILINE)
                yield buf.encode("utf-8")
                
    def find_related(self):
        normalized_tags = {}
        for x in self.resources.values():
            normalized_tags[x] = set([j.lower() for j in x.tags])
            
        self.related = {}
        for x in self.resources.values():
            self.related[x] = Counter()
            for y in self.resources.values():
                if x == y: continue # Don't refer to itself
                i = len(normalized_tags[x].intersection(normalized_tags[y])) # Find intersecting tags
                if i >= 1: self.related[x][y] = i # Add only if there is shared tags
            
    def urls(self, debug=True):
        """
        Return generator for url to renderer function mappings
        """
        if debug:
            for filename in os.listdir("css"):
                yield "/css/" + filename, partial(self.render_file, "css/" + filename)
            for filename in os.listdir("js"):
                yield "/js/" + filename, partial(self.render_file, "js/" + filename)
        else:
            yield "/js/assets.js", self.render_javascript
            yield "/css/assets.css", self.render_stylesheets

        for filename in os.listdir("fonts"):
            yield "/fonts/" + filename, partial(self.render_file, "fonts/" + filename)

        
        for filename in os.listdir("img"):
            yield "/img/" + filename, partial(self.render_file, "img/" + filename)

        for filename in os.listdir("pages"):
            if filename.endswith(".jpg"):
                yield "/" + filename, partial(self.render_file, "pages/" + filename)
        yield "/rss.xml", self.render_rss
        yield "/atom.xml", self.render_atom
        yield "/search.html", self.render_search
        yield "/sitemap.xml", self.render_sitemap
        yield "/posts.html", self.render_post_list
        for url, resource in self.resources.items():
            yield url, partial(self.render_post, resource)

    def render_file(self, filename, *args, **kwargs):
        with open(os.path.join(self.root, filename), "rb") as fh:
            return fh.read()
        
    def serve(site, address, port):
        import string,cgi,time
        from os import curdir, sep
        from http.server import BaseHTTPRequestHandler, HTTPServer
        
        urls = dict(site.urls())
#        print("Serving %d URL-s" % len(urls))
        
        class MyHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path
                if path.endswith("/"): path += "index.html"
                
                if path.startswith("/cache/"):
                    self.send_response(200)
                    content_type, encoding = mimetypes.guess_type(path)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    with open(os.path.join(self.cache, path[7:]), "rb") as ih:
                        self.wfile.write(ih.read())
                else:
                    try:
                        renderer = urls[path]
                    except KeyError:
                        self.send_error(404, 'File Not Found: %s' % self.path)
                        return
                    
                    self.send_response(200)
                    content_type, encoding = mimetypes.guess_type(self.path)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    buf = renderer(base="/")
#                    for url, substitute in self.embedded_objects():
#                        o = urlparse(url)
#                        if not o.netloc:
#                            self.resources[url] = self.render_file(os.path.join(

                    if isinstance(buf, str) or isinstance(buf, bytes):
                        self.wfile.write(buf)
                    else:
                        for chunk in buf:
                            self.wfile.write(chunk)

        try:
            server = HTTPServer((address, port), MyHandler)
            print('Serving', root)
            server.serve_forever()
        except KeyboardInterrupt:
            print('Ctrl-C received, shutting down server')
            server.socket.close()
            sys.exit(255)

    def tag_cloud(self, count=100):
        m = site.tags.most_common(count)
        counts = [count for tag,count in m]
        return sorted([(tag,interpolate(count, (min(counts), max(counts)), (50, 150))) for (tag,count) in m], key=lambda l:l[0])

    @property
    def context(self):
        """
        Return general context
        """
        return {
            "now": datetime.now(),
            "language": "en",
            "site": self,
            "base": self.base,
            "javascript": [os.path.join("/js", j) for j in os.listdir(self.javascript)],
            "stylesheets": [os.path.join("/css", j) for j in os.listdir(self.stylesheets)]
        }

    def build(self):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
        accept = "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

        # Preload URL blacklist
        with open("blacklist.urls") as fh:
            blacklist = set(fh.read().split("\n"))
            
        # Preload URL whitelist
        with open("whitelist.urls") as fh:
            whitelist = set(fh.read().split("\n"))

        with open("blacklist.urls", "a") as bh, open("whitelist.urls", "a") as wh:
            for resource in self.resources.values():
                # Parse HTML representing the document
                resource.parse_tree()
                
                # Fetch referred images and SVG-s to cache
                for url, substitute in resource.embedded_objects():
                    if url in blacklist:
                        print("Not caching blacklisted URL:"+ url)
                        continue
                        
                    o = urlparse(url)
                    
                    if o.netloc:
                        cached_relpath = os.path.join(o.netloc, unquote(o.path[1:]))
                    else:
                        basename, extension = os.path.splitext(o.path)
                        assert not o.path.startswith("/")
                        abspath = os.path.join(os.path.dirname(resource.source), o.path)
                        
                        try:
                            with open(abspath, mode='rb') as ih, open("output/cache/unknown.part", "wb") as oh:
                                d = hashlib.md5()
                                while True:
                                    buf = ih.read(4096) # 128 is smaller than the typical filesystem block
                                    if not buf:
                                        break
                                    oh.write(buf)
                                    d.update(buf)
                            whitelist.add(url)
                        except IOError:
                            print(colors.RED + "Found broken link within site:"  + colors.NORMAL, url, "resolved to", abspath, "in", resource.source)
                            raise

                        cached_relpath = d.hexdigest() + extension
                        

                    cached_path = os.path.join("output", "cache", cached_relpath)

                    if not os.path.exists(cached_path):
                        try:
                            os.makedirs(os.path.dirname(cached_path))
                        except OSError:
                            pass

                        if o.netloc:
                            print("Fetching:", url, "to", cached_path)
                            req = urllib.request.Request(url, headers={'User-Agent': user_agent, "Accept":accept})
                            try:
                                with urllib.request.urlopen(req, None, 3) as ih:
                                    with open(cached_path + ".part", "wb") as oh:
                                        buf = ih.read()
                                        oh.write(buf)
                            except urllib.error.URLError:
                                print("Found broken link:"+ url)
                                bh.write(url)
                                bh.write("\n")
                                bh.flush()
                                blacklist.add(url)
                            else:
                                os.rename(cached_path + ".part", cached_path)

                            if url not in blacklist:
                                whitelist.add(url)
                        else:
                            os.rename("output/cache/unknown.part", cached_path)

                    if substitute and url in whitelist:
                        print("Substituting:", url, "with", "/cache/" + cached_relpath)
                        substitute(os.path.join("/cache", cached_relpath))

                # Check referred URL-s
                for element in resource.tree.findall(".//a"):
                    try:
                        url = element.attrib["href"]
                    except KeyError:
                        print("Found bogus link element")
                        continue

                    o = urlparse(url)
                    path = o.path
                    
                    if ":" in o.netloc:
                        hostname, port = o.netloc.split(":")
                    else:
                        hostname = o.netloc
                    
                    if o.scheme not in ("ftp", "http", "https", ""):
                        print(colors.YELLOW + "Ignoring unknown URL scheme:" + colors.NORMAL, url)
                        continue

                    if hostname == "localhost":
                        print(colors.RED + "Found bogus link to:" + colors.NORMAL, url)
                        continue
                        
                    if hostname:
                        if hostname.endswith(".google.com"):
                            continue
                        elif hostname.endswith(".ebay.com"):
                            continue

                        if url in whitelist:
                            continue
                        if url in blacklist:
                            print(colors.YELLOW + "Document refers to blacklisted URL:" + colors.NORMAL, url, "in", resource)
                            continue

                        print("Crawling:", url)
                        req = urllib.request.Request(url, headers={'User-Agent': user_agent, "Accept":accept})
                        try:
                            with urllib.request.urlopen(req, None, 3) as ih:
                                with open(cached_path, "wb") as oh:
                                    ih.read(1024)
                        except (urllib.error.URLError, socket.timeout):
                            print("Found broken link:"+ url)
                            bh.write(url)
                            bh.write("\n")
                            bh.flush()
                            blacklist.add(url)
                        else:
                            wh.write(url)
                            wh.write("\n")
                            wh.flush()
                            whitelist.add(url)
                            
                    # URL is relative to document
                    else:
                        # Ignore anchors within page
                        if not path: continue
                            
                        if not path.startswith("/"):
                            path = os.path.join(os.path.dirname(resource.url), path)
                            
                        if path not in self.resources.keys():
                            print(colors.RED + "Found broken link within site:"  + colors.NORMAL, url, "resolved to", path)

        for url, renderer in self.urls(debug=False):
            abspath = os.path.join(self.output, url[1:])
            try:
                os.makedirs(os.path.dirname(abspath))
            except OSError:
                pass
            with open(abspath, "wb") as fh:
                with gzip.open(abspath + ".gz", "wb") as gh:
                    buf = renderer(debug=False, javascript=["/js/assets.js"], stylesheets=["/css/assets.css"])
                    if isinstance(buf, str) or isinstance(buf, bytes):
                        buf = buf
                        fh.write(buf)
                        gh.write(buf)
                    else:
                        for chunk in buf:
                            chunk = chunk
                            fh.write(chunk)
                            gh.write(chunk)

    def render_sitemap(self, *args, **kwargs):
        ctx = self.context
        ctx.update(resources=self.resources)
        ctx.update(kwargs)
        return self.env.get_template("sitemap.xml").render(ctx).encode("utf-8")
    
    def render_post_list(self, *args, **kwargs):
        ctx = self.context
        ctx.update(posts=filter(lambda p: not p.flags.intersection(set(["hidden", "no-archive"])), self.feed))
        ctx.update(kwargs)
        return self.env.get_template("post_list.html").render(ctx).encode("utf-8")
        
    def render_search(self, *args, **kwargs):
        ctx = self.context
        resources = self.resources.values()
        resources = filter(lambda r: not r.flags.intersection(set(["hidden", "no-search"])), resources)
        resources = sorted(resources, key=lambda r:r.revised)
        resources = reversed(resources)
        ctx.update(resources=resources)
        ctx.update(kwargs)
        return self.env.get_template("search.html").render(ctx).encode("utf-8")

        
    def render_post(self, post, *args, **kwargs):
        ctx = self.context
        if "no-related" not in post.flags:
            ctx["related_posts"]=self.related[post].most_common(5)
        ctx.update(
            post=post,
            language=post.language,
            revised=post.revised,
            document=post.render(*args, **kwargs))
        ctx.update(kwargs)
        return self.env.get_template(post.template).render(ctx).encode("utf-8")

    def render_rss(self, *args, **kwargs):
        ctx = self.context
        posts = filter(lambda p: not p.flags.intersection(set(["hidden", "no-feed"])), self.feed)
        posts = sorted(posts)
        posts = posts[-10:]
        posts = reversed(posts)
        ctx.update(posts=posts)
        ctx.update(kwargs)
        return self.env.get_template("rss.xml").render(ctx).encode("utf-8")
        
    def render_atom(self, *args, **kwargs):
        ctx = self.context
        posts = filter(lambda p: not p.flags.intersection(set(["hidden", "no-feed"])), self.feed)
        posts = sorted(posts)
        posts = posts[-10:]
        posts = reversed(posts)
        ctx.update(posts=posts)
        ctx.update(kwargs)
        return self.env.get_template("atom.xml").render(ctx).encode("utf-8")
        
    def add(self, resource):
        if "hidden" not in resource.flags:
            self.tags.update(resource.tags)
        self.resources[resource.url] = resource
        if resource.published:
            bisect.insort(self.feed, resource)

    def __repr__(self):
        return "Site %s at %s" % (self.root, self.base)



from youtube import Youtube
from chart import Chart
#from fritzing import Breadboard, Schematic

directives.register_directive('youtube', Youtube)
directives.register_directive('chart', Chart)

class Page(object):
    changefreq = "weekly"
    
    def __init__(self, root, directory, filename, template="page.html"):
        basename, self.extension = os.path.splitext(filename)
        self.root = root
        self.slug = basename.lower()
        self.source = os.path.join(root, directory, filename)
        self.tree = None
        self.directory = directory
        self.authors = set()
        self.tags = set()
        self.word_count = 0
        
        # Post can have various flags

        # no-sidebar - Hide sidebar in the post
        # no-feed - Hide post in RSS feed
        # no-archive - Hide post in archive
        
        self.flags = set()
        self.revised = datetime.fromtimestamp(os.stat(self.source).st_mtime)
        self.published = None
#        self.published = datetime.fromtimestamp(os.stat(self.source).st_ctime)
        self.title = None
        self.template = "post.html"
        self.language = None
        self.refers = set() # URL-s this page refers tou        
        self.parse_headers()
        self.parse_content() # Keywords, language
        assert self.authors, "No author specified or autofilled for %s"  % self.source

    def __eq__(self, other):
        return self.source == other.source
        
    def __gt__(self, other):
        return self.published > other.published

    def __lt__(self, other):
        return self.published < other.published

    def __repr__(self):
        return self.title or "Untitled post at %s" % self.url
        
    def __hash__(self):
        return hash(self.url)
        
    def resolve(self, path):
        if path.startswith("/") or "//" in path:
            return path
        return os.path.join(self.root, self.directory, path)
        
    @property
    def url(self):
        url = "%s.html" % self.slug
        if self.directory != ".":
            url = os.path.join(self.directory, url)
        if self.language != "en":
            url = os.path.join(self.language, url)
        return "/" + url        

    def parse_headers(self):
        with open(self.source, encoding="utf-8") as fh:
            self._content_offset = 0 # fh.tell() lies because for line in fh has read-ahead buffer
            while True:
                line = fh.readline()
                if not line: # End of file
                    print("Warning: no body in file %s" % self.source)
                    break

                self._content_offset += len(line.encode("utf-8"))

                m = re.match("\.\. +(?P<key>\w+)\:\s*(?P<value>.+)$", line)
                if not m: # Headers ended
                    break
                key, value = m.groups()
                if key == "tags":
                    self.tags = set([j.strip() for j in re.split("\s*,\s*", value)])
                elif key in "language":
                    self.language = value
                elif key == "template":
                    self.template = value
                elif key == "author":
                    m = re.match("(.+?)\s*(\<(.+?)\>)?$", value)
                    name, _, email = m.groups()
                    self.authors.add((name, email))
                elif key == "flags":
                    self.flags = set([j.strip() for j in re.split("\s*,\s*", value)])
                elif key == "date" or key == "published":
                    try:
                        self.published = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        self.published = datetime.strptime(value, "%Y-%m-%d")
                elif key == "title":
                    self.title = value
                continue

        if not self.authors:
            self.authors.add(DEFAULT_AUTHOR)
            
    def read_content(self):
        with open(self.source) as fh:
            fh.seek(self._content_offset)
            return fh.read()
            
    def first_paragraph(self):
        for element in self.tree.findall(".//p"):
            return etree.tostring(element).decode("utf-8")[3:-5]
        
    def parse_content(self):
        content = []
        ignore = False
        self.word_count = 0
        self.keywords = Counter()
        self.keywords.update([tag.lower() for tag in self.tags])
        with open(self.source) as fh:
            fh.seek(self._content_offset)
            while True:
                line = fh.readline()
                if not line:
                    break
                if line.startswith("=="):
                    continue
                if line.startswith("~~"):
                    continue
                if line.startswith("\n"):
                    continue
                    
                normalized = unicodedata.normalize('NFKD', line)
                words = [x for x in re.split("[^\w\d]+", normalized.lower()) if lambda x:len(x)>=3]
                self.word_count += len(words)

                if not self.title:
                    self.title = line.strip()
                if line.startswith(" "):
                    ignore = False
                if line.startswith("code::"):
                    ignore = True
                if line.startswith(" ") and ignore:
                    continue
                
                self.keywords.update(words)
            
        # Detect language
        if not self.language:
            self.language, score = classify(self.keywords)

    def parse_tree(self):
        """
        Parse HTML
        """
        # Parse the HTML chunk
        parser = etree.HTMLParser()
        if self.extension == ".rst":
            print("Rendering", self.source)
            with codecs.open(self.source, encoding="utf-8") as fh:
                fh.seek(self._content_offset)
                buf = fh.read()
                parts = publish_parts(
                     buf,
                     writer_name='html',
                     settings_overrides={
                        'stylesheet_path': None,
                        'link_stylesheet': True,
                        'syntax_highlight': 'short',
                        'math_output': 'mathjax',
                     })
                partial = parts["whole"].encode("utf-8")
                self.tree = etree.fromstring(partial, parser)
        else:
            self.tree = etree.parse(self.source, parser)
            
        if "outdated" in self.flags:
            notice = etree.Element("p")
            notice.attrib["class"] = "last"
            notice.text = "This post is outdated"
            container = etree.Element("div")
            container.attrib["class"] = "important"
            container.append(notice)
            document = self.tree.find(".//div")
            document.insert(1, container)

        if self.published:            
            date = etree.Element("span")
            date.attrib["class"] = "published"
            date.text = self.published.strftime("%d. %b '%y")
            document = self.tree.find(".//div")
            document.insert(0, date)
            
    def referred_urls(self):
        """
        Find URL-s referred by this post
        """
        if "outdated" not in self.tags:
            for e in self.tree.findall(".//a"):
                try:
                    yield e.attrib["href"]
                except KeyError:
                    print("Found bogus link element")

        for url, substitute in self.embedded_objects():
            yield url
            
    def embedded_objects(self):
        """
        Extract URL-s and URL substitutor functions of objects embedded in the document
        """
        def set_attribute(element, attribute, value):
            element.attrib[attribute] = value

        # Find images  
        for e in self.tree.findall(".//img"):
            url = e.attrib["src"]
            o = urlparse(url)
            if o.path.endswith(".svg") or o.path.endswith(".svgz"):
                raise Exception("Use object tag for SVG images")
                
            basename, extension = os.path.splitext(o.path)
            if extension.lower() in (".png", ".gif", ".jpeg", ".jpg"):
                yield url, partial(set_attribute, e, "src")
            else:
                raise Exception("Bogus image tag in %s, referring to %s" % (self.source, url))

        # Inline SVG-s
        for e in self.tree.findall(".//object[@type='image/svg+xml']"):
            o = urlparse(e.attrib["data"])
            if o.netloc:
                yield e.attrib["data"], partial(set_attribute, e, "data")
                continue

            if o.path.startswith("/cache/"):
                tree = svgz.parse("output" + o.path)
            else:
                tree = svgz.parse(os.path.join(os.path.dirname(self.source), o.path))
                
            root = tree.getroot()
            root.attrib["id"] = o.path
            parent = e.getparent()
            parent.insert(0, root) # This works out fine for .. figure but might fail elsewhere
            parent.remove(e)

    def render(self, *args, **kwargs):
        if not self.tree:
            self.parse_tree()
        return etree.tostring(self.tree.find("body/")).decode("utf-8")

class Post(Page):
    changefreq = "never"
    
    def __init__(self, *args, **kwargs):
        if "template" not in kwargs:
            kwargs["template"] = "post.html"
        Page.__init__(self, *args, **kwargs)
    
    @property
    def url(self):
        url = "%04d/%02d/%s.html" % (self.published.year, self.published.month, self.slug)
        if self.language != "en":
            url = os.path.join(self.language, url)
        return "/" + url


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--serve",
                      action="store_true", dest="serve", default=False,
                      help="Run built-in (insecure!) server")
    parser.add_option("-p", "--port",
                      action="store_true", dest="port", default=8080,
                      help="Port to bind")
    parser.add_option("-a", "--address",
                      dest="address", default="localhost",
                      help="Address to bind")

    options, args = parser.parse_args()

    root = os.getcwd()
    while root != "/":
        path = os.path.join(root, ".moar", "blog.ini")
        if os.path.exists(path):
            break
        root = os.path.dirname(root)
    else:
        print("Did not find .moar/blog.ini")
        sys.exit(255)

    site = Site(root, "http://lauri.vosandi.com")
   
    posts_root = os.path.join(root, "pages")
    for directory, dirs, files in os.walk(posts_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.startswith("README."):
                continue
            if filename.endswith(".rst"):
                post = Page(posts_root, os.path.relpath(directory, posts_root), filename)
                site.add(post)

    posts_root = os.path.join(root, "posts")
    for directory, dirs, files in os.walk(posts_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        run_fritzing = False
        for filename in files:
            if filename.startswith("README"):
                continue
            if filename.endswith(".fz") or filename.endswith(".fzz"):
                run_fritzing = True
            elif filename.endswith(".rst"):
                post = Post(posts_root, os.path.relpath(directory, posts_root), filename)

                if post.published:
                    site.add(post)
                else:
                    raise "No publishing date specified: %s" % post
            

        if run_fritzing:
            cmd = "Fritzing", "-svg", directory
            print("Would run:", cmd)

    # Find related posts
    site.find_related()

    if options.serve:
        site.serve(options.address, options.port)
    else:
        site.build()


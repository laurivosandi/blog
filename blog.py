#!/usr/bin/python3
# encoding: utf-8

# pip3 install jinja2 docutils numpy pygal langid==1.1.4dev

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
from urllib.parse import urlparse, unquote
from collections import Counter
from datetime import datetime
from docutils.core import publish_parts
from docutils import io
from docutils.parsers.rst import directives
from functools import partial
from numpy import interp as interpolate
from lxml import etree
from subprocess import call
from optparse import OptionParser
from crawler import Crawler
import pygments
import svgz
import gzip
import base64
import colors

parser = OptionParser()
parser.add_option("-r", "--root",
    dest="root",
    default=".",
    help="Root of the site source")
parser.add_option("-s", "--serve",
    action="store_true",
    dest="serve",
    default=False,
    help="Run built-in (insecure!) server")
parser.add_option("-p", "--port",
    action="store_true",
    dest="port",
    default=8080,
    help="Port to bind")
parser.add_option("-a", "--address",
    dest="address",
    default="localhost",
    help="Address to bind")
    
options, args = parser.parse_args()

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(options.root, "templates")),
    extensions=['jinja2.ext.i18n'])

assert os.path.exists(os.path.join(options.root, "templates/"))
assert os.path.exists(".moar/output/"), "No directory 'output' in current directory"
assert os.path.exists(".moar/output/cache/"), "No directory 'output/cache' in current directory"
assert os.path.exists("posts/")
assert os.path.exists("pages/")

HTML_REDIRECT = """<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1;url=%(url)s">
        <script type="text/javascript">
            window.location.href = "%(url)s"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow the <a href="%(url)s">link</a>
    </body>
</html>
"""

#class Report(object):
#    def __init__(self, path):
        
        

DEFAULT_AUTHOR = "Lauri Võsandi", "lauri.vosandi@gmail.com"

try:
    from langid import classify
except ImportError:
    print("Warning: failed to import langid, assuming English for unspecified posts")
    def classify(chunk):
        return "en", 1.0
        
class IsFresh(Exception):
    pass

class Site(object):
    def __init__(self, root, base=""):
        self.base = base
        self.root = root    
        self.tags = Counter()
        self.resources = dict() # URL -> Page instance
        self.renderers = dict() # URL -> function

        self.cache = os.path.join(root, ".moar", "output", "cache") # For crawled URL-s
        self.crawler = Crawler(
            os.path.join(root, ".moar", "output", "cache"), 
            os.path.join(root, "blacklist.urls"),
            os.path.join(root, "whitelist.urls"))
        self.output = os.path.join(root, ".moar", "output")
        self.javascript = os.path.join(root, "js")
        self.stylesheets = os.path.join(root, "css")
        self.feed = [] # Resources listed 

    def _list_stylesheets(self):
        for filename in sorted(os.listdir(self.stylesheets)):
            yield os.path.join(self.stylesheets, filename)
    
    def _list_javascript(self):
        for filename in sorted(os.listdir(self.javascript)):
            yield os.path.join(self.javascript, filename)

    def render_javascript_bundle(self, *args, **kwargs):
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

    def render_stylesheet_bundle(self, *args, **kwargs):
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

    def add_post(self, resource):
        if "hidden" not in resource.flags:
            self.tags.update(resource.tags)
        self.resources[resource.url] = resource
        self.renderers[resource.url] = partial(self.render_post, post)
        if resource.published:
            bisect.insort(self.feed, resource)


    def add_renderer(self, url, renderer):
        self.renderers[url] = renderer

    def add_static(self, source, dest=None):
        def render_file(filename, *args, **kwargs):
            with open(os.path.join(self.root, filename), "rb") as fh:
                return fh.read()
        assert os.path.exists(source), "Path does not exist %s" % source
        url = "/" + source
        if dest:
            url = dest
        print("Mounting", source, "at", url)
        self.renderers[url] = partial(render_file, source)

                
    def find_related(self):
        normalized_tags = {}
        for x in self.resources.values():
            normalized_tags[x] = set([j.lower() for j in x.tags])
        assert self.resources, "No resources!"
        self.related = {}
        for x in self.resources.values():
            self.related[x] = Counter()
            for y in self.resources.values():
                if x == y: continue # Don't refer to itself
                i = len(normalized_tags[x].intersection(normalized_tags[y])) # Find intersecting tags
                if i >= 1: self.related[x][y] = i # Add only if there is shared tags

    def serve(site, address, port):
        import string,cgi,time
        from os import curdir, sep
        from http.server import BaseHTTPRequestHandler, HTTPServer
        
        print("Starting up buit-in server")
        print("Serving %d URL-s" % len(site.renderers))
        
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
                        renderer = site.renderers[path]
                    except KeyError:
                        self.send_error(404, 'File Not Found: %s' % self.path)
                        return
                    else:
                    
                        self.send_response(200)
                        content_type, encoding = mimetypes.guess_type(self.path)
                        self.send_header('Content-type', content_type)

                        self.end_headers()

                        try:
                            resource = site.resources[path]
                        except KeyError:
                            pass
                        else:
                            resource.parse_tree()
                            for url, substitute in resource.embedded_objects():
                                o = urlparse(url)
                                if not o.netloc:
                                    site.add_static(os.path.join(os.path.dirname(resource.source), o.path), os.path.join(os.path.dirname(path), o.path))
                            resource.inline_svgs()

                        buf = renderer(base="/")

                        if isinstance(buf, str) or isinstance(buf, bytes):
                            self.wfile.write(buf)
                        else:
                            for chunk in buf:
                                self.wfile.write(chunk)

        try:
            server = HTTPServer((address, port), MyHandler)
            print('Serving', options.root)
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
        
    def stash(self, abspath):
        size = os.stat(abspath).st_size
        assert size > 0, "Source file size zero %s" % abspath
        basename, extension = os.path.splitext(abspath)

        with open(abspath, mode='rb') as ih:
            d = hashlib.md5()
            while True:
                buf = ih.read(4096)
                if not buf:
                    break
                d.update(buf)

        cached_relpath = d.hexdigest() + extension
        cached_path = os.path.join(".moar", "output", "cache", cached_relpath)
        if not os.path.exists(cached_path):
            print("Caching local file", abspath, "to", cached_path)
            cmd = "/bin/cp", "--reflink=auto", abspath, cached_path + ".part"
            call(cmd)
            assert os.stat(cached_path + ".part").st_size == size, "Reflinked file size differs %s.part" % cached_path
            os.rename(cached_path + ".part", cached_path)
            assert os.stat(cached_path).st_size != 0, "Renamed file size zero %s" % cached_path
        return cached_path, os.path.join("/cache", cached_relpath)

    def build(self):
        for resource in self.resources.values():
            # Parse HTML representing the document
            resource.parse_tree()
                
            # Fetch referred images and SVG-s to cache
            for url, substitute in resource.embedded_objects():
                if url in self.crawler.blacklist_set:
                    print("Not caching blacklisted URL:"+ url)
                    continue
                        
                o = urlparse(url)
                
                if o.netloc:
                    try:
                        cached_abspath, cached_url = self.crawler.cache(url)
                    except self.crawler.LinkBroken:
                        print("Found broken link to external URL:", url, "in file", resource.source)
                else:
                    # Resolve URL to absolute file path and absolute URL path
                    abspath, url = resource.resolve(o.path)
                    try:
                        cached_abspath, cached_url = self.stash(abspath)
                        self.crawler.whitelist(url)
                    except (IOError, OSError):
                        print(colors.RED + "Found broken link within site:"  + colors.NORMAL, url, "resolved to", abspath, "which does not exist, referred by", resource)
                        exit(255)

                if substitute and url in self.crawler.whitelist_set:
#                    print("Substituting:", url, "with", cached_url)
                    substitute(cached_url)

                assert os.stat(cached_abspath).st_size > 0, "File %s has size of 0" % cached_abspath
                
            # Inline SVG-s        
            resource.inline_svgs()
            
            # Check referred URL-s
            for element in resource.tree.findall(".//a"):
                try:
                    url = element.attrib["href"]
                except KeyError:
                    print("Found bogus link element in", resource.source)
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

                    if url in self.crawler.whitelist_set:
                        continue
                    if url in self.crawler.blacklist_set:
                        print(colors.YELLOW + "Document refers to blacklisted URL:" + colors.NORMAL, url, "in", resource.source)
                        # TODO: Why this does not work?
                        element.set("class", element.get("class", "") + " broken")
#                        print(element.attrib)
                        continue

                    try:
                        self.crawler.check(url)
                    except self.crawler.LinkBroken:
                        print(colors.RED + "Found broken link to" + colors.NORMAL, url, "in", resource.source)
                        continue
                        
                # URL is relative to document
                else:
                    # Ignore anchors within page
                    if not path: continue
                                            
                    if not path.startswith("/"):
                        path = os.path.join(os.path.dirname(resource.url), path)


                    if o.fragment == "TODO":
                        # TODO: Create placeholder page with donate button
                        continue
                     
                    if path.endswith("/"):
                        path += "index.html"

                    if path not in self.renderers.keys():
                        print(colors.RED + "Found broken link within site:"  + colors.NORMAL, url, "resolved to", path, "referred by", resource.source)
                        exit(255)
                        
        for url, renderer in self.renderers.items():
            abspath = os.path.join(self.output, url[1:])
            try:
                print("Creating dir:", abspath)
                os.makedirs(os.path.dirname(abspath))
            except OSError:
                pass
            try:
                buf = renderer(debug=False, javascript=["/js/assets.js"], stylesheets=["/css/assets.css"], if_newer=os.stat(abspath).st_mtime if os.path.exists(abspath) else 0)
            except IsFresh:
                continue
            with open(abspath, "wb") as fh:
                with gzip.open(abspath + ".gz", "wb") as gh:
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
        return environment.get_template("sitemap.xml").render(ctx).encode("utf-8")
    
    def render_post_list(self, *args, **kwargs):
        ctx = self.context
        ctx.update(posts=filter(lambda p: not p.flags.intersection(set(["hidden", "no-archive"])), self.feed))
        ctx.update(kwargs)
        return environment.get_template("post_list.html").render(ctx).encode("utf-8")
        
    def render_search(self, *args, **kwargs):
        ctx = self.context
        resources = self.resources.values()
        resources = filter(lambda r: not r.flags.intersection(set(["hidden", "no-search"])), resources)
        resources = sorted(resources, key=lambda r:r.published if r.published else r.revised)
        resources = reversed(resources)
        ctx.update(resources=resources)
        ctx.update(kwargs)
        return environment.get_template("search.html").render(ctx).encode("utf-8")

        
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
        return environment.get_template(post.template).render(ctx).encode("utf-8")

    def render_robots(self, *args, **kwargs):
        return b"User-agent: *\nDisallow:\n"

    def render_rss(self, *args, **kwargs):
        ctx = self.context
        posts = filter(lambda p: not p.flags.intersection(set(["hidden", "no-feed"])), self.feed)
        posts = sorted(posts)
        posts = posts[-30:]
        posts = reversed(posts)
        ctx.update(posts=posts)
        ctx.update(kwargs)
        return environment.get_template("rss.xml").render(ctx).encode("utf-8")
        
    def render_atom(self, *args, **kwargs):
        ctx = self.context
        posts = filter(lambda p: not p.flags.intersection(set(["hidden", "no-feed"])), self.feed)
        posts = sorted(posts)
        posts = posts[-30:]
        posts = reversed(posts)
        ctx.update(posts=posts)
        ctx.update(kwargs)
        return environment.get_template("atom.xml").render(ctx).encode("utf-8")



from youtube import Youtube
from chart import Chart
from listing import Listing
#from fritzing import Breadboard, Schematic

directives.register_directive('listing', Listing)
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
        self.redirects = set()
        
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
        
    def resolve(self, related):
        """
        Stash file referred by the document to the cache
        """
        # If it's a local file, hash it and put it to cache
        assert not related.startswith("/"), "Don't know how to resolve absolute path on a page"
        assert not "//" in related, "Page is unaware of absolute URL-s"

        # Derive referred absolute path
        return os.path.join(os.path.dirname(self.source), related), os.path.join(os.path.dirname(self.url), related)
        
    @property
    def url(self):
        url = "%s.html" % self.slug
        if self.directory != ".":
            url = os.path.join(self.directory, url)
#        if self.language != "en":
#            url = os.path.join(self.language, url)
        return "/" + url        

    def parse_headers(self):
        if self.source.endswith(".rst"):
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
                    elif key == "redirect_from":
                        self.redirects.add(value)
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
        elif self.source.endswith(".html"):
            if not self.tree:
                self.parse_tree()
            self.title = self.tree.find("head").find("title").text
#            raise
#                try:
#                    yield e.attrib["href"]
#                except KeyError:
#                    print("Found bogus link element in", self.source)

            

        if not self.authors:
            self.authors.add(DEFAULT_AUTHOR)
            
    def read_content(self):
        with open(self.source) as fh:
            fh.seek(self._content_offset)
            return fh.read()
            
    def first_paragraph(self):
        if not self.tree:
            self.parse_tree()
        for element in self.tree.findall(".//p"):
            return etree.tostring(element).decode("utf-8")[3:-5]
        
    def parse_content(self):
        content = []
        ignore = False
        self.word_count = 0
        self.keywords = Counter()
        if not self.source.endswith(".rst"):
            self.language = "en"
            return
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
#            print("Parsing", self.source)
            parts = publish_parts(
                source=None,
                source_class = io.FileInput,
                source_path=self.source,
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
            partial = open(self.source).read()
            self.tree = etree.parse(self.source, parser)
#            for j in self.tree.find("//body"):
#                print(j)
#            raise
            
        if "outdated" in self.flags:
            notice = etree.Element("p")
            notice.attrib["class"] = "last"
            notice.text = "This post is outdated"
            container = etree.Element("div")
            container.attrib["class"] = "important"
            container.append(notice)
            document = self.tree.find(".//div")
            document.insert(1, container)
            
        title_element = self.tree.find(".//h1")
#        if not title_element:
#            print(partial)
#            print(self.source)
#            print(title_element,self.tree.find("h1"),self.tree.find(".//h1"),self.tree.find("./h1"),self.tree.find("//h1"))
#            raise
        try:
            title_element.getparent().remove(title_element)
        except AttributeError:
            print(self.source)
            raise

#        if self.published:
#            date = etree.Element("span")
#            date.attrib["class"] = "published"
#            date.text = self.published.strftime("%d. %b '%y")
#            document = self.tree.find(".//div")
#            document.insert(0, date)
            
    def referred_urls(self):
        """
        Find URL-s referred by this post
        """
        if "outdated" not in self.tags:
            for e in self.tree.findall(".//a"):
                try:
                    yield e.attrib["href"]
                except KeyError:
                    print("Found bogus link element in", self.source)

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
            try:
                url = e.attrib["src"]
            except KeyError:
                continue
            o = urlparse(url)
            if o.path.endswith(".svg") or o.path.endswith(".svgz"):
                raise Exception("Use <object type=\"image/svg+xml\" data=\"%s\"/> for SVG image" % url)
                
            basename, extension = os.path.splitext(o.path)
            if extension.lower() in (".png", ".gif", ".jpeg", ".jpg"):
                yield url, partial(set_attribute, e, "src")
            else:
                raise Exception("Found bogus image tag in %s, referring to %s" % (self.source, url))

        # SVG-s
        for e in self.tree.findall(".//object[@type='image/svg+xml']"):
            o = urlparse(e.attrib["data"])
            if o.netloc:
                yield e.attrib["data"], partial(set_attribute, e, "data")

    def inline_svgs(self):
        for e in self.tree.findall(".//object[@type='image/svg+xml']"):
            o = urlparse(e.attrib["data"])
            if o.path.startswith("/cache/"):
                path = ".moar/output" + o.path
#                print("Inlining cached SVG file:", path)
            else:
                path = os.path.join(os.path.dirname(self.source), o.path)
#                print("Inlining local SVG file:", path)
            assert os.path.exists(path), "Path %s does not exist" % path
            tree = svgz.parse(path)
                
            root = tree.getroot()
            root.attrib["style"] = e.attrib.get("style", "")
            parent = e.getparent()

            parent.insert(0, root) # This works out fine for .. figure but might fail elsewhere
            parent.remove(e)

    def render(self, *args, **kwargs):
        if "if_newer" in kwargs and os.stat(self.source).st_mtime <= kwargs["if_newer"]:
            raise IsFresh()
        if not self.tree:
            self.parse_tree()
        return self._render()

    def render_redirect(self, *args, **kwargs):
        return (HTML_REDIRECT % {"url":self.url}).encode("utf-8")
        
    def _render(self):
        buf = etree.tostring(self.tree.find("body/")).decode("utf-8")

        # Nasty hack to inline JavaScript from HTML articles
        def replacer(m):
            relpath, = m.groups()
            with open(os.path.join(os.path.dirname(self.source), relpath)) as fh:
                return ">" + fh.read() + "\n</script>\n"

        buf = re.sub("src=\"(?P<relpath>.+?\.js)\"/>", replacer, buf)
        return buf

class Post(Page):
    changefreq = "never"
    
    def __init__(self, *args, **kwargs):
        if "template" not in kwargs:
            kwargs["template"] = "post.html"
        Page.__init__(self, *args, **kwargs)
    
    @property
    def url(self):
        url = "%04d/%02d/%s.html" % (self.published.year, self.published.month, self.slug)
#        if self.language != "en":
#            url = os.path.join(self.language, url)
        return "/" + url




site = Site(options.root, "http://lauri.vosandi.com")
site.add_renderer("/robots.txt", site.render_robots)
site.add_renderer("/rss.xml", site.render_rss)
site.add_renderer("/atom.xml", site.render_atom)
site.add_renderer("/search.html", site.render_search)
site.add_renderer("/posts.html", site.render_post_list)

for filename in os.listdir("fonts"):
    site.add_static("fonts/" + filename)
for filename in os.listdir("img"):
    site.add_static("img/" + filename)

stylesheets = ["css/" + j for j in os.listdir("css")]
javascript = ["js/" + j for j in os.listdir("js")]
if options.serve:
    for filename in stylesheets:
        site.add_static(filename)
    for filename in javascript:
        site.add_static(filename)
else:
    site.add_renderer("/js/assets.js", site.render_javascript_bundle)
    site.add_renderer("/css/assets.css", site.render_stylesheet_bundle)

posts_root = os.path.join(options.root, "pages")
for directory, dirs, files in os.walk(posts_root):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for filename in files:
        if filename.endswith(".rst") or filename.endswith(".html"):

            post = Page(posts_root, os.path.relpath(directory, posts_root), filename)
            print("Mounting:", posts_root, os.path.relpath(directory, posts_root), filename, "at", post.url)
            if filename.startswith("README."):
                post.flags.add("hidden")

            site.add_post(post)

            for url in post.redirects:
                print("Adding redirect from %s to %s" % (url, post.url))
                site.add_renderer(url, post.render_redirect)

posts_root = os.path.join(options.root, "posts")
for directory, dirs, files in os.walk(posts_root):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    run_fritzing = False
    for filename in files:
        if filename.endswith(".fz") or filename.endswith(".fzz"):
            run_fritzing = True
        elif filename.endswith(".rst"):
            post = Post(posts_root, os.path.relpath(directory, posts_root), filename)
            if filename.startswith("README."):
                post.flags.add("hidden")

            if post.published:
                site.add_post(post)
            else:
                raise Exception("No publishing date specified: %s in %s" % (filename, directory))
        

    if run_fritzing:
        cmd = "Fritzing", "-svg", directory
        print("Would run:", cmd)

# Find related posts
site.find_related()
site.add_renderer("/sitemap.xml", site.render_sitemap)

if options.serve:
    site.serve(options.address, options.port)
else:
    site.build()
#        os.system("rsync -e ssh -avz .moar/output/ root@nas.koodur.com:/var/www/lauri.vosandi.com/ --exclude='*.part'")
#        os.system("rsync -e ssh -avz .moar/output/ lauri@www.koodur.com:/var/www/lauri.vosandi.com/ --exclude='*.part' --exclude='mod.tar'")
    os.system("rsync -e ssh -avz .moar/output/ lauri@www.koodur.com:/var/www/lauri.vosandi.com/ --exclude='*.part'")
post

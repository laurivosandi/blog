.. title: Convert WordPress posts to reStructedText
.. date: 2013-06-30
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Python, Wordpress

Convert WordPress posts to reStructedText
=========================================

WordPress has become pretty bloated so I thought what the hell, I could just
serve my blogposts from my own web framework. I had WordPress export my blogposts
to JSON and I used following regular expression spaghetti to reformat all the 
posts to reStructuredText:

.. code:: python

    import re
    import codecs
    from cjson import decode

    """
    Convert WordPress exported posts JSON to separate reStructuredText files
    """

    fh = open("wp_posts.json")
    buf = fh.read().decode("utf-8")

    posts = decode(buf[98:]) # Skip headers
    for post in posts:
        if post["post_type"] != "post" or post["post_status"] != "publish":
            continue
            
        created = post["post_date_gmt"]
        date = created[:10]
        title = post["post_title"]
        author = post["post_author"]
        
        # Sanitize filename
        filename = "%s-%s.rst" % (date, title.replace("/", "_").replace(" ", "_").replace(".", "_").lower())
        
        # Replace DOS newlines
        content = post["post_content"].replace("\r\n", "\n").replace("\r", "")
        
        # Replace HTML entities
        content = content.replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<").replace("&and;", "&")
        content = content.replace("\\'", "'")
        
        # Replace bold and italic tags
        content = re.sub(r"<strong>(.*?)</strong>", "**\\1**", content)
        content = re.sub(r"<em>(.*?)</em>", "*\\1*", content)
        content = re.sub(r"<b>(.*?)</b>", "**\\1**", content)
        content = re.sub(r"<i>(.*?)</i>", "*\\1*", content)
        
        # Replace links and images
        content = re.sub(r"<a href=\"(.+?)\"><img .*?src=\"(.+?)\".*?/></a>", "\n.. image:: \\2\n", content)
        content = re.sub(r"<a href=\"(.+?)\">(.+?)</a>", "`\\2 <\\1>`_ ", content)
        content = re.sub(r"<img .*?src=\"(.+?)\".*?>", "\n.. image: \\1\n", content)
        
        # Replace headings
        def underline(m):
            fragment, = m.groups()
            return "%s\n%s\n" % (fragment, "-" * len(fragment))
        content = re.sub(r"<h[123456]>(.*?)</h[123456]>", underline, content, flags=re.DOTALL)
        
        # Replace <code> tags and indent code
        def indent_code_block(m):
            code_block, = m.groups()
            return ":\n\n.. code:: bash\n\n   " + code_block.replace("\n", "\n   ").strip() + "\n\n"
        content = re.sub(r"</code>\s*<code>", "\n", content)
        content = re.sub(r":?\n?\s*<code>(.*?)</code>\s*", indent_code_block, content, flags=re.DOTALL)
        content = re.sub(r":?\n?\s*<pre>(.*?)</pre>\s*", indent_code_block, content, flags=re.DOTALL)
        
        # Replace lists
        def replace_list_items(m):
            chunk, = m.groups()
            return "\n%s\n" % re.sub("\s*<li>\s*(.*?)\s*</li>\s*", "* \\1\n", chunk)
        content = re.sub("<ul>(.*?)</ul>", replace_list_items, content, flags=re.DOTALL)
        
        fh = codecs.open("%s" % filename, "w", encoding="utf-8")
        fh.write(".. title: %s\n.. date: %s\n.. author: %s\n\n" % (title, created, author))
        fh.write(content)
        fh.write("\n")
        fh.close()


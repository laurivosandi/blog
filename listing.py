# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


""" Define and register a listing directive using the existing CodeBlock """


from __future__ import unicode_literals
import io
import os
try:
    from urlparse import urlunsplit
except ImportError:
    from urllib.parse import urlunsplit  # NOQA

from docutils import core
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.misc import Include
try:
    from docutils.parsers.rst.directives.body import CodeBlock
except ImportError:  # docutils < 0.9 (Debian Sid For The Loss)
    class CodeBlock(Directive):
        required_arguments = 1
        has_content = True
        option_spec = {}
        CODE = '<pre>{0}</pre>'

        def run(self):
            """ Required by the Directive interface. Create docutils nodes """
            return [nodes.raw('', self.CODE.format('\n'.join(self.content)), format='html')]
    directives.register_directive('code', CodeBlock)



# Add sphinx compatibility option
CodeBlock.option_spec['linenos'] = directives.unchanged


class FlexibleCodeBlock(CodeBlock):

    def run(self):
        if 'linenos' in self.options:
            self.options['number-lines'] = self.options['linenos']
        return super(FlexibleCodeBlock, self).run()
CodeBlock = FlexibleCodeBlock



# Add sphinx compatibility option
listing_spec = Include.option_spec
listing_spec['linenos'] = directives.unchanged


class Listing(Include):
    has_content = False
    required_arguments = 1
    optional_arguments = 1
    option_spec = listing_spec

    def run(self):
        fname, = self.arguments
        basename = os.path.basename(fname)
        if basename == "Makefile":
            lang = "makefile"
        elif fname.endswith(".py"):
            lang = "python"
        elif fname.endswith(".vhd"):
            lang = "vhdl"
        elif fname.endswith(".sh"):
            lang = "bash"
        elif fname.endswith(".c"):
            lang = "c"
        elif fname.endswith(".h"):
            lang = "c"
        else:
            raise

        source_dir = os.path.dirname(
                os.path.abspath(self.state.document.current_source))

        fpath = os.path.join(source_dir, fname)

        self.arguments.insert(0, fpath)
        self.options['code'] = lang
        with io.open(fpath, 'r+', encoding='utf8') as fileobject:
            self.content = fileobject.read().splitlines()
        self.state.document.settings.record_dependencies.add(fpath)
        return self.get_code_from_file(fileobject)

    def get_code_from_file(self, data):
        """ Create CodeBlock nodes from file object content """
        return super(Listing, self).run()

    def assert_has_content(self):
        """ Listing has no content, override check from superclass """
        pass

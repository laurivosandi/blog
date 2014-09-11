
from docutils import nodes
from docutils.parsers.rst import directives, Directive

CODE = """\
<iframe width="{width}"
height="{height}"
src="//www.youtube.com/embed/{yid}?rel=0&amp;hd=1&amp;wmode=transparent"
></iframe>"""

class Youtube(Directive):
    """ Restructured text extension for inserting youtube embedded videos

    Usage:
        .. youtube:: lyViVmaBQDg
           :height: 400
           :width: 600

    """
    has_content = True
    required_arguments = 1
    option_spec = {
        "width": directives.positive_int,
        "height": directives.positive_int,
    }

    def run(self):
        self.check_content()
        options = {
            'yid': self.arguments[0],
            'width': 425,
            'height': 344,
        }
        options.update(self.options)
        return [nodes.raw('', CODE.format(**options), format='html')]

    def check_content(self):
        if self.content:
            raise self.warning("This directive does not accept content. The "
                               "'key=value' format for options is deprecated, "
                               "use ':key: value' instead")

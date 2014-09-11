
import pygal
from ast import literal_eval

from docutils import nodes
from docutils.parsers.rst import Directive, directives



class Chart(Directive):
    """ Restructured text extension for inserting charts as SVG

        Usage:
            .. chart:: Bar
               :title: 'Browser usage evolution (in %)'
               :x_labels: ["2002", "2003", "2004", "2005", "2006", "2007"]

               'Firefox', [None, None, 0, 16.6, 25, 31]
               'Chrome',  [None, None, None, None, None, None]
               'IE',      [85.8, 84.6, 84.7, 74.5, 66, 58.6]
               'Others',  [14.2, 15.4, 15.3, 8.9, 9, 10.4]
    """

    has_content = True
    required_arguments = 1
    option_spec = {
        "copy": directives.unchanged,
        "css": directives.unchanged,
        "disable_xml_declaration": directives.unchanged,
        "dots_size": directives.unchanged,
        "explicit_size": directives.unchanged,
        "fill": directives.unchanged,
        "font_sizes": directives.unchanged,
        "height": directives.unchanged,
        "human_readable": directives.unchanged,
        "include_x_axis": directives.unchanged,
        "interpolate": directives.unchanged,
        "interpolation_parameters": directives.unchanged,
        "interpolation_precision": directives.unchanged,
        "js": directives.unchanged,
        "label_font_size": directives.unchanged,
        "legend_at_bottom": directives.unchanged,
        "legend_box_size": directives.unchanged,
        "legend_font_size": directives.unchanged,
        "logarithmic": directives.unchanged,
        "major_label_font_size": directives.unchanged,
        "margin": directives.unchanged,
        "no_data_font_size": directives.unchanged,
        "no_data_text": directives.unchanged,
        "no_prefix": directives.unchanged,
        "order_min": directives.unchanged,
        "pretty_print": directives.unchanged,
        "print_values": directives.unchanged,
        "print_zeroes": directives.unchanged,
        "range": directives.unchanged,
        "rounded_bars": directives.unchanged,
        "show_dots": directives.unchanged,
        "show_legend": directives.unchanged,
        "show_minor_x_labels": directives.unchanged,
        "show_y_labels": directives.unchanged,
        "spacing": directives.unchanged,
        "strict": directives.unchanged,
        "stroke": directives.unchanged,
        "style": directives.unchanged,
        "title": directives.unchanged,
        "title_font_size": directives.unchanged,
        "to_dict": directives.unchanged,
        "tooltip_border_radius": directives.unchanged,
        "tooltip_font_size": directives.unchanged,
        "truncate_label": directives.unchanged,
        "truncate_legend": directives.unchanged,
        "value_font_size": directives.unchanged,
        "value_formatter": directives.unchanged,
        "width": directives.unchanged,
        "x_label_rotation": directives.unchanged,
        "x_labels": directives.unchanged,
        "x_labels_major": directives.unchanged,
        "x_labels_major_count": directives.unchanged,
        "x_labels_major_every": directives.unchanged,
        "x_title": directives.unchanged,
        "y_label_rotation": directives.unchanged,
        "y_labels": directives.unchanged,
        "y_title": directives.unchanged,
        "zero": directives.unchanged,
    }

    def run(self):
        if pygal is None:
            msg = req_missing(['pygal'], 'use the Chart directive', optional=True)
            return [nodes.raw('', '<div class="text-error">{0}</div>'.format(msg), format='html')]
        options = {}
        if 'style' in self.options:
            style_name = self.options.pop('style')
        else:
            style_name = 'LightStyle'
        if 'fill' not in self.options:
            self.options["fill"] = "red"
        if '(' in style_name:  # Parametric style
            style = eval('pygal.style.' + style_name)
        else:
            style = getattr(pygal.style, style_name)
        for k, v in self.options.items():
            options[k] = literal_eval(v)

        chart = getattr(pygal, self.arguments[0])(style=style)
        chart.config(**options)
        for line in self.content:
            label, series = literal_eval('({0})'.format(line))
            chart.add(label, series)
        data = chart.render().decode('utf8')
        assert data.startswith("<?xml version='1.0' encoding='utf-8'?>")
        data = data[71-33:]
        return [nodes.raw('', data, format='html')]

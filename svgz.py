from lxml import etree

WHITELIST = {
		"a": ("class", "clip-path", "clip-rule", "fill", "fill-opacity", "fill-rule", "filter", "id", "mask", "opacity", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform", "href", "xlink:href", "xlink:title"),
		"circle": ("class", "clip-path", "clip-rule", "cx", "cy", "fill", "fill-opacity", "fill-rule", "filter", "id", "mask", "opacity", "r", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform"),
		"clipPath": ("class", "clipPathUnits", "id"),
		"defs": (),
	    "style" : ("type"),
		"desc": (),
		"ellipse": ("class", "clip-path", "clip-rule", "cx", "cy", "fill", "fill-opacity", "fill-rule", "filter", "id", "mask", "opacity", "requiredFeatures", "rx", "ry", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform"),
		"feGaussianBlur": ("class", "color-interpolation-filters", "id", "requiredFeatures", "stdDeviation"),
		"filter": ("class", "color-interpolation-filters", "filterRes", "filterUnits", "height", "id", "primitiveUnits", "requiredFeatures", "width", "x", "xlink:href", "y"),
		"foreignObject": ("class", "font-size", "height", "id", "opacity", "requiredFeatures", "style", "transform", "width", "x", "y"),
		"g": ("class", "clip-path", "clip-rule", "id", "display", "fill", "fill-opacity", "fill-rule", "filter", "mask", "opacity", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform", "font-family", "font-size", "font-style", "font-weight", "text-anchor"),
		"image": ("class", "clip-path", "clip-rule", "filter", "height", "id", "mask", "opacity", "requiredFeatures", "style", "systemLanguage", "transform", "width", "x", "xlink:href", "xlink:title", "y"),
		"line": ("class", "clip-path", "clip-rule", "fill", "fill-opacity", "fill-rule", "filter", "id", "marker-end", "marker-mid", "marker-start", "mask", "opacity", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform", "x1", "x2", "y1", "y2"),
		"linearGradient": ("class", "id", "gradientTransform", "gradientUnits", "requiredFeatures", "spreadMethod", "systemLanguage", "x1", "x2", "xlink:href", "y1", "y2"),
		"marker": ("id", "class", "markerHeight", "markerUnits", "markerWidth", "orient", "preserveAspectRatio", "refX", "refY", "systemLanguage", "viewBox"),
		"mask": ("class", "height", "id", "maskContentUnits", "maskUnits", "width", "x", "y"),
		"metadata": ("class", "id"),
		"path": ("class", "clip-path", "clip-rule", "d", "fill", "fill-opacity", "fill-rule", "filter", "id", "marker-end", "marker-mid", "marker-start", "mask", "opacity", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform"),
		"pattern": ("class", "height", "id", "patternContentUnits", "patternTransform", "patternUnits", "requiredFeatures", "style", "systemLanguage", "viewBox", "width", "x", "xlink:href", "y"),
		"polygon": ("class", "clip-path", "clip-rule", "id", "fill", "fill-opacity", "fill-rule", "filter", "id", "class", "marker-end", "marker-mid", "marker-start", "mask", "opacity", "points", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform"),
		"polyline": ("class", "clip-path", "clip-rule", "id", "fill", "fill-opacity", "fill-rule", "filter", "marker-end", "marker-mid", "marker-start", "mask", "opacity", "points", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform"),
		"radialGradient": ("class", "cx", "cy", "fx", "fy", "gradientTransform", "gradientUnits", "id", "r", "requiredFeatures", "spreadMethod", "systemLanguage", "xlink:href"),
		"rect": ("class", "clip-path", "clip-rule", "fill", "fill-opacity", "fill-rule", "filter", "height", "id", "mask", "opacity", "requiredFeatures", "rx", "ry", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform", "width", "x", "y"),
		"stop": ("class", "id", "offset", "requiredFeatures", "stop-color", "stop-opacity", "style", "systemLanguage"),
		"svg": ("class", "clip-path", "clip-rule", "filter", "id", "height", "mask", "preserveAspectRatio", "requiredFeatures", "style", "systemLanguage", "viewBox", "width", "x", "xmlns", "xmlns:se", "xmlns:xlink", "y"),
		"switch": ("class", "id", "requiredFeatures", "systemLanguage"),
		"symbol": ("class", "fill", "fill-opacity", "fill-rule", "filter", "font-family", "font-size", "font-style", "font-weight", "id", "opacity", "preserveAspectRatio", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "transform", "viewBox"),
		"text": ("class", "clip-path", "clip-rule", "fill", "fill-opacity", "fill-rule", "filter", "font-family", "font-size", "font-style", "font-weight", "id", "mask", "opacity", "requiredFeatures", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "text-anchor", "transform", "x", "xml:space", "y"),
		"textPath": ("class", "id", "method", "requiredFeatures", "spacing", "startOffset", "style", "systemLanguage", "transform", "xlink:href"),
		"title": (),
		"tspan": ("class", "clip-path", "clip-rule", "dx", "dy", "fill", "fill-opacity", "fill-rule", "filter", "font-family", "font-size", "font-style", "font-weight", "id", "mask", "opacity", "requiredFeatures", "rotate", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "systemLanguage", "text-anchor", "textLength", "transform", "x", "xml:space", "y"),
		"use": ("class", "clip-path", "clip-rule", "fill", "fill-opacity", "fill-rule", "filter", "height", "id", "mask", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "style", "transform", "width", "x", "xlink:href", "y"),
}

DEBUG = False

def parse(source):
    fix_fritzing = False
    fix_dia = False
    fix_inkscape = False

    with open(source) as fh:
        buf = fh.read(1024)
        if "<!-- Created with Fritzing (http://www.fritzing.org/) -->" in buf:
            fix_fritzing = True
        if "<!-- Created by diasvg.py -->" in buf:
            fix_dia = True
        if "<!-- Created with Inkscape (http://www.inkscape.org/) -->" in buf:
            fix_inkscape = True

    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    tree = etree.parse(source, parser)
    root = tree.getroot()

    left = root.attrib.pop("x", 0)
    top = root.attrib.pop("y", 0)
    width = root.attrib.pop("width", 0)
    height = root.attrib.pop("height", 0)

    # Make SVG-s scalable
    if "viewBox" not in root.attrib and width and height:
        root.attrib["viewBox"] = "%s %s %s %s" % (left, top, width, height)

    root.attrib["preserveAspectRatio"] = "xMidYMid meet"
        
    PREFIX = "{http://www.w3.org/2000/svg}"
    # Purge unknown attributes
    for j in tree.findall("//"):
        if not j.tag.startswith(PREFIX):
            if DEBUG: print("Purging unknown namespace:", j.tag)
            j.getparent().remove(j)
        elif not j.tag[len(PREFIX):] in WHITELIST:
            if DEBUG: print("Purging invalid tag:", j.tag)
            j.getparent().remove(j)
        else:
            # Expand CSS attributes for Inkscape, dafuq guys?!
            style = j.attrib.pop("style", "")
            if style:

                for i in style.split(";"):
                    if not i:
                        continue
                    key, value = i.split(":")
                    if key.startswith("-"):
                        continue
                    j.attrib[key.strip()] = value.strip()
                
            for key, value in j.attrib.iteritems():
                if key.startswith("{") and not key.startswith(PREFIX):
                    if DEBUG: print("Purging attribute of unknown namespace:", key, "of", j)
                    del j.attrib[key]
                elif key not in WHITELIST[j.tag[len(PREFIX):]]:
                    if DEBUG: print("Purging invalid attribute:", key, "of", j)
                    del j.attrib[key]
                    
            # Fix font family in Fritzing schematics, note that renaming is not enough
            # the real problem was the quotation!
            if fix_fritzing:
                if j.attrib.get("font-family", None) in ("OCR A Tribute", "'OCRA'", "'OCRAStd'", "OCRA", "'DroidSans'", "Bitstream Vera Sans"): # dafuq are you doing guys at Potsdam?!
                     j.attrib["font-family"] = "OCR A Tribute"
                     
            # Consistency!
            if j.attrib.get("font-family", None) in ("sans", "sans-serif", "Sans", "Bitstream Vera Sans"):
                 j.attrib["font-family"] = "Cabin Condensed"


    return tree
    
    # Inject CSS stylesheets is not neccessary if SVG is inlined
    with open(destination, "wb") as sh:
        if fix_fritzing:
            sh.write(('<?xml-stylesheet href="http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute.css" type="text/css"?>\n').encode("utf-8"))
        if fix_dia or fix_inkscape:
            sh.write(('<?xml-stylesheet href="http://fonts.googleapis.com/css?family=Cabin+Condensed" type="text/css"?>\n').encode("utf-8"))
        tree.write(sh, inclusive_ns_prefixes=False)


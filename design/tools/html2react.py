"""
Convert an approved design preview (design/previews/*.html) into:
  - a React component (JSX) with the same markup, large SVG drawings split into their own components
  - a CSS file whose rules are scoped under one class, so pages do not clash

Usage:
  python3 design/tools/html2react.py design/previews/signin.html \
      --name SignIn --scope jm-signin --out frontend/src/jm/pages/signin --links routes.json

The output is a starting point: behaviour (forms, data) is wired by hand in the generated component.
"""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BOOL = {"hidden", "checked", "required", "disabled", "open", "selected", "multiple", "readonly", "novalidate",
        "autofocus", "async", "defer", "playsinline", "muted", "loop", "autoplay", "controls", "inert", "default"}
HTML_ATTR = {
    "class": "className", "for": "htmlFor", "tabindex": "tabIndex", "readonly": "readOnly", "maxlength": "maxLength",
    "minlength": "minLength", "autocomplete": "autoComplete", "autofocus": "autoFocus", "crossorigin": "crossOrigin",
    "srcset": "srcSet", "enctype": "encType", "novalidate": "noValidate", "colspan": "colSpan", "rowspan": "rowSpan",
    "inputmode": "inputMode", "enterkeyhint": "enterKeyHint", "spellcheck": "spellCheck", "contenteditable": "contentEditable",
    "popovertarget": "popoverTarget", "popovertargetaction": "popoverTargetAction", "accept-charset": "acceptCharset",
    "http-equiv": "httpEquiv", "datetime": "dateTime", "referrerpolicy": "referrerPolicy", "fetchpriority": "fetchPriority",
    "playsinline": "playsInline", "allowfullscreen": "allowFullScreen", "frameborder": "frameBorder",
    "xlink:href": "xlinkHref", "xmlns:xlink": "xmlnsXlink", "xml:space": "xmlSpace", "itemprop": "itemProp",
}
# SVG attributes whose case the HTML parser folded to lowercase
SVG_CASE = {n.lower(): n for n in [
    "viewBox", "preserveAspectRatio", "gradientUnits", "gradientTransform", "patternUnits", "patternTransform",
    "patternContentUnits", "clipPathUnits", "maskUnits", "maskContentUnits", "markerWidth", "markerHeight",
    "markerUnits", "refX", "refY", "textLength", "lengthAdjust", "spreadMethod", "stdDeviation", "baseFrequency",
    "numOctaves", "keyTimes", "keySplines", "calcMode", "repeatCount", "attributeName", "pathLength",
    "startOffset", "primitiveUnits", "filterUnits", "kernelMatrix", "tableValues", "diffuseConstant",
    "specularExponent", "surfaceScale", "edgeMode", "xChannelSelector", "yChannelSelector", "repeatDur", "begin"]}


def camel(name: str) -> str:
    parts = name.split("-")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def style_obj(css: str) -> str:
    items = []
    for decl in css.split(";"):
        if ":" not in decl:
            continue
        k, v = decl.split(":", 1)
        k, v = k.strip(), v.strip()
        if not k:
            continue
        key = json.dumps(k) if k.startswith("--") else camel(k)
        items.append(f"{key}: {json.dumps(v)}")
    return "{{ " + ", ".join(items) + " }}"


def jsx_text(s: str) -> str:
    # braces and angle brackets must be escaped in JSX text
    return re.sub(r"([{}<>])", lambda m: "{'" + m.group(1) + "'}", s)


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, attrs, parent, []


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None)
        self.cur = self.root
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        if self.skip:
            return
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self.skip:
            return
        self.cur.children.append(data)


class Emitter:
    def __init__(self, links, asset_prefix, svg_min, comp_prefix):
        self.links, self.asset_prefix, self.svg_min, self.comp_prefix = links, asset_prefix, svg_min, comp_prefix
        self.art = {}          # component name -> jsx
        self.uses_link = False

    def attrs(self, node, in_svg):
        out = []
        tag = node.tag
        is_link = False
        for k, v in node.attrs:
            if k.startswith("on"):
                continue                     # no inline handlers
            if k == "href" and tag == "a" and v and v.split("#")[0].endswith(".html"):
                page, _, frag = v.partition("#")
                route = self.links.get(v) or self.links.get(page, "/")
                if frag and v not in self.links:
                    route = route + "#" + frag
                out.append(f'to="{route}"')
                is_link = True
                continue
            if k in ("src", "href") and v and v.startswith("assets/"):
                v = self.asset_prefix + v[len("assets/"):]
            if k == "style":
                out.append(f"style={style_obj(v or '')}")
                continue
            if tag in ("input", "textarea") and k == "value":
                k = "defaultValue"
            if tag == "input" and k == "checked":
                out.append("defaultChecked")
                continue
            if tag == "option" and k == "selected":
                continue                     # handled with defaultValue on <select> by hand
            if k.startswith(("data-", "aria-")):
                name = k
            elif in_svg:
                name = SVG_CASE.get(k) or HTML_ATTR.get(k) or (camel(k) if "-" in k or ":" in k else k)
                name = name.replace(":", "")
            else:
                name = HTML_ATTR.get(k, k)
            if v is None or (k in BOOL and v in ("", k)):
                out.append(name)
                continue
            if '"' in v or "\\" in v or "{" in v:
                out.append(f"{name}={{{json.dumps(v)}}}")
            else:
                out.append(f'{name}="{v}"')
        return out, is_link

    def emit(self, node, in_svg=False, top_svg=True):
        if isinstance(node, str):
            return jsx_text(node)
        tag = node.tag
        svg_here = in_svg or tag == "svg"
        if tag == "svg" and not in_svg and top_svg:
            inner = self.emit(node, in_svg=False, top_svg=False)
            if len(inner) >= self.svg_min:
                cls = dict(node.attrs).get("class", "") or ""
                base = re.sub(r"[^A-Za-z0-9]", " ", cls).title().replace(" ", "") or "Drawing"
                name = f"{self.comp_prefix}{base}Art"
                i = 2
                while name in self.art and self.art[name] != inner:
                    name = f"{self.comp_prefix}{base}Art{i}"
                    i += 1
                self.art[name] = inner
                return f"<{name} />"
            return inner
        attrs, is_link = self.attrs(node, svg_here)
        name = "Link" if is_link else tag
        if is_link:
            self.uses_link = True
        a = (" " + " ".join(attrs)) if attrs else ""
        if tag == "textarea":
            text = "".join(c for c in node.children if isinstance(c, str))
            if text:
                a += f" defaultValue={{{json.dumps(text)}}}"
            return f"<{name}{a} />"
        if tag in VOID or not node.children:
            return f"<{name}{a} />"
        inner = "".join(self.emit(c, svg_here, top_svg=False if tag == "svg" else top_svg) for c in node.children)
        return f"<{name}{a}>{inner}</{name}>"


# ── CSS scoping ─────────────────────────────────────────────────────────────────

def split_blocks(css: str):
    """Yield (prelude, body) for top-level blocks; body is None for @statements."""
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        semi = css.find(";", i)
        if j == -1:
            break
        if css[i:].lstrip().startswith("@") and semi != -1 and semi < j:
            yield css[i:semi + 1].strip(), None
            i = semi + 1
            continue
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        yield css[i:j].strip(), css[j + 1:k - 1]
        i = k


def scope_selector(sel: str, scope: str) -> str:
    sel = sel.strip()
    if not sel:
        return sel
    m = re.match(r"^(:root|html|body)(?![\w-])", sel)
    if m:
        rest = sel[m.end():]
        return f".{scope}{rest}"
    return f".{scope} {sel}"


def scope_css(css: str, scope: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for prelude, body in split_blocks(css):
        if body is None:
            if not prelude.startswith("@import") and not prelude.startswith("@charset"):
                out.append(prelude)
            continue
        if prelude.startswith(("@media", "@supports", "@container", "@layer", "@starting-style")):
            out.append(f"{prelude}{{{scope_css(body, scope)}}}")
        elif prelude.startswith("@"):
            out.append(f"{prelude}{{{body}}}")        # @keyframes, @font-face, @property: global
        else:
            sels = ",".join(scope_selector(s, scope) for s in prelude.split(","))
            out.append(f"{sels}{{{body}}}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--name", required=True)
    ap.add_argument("--scope", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--links", default="{}")
    ap.add_argument("--asset-prefix", default="/jm/")
    ap.add_argument("--svg-min", type=int, default=1500)
    ap.add_argument("--root-selector", default=None, help="CSS selector of the element to export (default: body)")
    a = ap.parse_args()

    html = Path(a.html).read_text()
    links = json.loads(Path(a.links).read_text()) if a.links.endswith(".json") else json.loads(a.links)
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    if "<body" in html:
        body = html[html.index("<body"):]
        body = body[body.index(">") + 1:]
        body = body[: body.rfind("</body>")] if "</body>" in body else body
    else:                                   # a fragment: drop the head-like parts
        body = re.sub(r"<(title)[^>]*>.*?</\1>|<(link|meta)[^>]*>", "", html, flags=re.S)
    b = Builder()
    b.feed(body)
    em = Emitter(links, a.asset_prefix, a.svg_min, a.name)
    children = [c for c in b.root.children if not (isinstance(c, str) and not c.strip())]
    jsx = "".join(em.emit(c) for c in children)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{a.name}.css").write_text(scope_css(css, a.scope) + "\n")
    art_lines = [f"export const {k} = () => ({v});" for k, v in em.art.items()]
    (out / f"{a.name}Art.jsx").write_text("/* Drawings from the approved design (generated by design/tools/html2react.py). */\n" + "\n\n".join(art_lines) + "\n")
    imports = ["import './%s.css';" % a.name]
    if em.uses_link:
        imports.insert(0, "import { Link } from 'react-router-dom';")
    if em.art:
        imports.append("import { %s } from './%sArt';" % (", ".join(em.art), a.name))
    comp = (
        "\n".join(imports)
        + f"\n\n/* Generated from {Path(a.html).name} by design/tools/html2react.py, then wired by hand. */\n"
        + f"export default function {a.name}Markup() {{\n  return (\n    <div className=\"{a.scope}\">{jsx}</div>\n  );\n}}\n"
    )
    (out / f"{a.name}Markup.jsx").write_text(comp)
    print(f"{a.name}: {len(jsx)} chars of JSX, {len(em.art)} drawings, css {len(css)} -> scoped")


if __name__ == "__main__":
    main()

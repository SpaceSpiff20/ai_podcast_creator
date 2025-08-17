from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import os

def _text(node, text): node.text = text; return node

def update_rss(feed_path, item_title, item_desc, audio_url, pub_date):
    rss_el = Element("rss", attrib={"version":"2.0"})
    ch = SubElement(rss_el, "channel")
    _text(SubElement(ch,"title"),"AI Podcast Starter")
    _text(SubElement(ch,"link"),"https://example.com/podcast")
    _text(SubElement(ch,"description"),"An AI-generated podcast about AI and tech.")
    _text(SubElement(ch,"language"),"en-us")

    item = SubElement(ch,"item")
    _text(SubElement(item,"title"), item_title)
    _text(SubElement(item,"description"), item_desc)
    _text(SubElement(item,"link"), audio_url)
    _text(SubElement(item,"pubDate"), pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000"))
    SubElement(item,"enclosure", attrib={"url":audio_url,"type":"audio/mpeg"})
    _text(SubElement(item,"guid"), audio_url)

    os.makedirs(os.path.dirname(feed_path), exist_ok=True)
    with open(feed_path,"wb") as f:
        f.write(tostring(rss_el, encoding="utf-8"))

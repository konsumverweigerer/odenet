#!/usr/bin/python

import csv
import xml.etree.ElementTree as ET
import urllib2

ilimap = dict(csv.reader(urllib2.urlopen(
    "https://raw.githubusercontent.com/globalwordnet/ili/master/ili-map-pwn30.tab"), delimiter='\t'))

wnlex = ET.parse("deWordNet.xml").find("Lexicon")

synset_map = dict(((x.attrib["id"], x.attrib["ili"])
                   for x in wnlex.findall("Synset")))


def wn_data():
    for a in wnlex.findall("LexicalEntry"):
        for sense in a.findall("Sense"):
            ili = synset_map[sense.attrib["synset"]]
            if ili != "" and ili in ilimap:
                yield (ilimap[ili], a.find("Lemma").attrib["writtenForm"])


wn_data_ger = list(set(wn_data()))
wn_data_ger.sort()

csv.writer(open("wn-data-ger.tab", 'w'), delimiter='\t').writerows(((s,
                                                                     "ger:lemma", l.encode('utf8')) for s, l in wn_data_ger))

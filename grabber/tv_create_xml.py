#! /usr/bin/env python2.7
import sys,os
import xml.etree.ElementTree as ElementTree
import tv_grab

TV_CHANNELS_FILE = "channels.tv"

def grab1day():
    xml = ElementTree.Element("tv")
    if not os.path.exists(TV_CHANNELS_FILE):
        tv_grab.get_channels(TV_CHANNELS_FILE, 1)
    f = open(TV_CHANNELS_FILE)
    for line in f:
        if line[0] <> '#':
            start = line.find(' ')
            name = line[start+1:-1].decode(errors='replace')
            id = line[:start]
            _subelement_channel(xml, name, id)
    return(xml)
        
def _subelement_channel(xml, name, id):
    el = ElementTree.Element("channel", {'name':name})
    prog_dicts = tv_grab.get_channel_all_days(id, 1)
    for d in  prog_dicts:
        newd = {
            'name':d['name'].decode(errors='replace'),
            'start':d['start'],
            'stop':d['stop']
        }
        ElementTree.SubElement(el, 'program', newd)
        
    xml.append(el)


#--------------------------------
if len(sys.argv) < 2:
    print("no commands received")
elif len(sys.argv) == 2:
    if sys.argv[1] == 'grab1day':
        xml = grab1day()
        print(ElementTree.tostring(xml))

#! /usr/bin/env python2.7
import xml.etree.ElementTree as ElementTree
import sys
import time

TVGUIDE_FILE = 'today.xml'
TVGUIDE_PIXELS_PER_MINUTE = 4
TVGUIDE_BASE_MINUTES = 360 * TVGUIDE_PIXELS_PER_MINUTE
TVGUIDE_TIME_START_LEFT = 250
TVGUIDE_PADDING = 3
TVGUIDE_HEIGHT = 50 
TVGUIDE_SPACING = 2
TVGUIDE_RESET = 300 #new day starts at 05:00
TVGUIDE_GROUP_SIZE = 8 #includes time row

def create_page():
    t = time.localtime()
    local_minutes = t[3] * 60 + t[4]
    t = t[3] * 60 -60 
    if t < TVGUIDE_RESET:
        t = t + 24 * 60
        local_minutes = local_minutes + 24 * 60
    base_time_px = t * TVGUIDE_PIXELS_PER_MINUTE
    xml = ElementTree.parse(TVGUIDE_FILE)
    #base
    html =  ElementTree.Element("html")
    head = ElementTree.SubElement(html, 'head')
    body = ElementTree.SubElement(html, 'body')
    link = ElementTree.SubElement(head, 'link', {'rel':'stylesheet','type':'text/css','href':'tv.css'})
    ElementTree.SubElement(head, 'script', {'src':'tv.js'}).text = ' '
    title = ElementTree.SubElement(head, 'title')
    title.text = 'tv guide pengu'
    line = ElementTree.SubElement(body, 'div', {'class':'line'})
    l = TVGUIDE_TIME_START_LEFT + (local_minutes-t) * TVGUIDE_PIXELS_PER_MINUTE
    line.set('style','left:{}px;'.format(l))
    line.text = ' '
    tvguide = ElementTree.SubElement(body, 'div',{'id':'tvguide'})
    time_div = ElementTree.SubElement(tvguide, 'div', {
        'class':'time',
        'style':'left{}px;'.format(0)})
    #add hour and half hour indicators for base till reset
    for i in range(t, TVGUIDE_RESET + 24 * 60, 30):
        l = TVGUIDE_TIME_START_LEFT + (i-t) * TVGUIDE_PIXELS_PER_MINUTE
        if (i / 30) % 2 == 0:
            txt = minutes_to_string(i)
        else:
            txt = " ".encode()
        ElementTree.SubElement(time_div, 'div', {
            'class':'itime',
            'style':'left:{}px;width:60px'.format(l)}).text = txt



    channelnames = ElementTree.SubElement(tvguide, 'div', {'id':'channelnames'})
    channels = ElementTree.SubElement(tvguide, 'div', {'id':'channels'})
    e1 = ElementTree.SubElement(channelnames, 'div', {'class':'echannelname'}).text = ' '
    #generate
    xml_channels = xml.findall('channel')
    y = 30
    channel_count = 0
    for c in xml_channels:
        channel_count = channel_count + 1
        if channel_count % TVGUIDE_GROUP_SIZE == 0:
            e1 = ElementTree.SubElement(channelnames, 'div', {'class':'echannelname'}).text = ' '
            str_time_div = ElementTree.tostring(time_div)
            new_item =ElementTree.fromstring(str_time_div)
            new_item.set('style',new_item.get('style') + 'top:{}px;'.format(y+5))
            tvguide.append(new_item)

            y = y + 30
        e1 = ElementTree.SubElement(channelnames, 'div', {'class':'channelname'})
        e1.text = c.attrib['name']
        channelx = ElementTree.SubElement(channels, 'div', {'class':'channel','id':e1.text})
        channelx.set('style','top:{}px;'.format(y))
        xml_programs = c.findall('program')
        if len(xml_programs) < 1:
            px = ElementTree.SubElement(channelx, 'div', {'class':'program'})
            px.text = 'nothing'
            continue;

        x = 0 
        prev_x = 0
        for p in xml_programs:
            start = string_to_minutes(p.get('start')) * TVGUIDE_PIXELS_PER_MINUTE
            if start < TVGUIDE_RESET:
                start = start + 24 * 60 * TVGUIDE_PIXELS_PER_MINUTE
                
            stop = string_to_minutes(p.get('stop')) * TVGUIDE_PIXELS_PER_MINUTE
            if stop < start:
                stop = stop + 24 * 60 * TVGUIDE_PIXELS_PER_MINUTE
            
            if start <= local_minutes*TVGUIDE_PIXELS_PER_MINUTE < stop:
                classname = 'aprogram'
            else:
                classname = 'program'


            width = stop - start- TVGUIDE_SPACING - TVGUIDE_PADDING * 2 
            x = start - base_time_px
            # if start is before base but end is after, clip
            if x < 0 and stop > base_time_px:
                x = -10 
                width = stop -TVGUIDE_SPACING - base_time_px - TVGUIDE_PADDING * 2 + 10
            
            #if start and stop are before base, ignore program
            if x < 0 and stop <= base_time_px:
                continue 

            #if connecting to previous program, empty a pixel
            if x == prev_x:
                x = x + TVGUIDE_SPACING 
                width = width -TVGUIDE_SPACING 

            px = ElementTree.SubElement(channelx, 'div', {'class':classname})
            px.text = p.get('name')
            px.set('title',px.text+ ' | {}-{}'.format(p.get('start'),p.get('stop')))

            px.set('style','left:{}px;top:{}px;width:{}px;'.format(x,y,width))
           
        y = y + TVGUIDE_HEIGHT 
    line.set('style','{}height:{}px'.format(line.get('style'),y+50))
    return html

def string_to_minutes(timestr):
    h = int(timestr[0:2])
    m = int(timestr[3:])
    return(h*60+m)

def minutes_to_string(min):
    h = int(min / 60)
    m = min - h*60
    if h>23:
        h = h -24
    return '{:0=2}:{:0=2}'.format(h,m)


#-----------------------
html = create_page()
print("Content-Type: text/html; charset=utf-8")
print("")
print(ElementTree.tostring(html))

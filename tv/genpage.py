import xml.etree.ElementTree as ElementTree
import json
import datetime

# add <!doctype HTML> yourself

f = open("today.json")
jsondata = json.load(f)
f.close()

tree = ElementTree.parse("base.html")
html = tree.getroot()
guide = html.find("./body/div[@id='guide']")

TFACTOR = 3 # 1 min = TFACTOR pixels
x = 150
now = datetime.datetime.now()

def tvgidsdatum_to_datetime(datumstring):
    #"2014-01-28 07:00:00"
    #"0123456789"        
    return(datetime.datetime(
            int(datumstring[0:4]), #YYYY
            int(datumstring[5:7]), #MM
            int(datumstring[8:10]),#DD
            int(datumstring[11:13]),#HH
            int(datumstring[14:16]),#mm
            int(datumstring[17:19]),#ss
    ))

def date_to_pixels(datum):
    pass
    

def add_program_to(xml_el, d):
    global x
    titel = d[u'titel']
    startd = tvgidsdatum_to_datetime(d[u'datum_start'])
    endd = tvgidsdatum_to_datetime(d[u'datum_end'])
    runtime = TFACTOR * (endd-startd).total_seconds()/60.0 #in minutes*TFACTOR
    el = ElementTree.SubElement(xml_el, "div", {
        "class":"prog", "style":"left:" + x.__str__() + "px;width:" + 
        runtime.__str__() + "px", "title":titel + " | " + 
        startd.strftime("%H:%M") + " - " + endd.strftime("%H:%M")
    })
    el.text = titel
    x += runtime+5
    
#jsondata = {"channelname":[{program}, {program}]}
for channelname in jsondata['order']:
    programlist = jsondata[channelname]
    chan_el = ElementTree.SubElement(guide, "div", {"class":"channel"})
    channame_el = ElementTree.SubElement(chan_el, "div", 
        {"class":"channelname"})
    channame_el.text = channelname
    x = 150
    for progdict in programlist:
        try:
            add_program_to(chan_el, progdict)
        except Exception as e:
            el = ElementTree.SubElement(chan_el, "div")
            el.text = e.__str__();
            break
            
    #break
        
print('<!doctype HTML>')        
print(ElementTree.tostring(html))

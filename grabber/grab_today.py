import urllib2
import json
import codecs

TV_CHANNELS_FILE = "channels2.tv"
f = codecs.open(TV_CHANNELS_FILE, 'r', "utf-8") #assume it exists
#find all the ids we need
#json data won't contain channel name, only number so we keep track of the names ourselves
id_names = {}
order = []
req = 'http://www.tvgids.nl/json/lists/programs.php?day=0&channels='
for u_line in f:
    if u_line[0] <> '#':
        start = u_line.find(' ')
        name = u_line[start+1:-1] 
        id = u_line[:start]
        id_names[id] = name
        order.append(name)
        req = req + id + ','
f.close()
#grab data from tvgids.nl. remove last ,
req = req[:-1]
webdata = urllib2.urlopen(req)
jsondata = json.load(webdata)
#replace channel id with channel name in jsondata
for key in jsondata.keys():
    jsondata[id_names[key]] = jsondata.pop(key)
#add channel order to jsondata
jsondata[u'order'] = order
f = codecs.open("today.json", 'w', "utf-8")
json.dump(jsondata, f, ensure_ascii=False)
f.close()

#{'channelid':
#   [
#       {'kijkwijzer':'', 'db_id':'124','titel':'aapjes','datum_start':'2014-01-26 23:05:00'
#       'datum_end':'2014-01-26 23:55:00'}.
#        {next program}
# 
# object{"channelid":array with prog objects, }

import xml.etree.ElementTree as xml
from xml.dom import minidom
import TimObjects
import string

class XMLManager:
    def __init__(self):
        print "XML Manager Initialised"

    def load_maplist(self):
        tree = xml.parse("data/maplist.xml")
        root = tree.getroot()
        map_dict = {}
        counter = 0
        for m in root.findall("map"):
            map_dict[counter]={}
            map_dict[counter]["name"] = m.attrib["name"]
            map_dict[counter]["path"] = m.attrib["path"]
            map_dict[counter]["fullname"] = m.find("fullname").text
            map_dict[counter]["preview"] = m.find("preview").text
            counter += 1
        return(map_dict)

    def load_playerdata(self):
        tree = xml.parse("user/player.xml")
        root = tree.getroot()
        base.player_name = root.find("name").text
        base.player_kingdom = root.find("kingdom").text
        base.direct_connect_ip = root.find("direct_connect").text

    def save_playerdata(self):
        root = xml.Element("PlayerData")
        pname = xml.Element("name")
        pname.text = base.player_name
        root.append(pname)
        pking = xml.Element("kingdom")
        pking.text = base.player_kingdom
        root.append(pking)
        dcip = xml.Element("direct_connect")
        dcip.text = base.direct_connect_ip
        root.append(dcip)

        fname = "user/player.xml"
        file = open(fname, 'w')
        xml.ElementTree(root).write(file)
        file.close()

        dom = minidom.parse(fname)
        final_xml = dom.toprettyxml()

        file = open(fname, 'w')
        file.write(final_xml)
        file.close()

    def map_load(self,map_path):
        tree = xml.parse(map_path)
        root = tree.getroot()
        base.map_width = int(string.split(root.attrib["size"],",")[0])
        base.map_height = int(string.split(root.attrib["size"],",")[1])
        base.map_scale = float(root.attrib["scale"])

        base.map_name = root.find("name").text
        base.map_tex = root.find("map_texture").text
        base.map_pre = root.find("map_preview").text

        fns = root.find("factions")
        for f in root.findall("faction"):
            base.factions.append(TimObjects.Faction(f.text,int(f.attrib["id"]),int(f.attrib["coin"])))

        objs = root.find("objects")

        for t in objs.findall("tower"):
            pos = string.split(t.attrib["position"],",")
            base.towers.append(TimObjects.Tower(int(t.attrib["faction"]),t.text,float(pos[0]),float(pos[1]),float(t.attrib["income"])))

        for a in objs.findall("army"):
            pos = string.split(a.attrib["position"],",")
            base.armies.append(TimObjects.Army(int(a.attrib["faction"]),a.text,float(pos[0]),float(pos[1]),-1))
import xml.etree.ElementTree as xml
from xml.dom import minidom

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

    def save_playerdata(self):
        root = xml.Element("PlayerData")
        pname = xml.Element("name")
        pname.text = base.player_name
        root.append(pname)
        pking = xml.Element("kingdom")
        pking.text = base.player_kingdom
        root.append(pking)

        fname = "user/player.xml"
        file = open(fname, 'w')
        xml.ElementTree(root).write(file)
        file.close()

        dom = minidom.parse(fname)
        final_xml = dom.toprettyxml()

        file = open(fname, 'w')
        file.write(final_xml)
        file.close()
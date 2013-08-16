import xml.etree.ElementTree as xml

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
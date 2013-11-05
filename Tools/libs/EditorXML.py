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

    def load(self):
        tree = xml.parse(base.map_path+"map.xml")
        root = tree.getroot()
        base.player_name = root.find("name").text
        base.player_kingdom = root.find("kingdom").text
        base.direct_connect_ip = root.find("direct_connect").text

    def save(self):
        if base.state != "placement" and base.state != "selecting":
            return 0

        print "SAVING XML!"

        root = xml.Element("Map")
        root.attrib["size"] = str(base.map_width)+","+str(base.map_height)
        root.attrib["scale"] = str(base.map_scale)

        mname = xml.Element("name")
        mname.text = base.map_name
        root.append(mname)

        tex = xml.Element("map_texture")
        tex.text = base.tex_name
        root.append(tex)

        pre = xml.Element("map_preview")
        pre.text = base.pre_name
        root.append(pre)

        fns = xml.Element("factions")
        root.append(fns)

        fn = xml.SubElement(fns,"faction")
        fn.text = base.faction0
        fn.attrib["id"] = "0"
        fn.attrib["coin"] = str(base.faction0_gold)

        fn = xml.SubElement(fns,"faction")
        fn.text = base.faction1
        fn.attrib["id"] = "1"
        fn.attrib["coin"] = str(base.faction1_gold)

        fn = xml.SubElement(fns,"faction")
        fn.text = base.faction2
        fn.attrib["id"] = "2"
        fn.attrib["coin"] = str(base.faction2_gold)

        objs = xml.Element("objects")
        root.append(objs)

        for t in base.towers:
            obj = xml.SubElement(objs,"tower")
            obj.text = t.name
            obj.attrib["faction"] = str(t.player)
            obj.attrib["income"] = str(t.income)
            obj.attrib["position"] = str(t.node_path.getX())+","+str(t.node_path.getY())

        for a in base.armies:
            obj = xml.SubElement(objs,"army")
            obj.text = a.name
            obj.attrib["faction"] = str(a.player)
            obj.attrib["position"] = str(a.node_path.getX())+","+str(a.node_path.getY())

        fname = base.map_path+"map.xml"
        file = open(fname, 'w')
        xml.ElementTree(root).write(file)
        file.close()

        dom = minidom.parse(fname)
        final_xml = dom.toprettyxml()

        file = open(fname, 'w')
        file.write(final_xml)
        file.close()
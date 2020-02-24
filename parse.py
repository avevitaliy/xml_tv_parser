# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import configparser, os, urllib.request, gzip

def getXMLFiles(url):
    urllib.request.urlretrieve(url, 'xmltv.xml.gz')
    input = gzip.GzipFile('xmltv.xml.gz', 'rb')
    s = input.read()
    input.close()

    output = open('xmltv.xml', 'wb')
    output.write(s)
    output.close()

def parseXML(xml_file,filename,channel_name):
    """
    Парсинг XML используя ElementTree
    """
    root_out = ET.Element("tv")
    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()

    for child in root:
        for step_child in child:
            if str(step_child.text) == channel_name:
                print("Канал %s найден, id канала - %s" % (channel_name,child.attrib['id']))
                channel_id=child.attrib['id']
                break
    try:
        channel_id
    except:
        print("Канал",channel_name,"не найден")
        return

    channel_out = ET.SubElement(root_out, "channel", attrib={'id':channel_id})
    display_name = ET.SubElement(channel_out, "display-name",attrib={'lang':'ru'})
    display_name.text = channel_name


    for child in root:
        if child.tag =='programme' and child.attrib['channel'] == channel_id:
            #print ("%s  -- %s"  % (child.attrib['start'],child.attrib['stop']))
            programm = ET.SubElement(root_out, "programme",attrib={'channel':channel_id,'start':child.attrib['start'],'stop':child.attrib['stop']})
            for step_child in child:
                if step_child.tag == "title":
                    #print("%s" % (step_child.text))
                    title = ET.SubElement(programm, "title")
                    title.text = step_child.text


    tree = ET.ElementTree(root_out)

    with open(filename, "wb") as fh:
        tree.write(fh, encoding="utf-8", xml_declaration=True)

 
if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini', encoding='utf-8')
    config.sections()
    main = config['main']
    channel = config['channels']
    getXMLFiles(main['url'])
    for file_name in config['channels']:  
        parseXML("xmltv.xml",os.path.join(main['dir'],file_name),channel[file_name])

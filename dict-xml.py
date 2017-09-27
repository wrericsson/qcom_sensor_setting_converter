# coding = 'utf-8'
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def read_xml(in_path):
    tree = ET.parse(in_path)
    return tree

def creat_dict(root):
    dict = {'registerData': '0x9999', 'registerAddr': '0x99', 'regDataType': '1', 'operation': 'WRITE', 'delayUs': '0x0'}
    dict_new = {}
    for key, valu in enumerate(root):
        dict_init = {}
        list_init = []
        for item in valu:
            list_init.append([item.tag, item.text])
            for lists in list_init:
                dict_init[lists[0]] = lists[1]
        dict_new[key] = dict_init
    return dict_new


def dict_to_xml(input_dict,root_tag,node_tag):
    root_name = ET.Element(root_tag)
    addrtype = r'range=\"[1,4]>2\"'
    addrdata = r'range=\"[1,4]>1\"'
    for (k, v) in input_dict.items():
        node_name = ET.SubElement(root_name, node_tag)
        for (key, val) in sorted(v.items(), key=lambda e:e[0], reverse=True):
            key = ET.SubElement(node_name, key)
            key.text = val
            # print key.tag
            if key.tag == 'operation':
                key.text = 'WRITE'
            if key.tag == 'delayUs':
                key.text = '0x0'
            if key.tag == 'registerAddr':
                key.text = addrtype
            if key.tag == 'registerData':
                key.text = addrdata
    return root_name


# def dict_to_xml(input_dict, root_tag, node_tag):
    # root_name = ET.Element(root_tag)
    # for (k, v) in input_dict.items():
        # node_name = ET.SubElement(root_name, node_tag)
        # for key, val in v.items():
            # key = ET.SubElement(node_name, key)
            # key.text = val
    # return root_name

def out_xml(root):
    rough_string = ET.tostring(root, 'utf-8')
    reared_content = minidom.parseString(rough_string)
    with open(out_file, 'w+') as fs:
        reared_content.writexml(fs, addindent=" ", newl="\n", encoding="utf-8")
    return True

if __name__ == '__main__':
    in_files = r"in.xml"
    out_file = r"out.xml"
    tree = read_xml(in_files)

    file_object = open('init.setting')
    try:
             all_the_text = file_object.read( )
    finally:
             file_object.close( )
    file_object.readline()

    node_new = creat_dict(tree.getroot())
    root = dict_to_xml(node_new, "initSetting", "regSetting") 
    out_xml(root)

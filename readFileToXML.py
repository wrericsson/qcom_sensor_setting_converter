#coding=utf-8  2017/4/7
__author__ = 'rui.r.wang@fih-foxconn.com'

import os
from xml.dom.minidom import Document

class readFileToXML(object):
    class_name = "MyClass"
    def __init__(self, filepath):
        self.filepath = filepath                        # 完整路径
        self._path = os.path.split(filepath)[0]         # 文件的路径
        self._filename = os.path.split(filepath)[1]     # 文件的名称
        self.DATA_JSON = readFileToXML.readFileToDict(self) # JSON格式数据
        self.DATA_XML = readFileToXML.json2XML(self)        # XML格式数据

    def getTime(self):
        '''
        文件名格式：zmonitor.2017-04-06-14_28
        把文件名的中的时间信息截取出来。格式：2017-04-06 14:28:00
        '''
        getTime_str = self._filename.partition(".")[2].replace("_", ":")
        # name.partition(".")的结果为("zmonitor", ".", "2017-04-06-14_28")
        getTime_list = list(getTime_str)
        getTime_list[10] = " "      # 字符串不可以单独修改，则修改格式为列表格式，修改后再整体修改为字符串格式。
        getTime_str = "".join(getTime_list)
        return getTime_str+":00"

    def readFileToDict(self):
        '''
        解析原始文件，提取信息存为字典格式（JSON）
        '''
        JSON_dict = {"hosts": {}}      # 用于这里原始文件的数据，编排成JSON格式。
        fileUpdataTime = readFileToXML.getTime(self)     # 取文件名中包含的时间。
        JSON_dict["datetime"] = fileUpdataTime
        with open(self.filepath, "r") as file:
            for line in file:
                print line
                line = line.replace("\n", "")
                
                print line

                line_item = line.split(' ')
                ip = line_item[0]                           # IP地址
                print ip
                name = line_item[1]                        # 机器名
                print name
                num3 = line_item[2]                         # 不知道做什么的三位数
                print num3
                delayus = line_item[3]     # CPU占用率 **%
                print  delayus          # 求得CPU空闲时间

                if not ip in JSON_dict["hosts"]:     #判断JSON_dict中索引是否存在，如不在则创建
                    JSON_dict["hosts"][ip] = {}               # 用IP做索引（用IP做一级目录）
                JSON_dict["hosts"][ip]["ip"] = ip     # 添加机器名到JSON_dict
                JSON_dict["hosts"][ip]["name"] = name     # 添加机器名到JSON_dict
                JSON_dict["hosts"][ip]["num3"] = num3        # 添加不知道什么的3位数，到JSON_dict
                JSON_dict["hosts"][ip]["delay"] = delayus        # 添加不知道什么的3位数，到JSON_dict
                # CPU占用率
                # JSON_dict["hosts"][ip]["CPU_utilization_percentage"] = CPU_utilization_percentage

        return JSON_dict

    def json2XML(self):
        '''
        生成XML文档。
        '''
        doc = Document()  #创建DOM文档对象
        root = doc.createElement('initSetting')                        # 创建根元素
        doc.appendChild(root)


        for ip in self.DATA_JSON["hosts"]:
            datas = doc.createElement('regSetting')                      # 创建root下第一节点datas
            root.appendChild(datas)

            data = doc.createElement('registerAddr')
            data_title = doc.createTextNode(self.DATA_JSON["hosts"][ip]["ip"])
            data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)
            
            data = doc.createElement('registerData')
            data_title = doc.createTextNode(self.DATA_JSON["hosts"][ip]["name"])
            data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)
            
            data = doc.createElement('regDataType')
            data_title = doc.createTextNode("")     # 为了解决自闭合标签。
            data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)

            data = doc.createElement('operation')
            # data.setAttribute("test", self.DATA_JSON["hosts"][ip]["ip"])
            # # data.setAttribute("itemName", "CPU idle time")      # CPU空闲时间
            # data.setAttribute("itemValue", self.DATA_JSON["hosts"][ip]["CPU_utilization_percentage"])
            data_title = doc.createTextNode("WRITE")     # 为了解决自闭合标签。
            data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)

            data = doc.createElement('delayUs')
            # data.setAttribute("test", self.DATA_JSON["hosts"][ip]["ip"])
            # # data.setAttribute("itemName", "CPU idle time")      # CPU空闲时间
            # data.setAttribute("itemValue", self.DATA_JSON["hosts"][ip]["CPU_utilization_percentage"])
            data_title = doc.createTextNode(self.DATA_JSON["hosts"][ip]["delay"])
            # data_title = doc.createTextNode("0x00")     # 为了解决自闭合标签。
            data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)

        return doc.toprettyxml(indent='   ')

    def makeXML(self):
        f = open(self._filename+'.xml', 'w')
        f.write(self.DATA_XML)
        f.close()


if __name__ == "__main__":
    TEST = readFileToXML("zmonitor.2017-04-06-14_28")

    TEST.makeXML()

    print("JSON格式：%s" % TEST.DATA_JSON)

    print("XML格式：\n %s " % TEST.DATA_XML)

    print(TEST._path)       # 路径
    print(TEST._filename)   # 文件名

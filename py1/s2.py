
import xml.etree.ElementTree as ET
import os
import json


def spotbugs():
    root = '/home/test/'
    project_name = ''
    paras = ''
    conf_json = root + "spotbugs.json"

    with open(conf_json, 'r') as json_file:
        configure = json.load(json_file)
        flag = True
        for val in configure:
            if flag:
                project_name = val["project_name"]
                flag = False
            else:
                paras += val['name'] + " "
    project_path = root + "/" + project_name
    xml_path = root + "spotbugs_details.xml"
    json_path = root + "spotbugs_overviews.json"

    command = '/home/spotbugs-4.2.3/bin/spotbugs ' + paras + " -output " + xml_path + " " + project_path
    os.system(command)

    details = analyze_results(xml_path)
    data = dict()
    data['project'] = {"project_name": project_name, "tool_name": 'spotbugs'}
    data["error"] = details

    print(data)
    with open(json_path, 'w') as json_file:
        json_file.write(json.dumps(data))


def analyze_results(xml_path):
    tree = ET.parse(xml_path)
    details = []
    if tree:
        dom = tree.getroot()
        for bugs in dom:
            tmp = dict()
            tmp["type"] = ""
            tmp["start"] = ""
            tmp["file_name"] = ""
            tmp["desc"] = ""
            if bugs.tag == 'BugInstance':
                tmp["type"] = bugs.attrib['category']
                tmp["desc"] = bugs.attrib['type']
                for bug in bugs:
                    start = ''
                    if bug.tag == 'Class':  # class 相关信息
                        if bug[0].tag == 'SourceLine':
                            start = bug[0].attrib['start']
                            tmp["file_name"] = bug[0].attrib['sourcepath']

                    flag = False
                    if bug.tag == 'Method':  # Method 相关信息
                        if bug[0].tag == 'SourceLine':
                            start = bug[0].attrib['start']
                            flag = True

                    tmp["start"] = start
                    if flag: break
                details.append(tmp)
    return details


if __name__ == '__main__':
    spotbugs()


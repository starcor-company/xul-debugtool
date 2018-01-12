#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import xmltodict
from PyQt5.QtWebEngineWidgets import QWebEngineScript
from lxml import etree

from XulDebugTool.logcatapi.Logcat import STCLogger


class Utils(object):
    @staticmethod
    def xml2json(xml, tag):
        # 将xml的某个tag转化成json
        doc = xmltodict.parse(xml)[tag]
        if doc != None:
            str = json.dumps(dict(doc))
            return json.loads(str)
        else:
            return ''

    @staticmethod
    def scriptCreator(path, name, page):
        script = QWebEngineScript()
        f = open(path, 'r', encoding='utf-8')
        script.setSourceCode(f.read())
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setName(name)
        script.setWorldId(QWebEngineScript.MainWorld)
        page.scripts().insert(script)

    @staticmethod
    def findNodeById(id, xml):
        root = etree.fromstring(xml)
        # print(etree.tostring(root, pretty_print=True).decode('utf-8'))
        try:
            list = root.xpath("//*[@id=%s]" % id)
        except Exception as e:
            STCLogger().e(e)
        return list[0]

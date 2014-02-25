__author__ = 'Tadimy'
import sys
import re
import xml.etree.ElementTree as ET
from xml.sax import handler, parseString

reload(sys)
sys.setdefaultencoding('utf-8')
fields = (
"fullName", "absName", "cycle", "ISSN", "contact", "homepage", "submitLink", "elseLink", "fields", "acceptPercent",
"speed", "ediFee", "pubFee", "totalCite", "impactFactor", "impactFactor5", "immediacyIndex", "articles",
"citedHalfLife", "igenfactorScore", "articleInfluenceScore", "abbTitle")
init_sql = "INSERT INTO `51prof_main`.`journal` (`id`, `fullName`, `absName`, `cycle`, `ISSN`, `contact`, `homepage`, `submitLink`, `elseLink`, `fields`, `acceptPercent`, `speed`, `ediFee`, `pubFee`, `totleCite`, `impactFactor`, `impactFactor5`, `immediacyIndex`, `articles`, `citedHalfLife`, `igenfactorScore`, `articleInfluenceScore`, `abbTitle`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


class JournalHandler(handler.ContentHandler):
    def __init__(self):
        self.journal = {}
        self.current_tag = ""
        self.in_quote = 0

    def startElement(self, name, attrs):
        if name == "journal":
            self.journal = {}
        self.current_tag = name
        self.in_quote = 1

    def endElement(self, name):
        if name == "journal":
            in_fields = tuple([("'" + re.sub('"', ' ', self.journal.get(i, "")) + " '") for i in fields])
            #print init_sql % in_fields
            with open('output_.sql', 'a+') as output:
                output.write(init_sql % in_fields + '\n')
        self.in_quote = 0

    def characters(self, content):
        if self.in_quote:
            self.journal.update({self.current_tag: content})


if __name__ == "__main__":
    f = open(sys.argv[1])
    parseString(f.read(), JournalHandler())
    f.close()

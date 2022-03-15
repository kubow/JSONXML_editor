'''This file is part of H808E project
class File to determine loaded content
class Json & Xml to shadow File process
'''
import json
from random import randint, choice
import xml.etree.ElementTree as ETree


class File(object):
    def __init__(self):
        self.content = ''
        self.type = ''
        self.debug = True

    def values_list(self):
        v_l = []
        if isinstance(self.content, dict):
            v_l.extend(value for column, value in self.content.items())
        elif isinstance(self.content, list):
            for row in self.content:
                v_l.extend(value for column, value in row.items())
        return v_l

    def field_list(self):
        if self.debug:
            if isinstance(self.content, dict):
                if len(self.content) > 1:
                    f_l = list(self.content.keys())
                elif isinstance(self.content[next(iter(self.content))], dict):
                    f_l = list(self.content[next(iter(self.content))].keys())
                else:
                    f_l = list(1,2,3)  # what can be extended?
                print(self.type, 'is a dictionary with keys:', f_l)
            elif isinstance(self.content, list):
                f_l = list(self.content[0])
                print(self.type, 'is a array with keys:', f_l)
            else:
                f_l = []
                print(self.type, 'is not recognized:', f_l)
        elif isinstance(self.content, dict):
            if len(self.content) > 1:
                f_l = list(self.content.keys())
            else:
                f_l = list(self.content[next(iter(self.content))].keys())
        elif isinstance(self.content, list):
            f_l = list(self.content[0])
        else:
            f_l = []
        return f_l 

class Json(File):
    def __init__(self, source='', from_stream=False):
        File.__init__(self)
        if from_stream:
            self.type = 'stream'
            self.content = json.loads(source)
        elif source:
            self.type = source
            with open(source, "r", encoding="utf-8") as read_content:
                self.content = json.load(read_content)  # TODO: need to determine if to use load or loads
        else:
            self.type = 'random_default'
            self.content = json.loads(random_json())
        
    def export_to(self, location):
        if location:
            with open(location, "w", encoding="utf-8") as dump:
                dump.write(json.dumps(self.content))

class Xml(File):
    def __init__(self, source='', from_stream=False):
        File.__init__(self)
        if from_stream:
            self.type = 'stream'
            self.content = ETree.fromstring(source)
        elif source:
            self.type = source
            self.content = ETree.parse(source).getroot()
        else:
            self.type = 'random_default'
            self.content = ETree.fromstring(random_xml())

    def export_to(self, location):
        if location:
            pass  # for now
        
                
def random_json(not_so_random=0):
    """This function describes types of JSON objects, that come into play
    https://techwithtech.com/json-object-vs-json-array/
    Helps debug process
    """
    dictionary = '{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362}'
    d_with_array = '{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362, "battery": ["100 kWh", "90 kWh", "80 kWh"]}'
    array = '[{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362}, {"manufacturer": "Tesla Inc. "," model": "Tesla 3 "," engineType": "elecrical", "horsePower": 346}]'
    if not not_so_random:
        return (dictionary, d_with_array, array)[randint(0,2)]

    if isinstance(not_so_random, int):
        return (dictionary, d_with_array, array)[not_so_random-1]
    else:
        return ''  #
    # return choice(dictionary, d_with_array, array)

def random_xml(not_so_random=0):
    """This function describes types of XML objects, that come into play
    https://techwithtech.com/json-object-vs-json-array/
    Helps debug process
    """
    simple = """
    <data>
        <items>
            <item name="item1">item1abc</item>
            <item name="item2">item2abc</item>
        </items>
    </data>
    """
    simple_array = """
    <encspot>
        <file>
            <Name>some filename.mp3</Name>
            <Encoder>Gogo (after 3.0)</Encoder>
            <Bitrate>131</Bitrate>
        </file>
        <file>
            <Name>another filename.mp3</Name>
            <Encoder>iTunes</Encoder>
            <Bitrate>128</Bitrate>  
        </file>
    </encspot>
    """
    if not_so_random == 1:
        return simple
    elif not_so_random == 2:
        return simple_array
    else:
        return choice(simple, simple_array)

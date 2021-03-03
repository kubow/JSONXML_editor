'''All should be returned as a dictionary'''
import json


class JsonArray:
    def __init__(self, source=""):
        self.content = ""
        self.field = []
        if source:
            print('getting', source)
            with open(source, "r", encoding="utf-8") as read_content:
                # need to determine if to use load or loads
                self.content = json.load(read_content)
                #self.serialized = json.loads(read_content)
                if isinstance(self.content, dict):
                    print('special process undergo')
            for line in self.content:
                for field in line.keys():
                    self.field.append(field)
                break                    
                

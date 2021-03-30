'''All should be returned as a dictionary'''
import json
from random import randint  # , choice


class JsonObject:
    def __init__(self, source="", debug=True):
        if source:
            print('getting', source)  # if debug else pass
            with open(source, "r", encoding="utf-8") as read_content:
                self.content = json.load(read_content)  # TODO: need to determine if to use load or loads
        else:
            self.content = json.loads(random_json())
        if isinstance(self.content, dict):
            print('JSON is type dictionary')
            self.field_list = list(self.content.keys())
            self.type = 'dic'
        elif isinstance(self.content, list):
            print('JSON is type array')
            self.field_list = list([a for a in self.content[0]])
            self.type = 'arr'
        else:
            print('JSON is unknown type, rolling back')
            self.field_list = ''
            self.type = ''

    def export(self, location):
        if location:
            with open(location, "w", encoding="utf-8") as dump:
                dump.write(json.dumps(self.content))

                
def random_json():
    """This function describes types of JSON objects, that come into play
    https://techwithtech.com/json-object-vs-json-array/
    Helps debug process
    """
    dictionary = '{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362}'
    d_with_array = '{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362, "battery": ["100 kWh", "90 kWh", "80 kWh"]}'
    array = '[{"manufacturer": "Tesla Inc.", "model": "Tesla S", "engineType": "elecrical", "horsePower": 362}, {"manufacturer": "Tesla Inc. "," model": "Tesla 3 "," engineType": "elecrical", "horsePower": 346}]'
    return (dictionary, d_with_array, array)[randint(0,2)]
    # return choice(dictionary, d_with_array, array)

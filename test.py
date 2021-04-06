from DataObject import Json, Xml, random_json, random_xml

timer = {}

print('*'*10,'JSON part')
json1 = Json(random_json(1), from_stream=True)
json1.field_list()

json2 = Json(random_json(2), from_stream=True)
json2.field_list()

json3 = Json(random_json(3), from_stream=True)
json3.field_list()

json4 = Json('test_array.json')
json4.field_list()

json5 = Json('test_dict.json')
json5.field_list()

# TODO: same with XML object
# TODO: rewrite with unittesting
# TODO: add timing for each separate operation
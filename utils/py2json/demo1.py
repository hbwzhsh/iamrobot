import json

obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
encodejson = json.dumps(obj)

print repr(obj)
print encodejson

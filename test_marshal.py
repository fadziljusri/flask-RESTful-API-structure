from flask_restful import marshal, fields
import json

test = {}
test['name'] = fields.String(attribute='p_name')
data = {'p_name': 'black'}
print(json.dumps(marshal(data, test)))


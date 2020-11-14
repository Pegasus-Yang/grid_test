# Author:Pegasus-Yang
# Time:2020/11/13 21:52
import json

import requests

# r = requests.get('http://localhost:8006/history')
# print(r.text)
# with open('x.json', 'w') as f:
#     json.dump(r.json(), f, indent=2)
import yaml


def gen_mock_rule(history_data):
    history_data = history_data.get('data', None)
    if not history_data:
        return False
    if isinstance(history_data, list):
        yaml_data = []
        for history in history_data:
            h_req = history['req']
            req = {
                'method': h_req['method'],
                'path': h_req['path'],
            }
            # req.update(get_content(h_req))
            h_res = history['res']
            res = h_res['content']
            yaml_data.append({'req': req, 'res': res})
        # todo:去重
        return yaml_data


if __name__ == '__main__':
    with open('x.json',encoding='U8') as f:
        base_data = json.load(f)
    yaml_data = gen_mock_rule(base_data)
    with open('tmp.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, indent=2)
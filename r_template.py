from __future__ import print_function
import json
import requests
import collections


def get_item(item_uri):
    r = requests.get(item_uri)
    if r.status_code == requests.codes.ok:
        t = r.json()
        return t
    else:
        return None


def item_processor(class_uri):
    t = get_item(class_uri)
    if t:
        c = collections.OrderedDict()
        c['@id'] = t['@id']
        c['name'] = t['o:local_name']
        c['term'] = t['o:term']
        if 'o:comment' in t:
            c['description'] = t['o:comment']
        return c
    else:
        return None

def parse_template(t):
    template = item_processor(t['o:resource_class']['@id'])
    template['label'] =  t['o:label']
    if template:
        template['fields'] = []
        for item in t['o:resource_template_property']:
            i = item['o:property']['@id']
            c = item_processor(i)
            template['fields'].append(c)
    print(json.dumps(template, sort_keys=False, indent=4))

def main():
    for r in range(4,8):
        t = get_item('http://omeka.dlcs-ida.org/api/resource_templates/' + str(r))
        if t:
            parse_template(t)

if __name__ == '__main__':
    main()

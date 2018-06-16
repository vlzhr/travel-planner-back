from glob import glob
from json import loads, dumps
from service import link, load_file, dump_to_file

old_max = max
def max(*args):
    if len(args[0]) == 0:
        return -1
    return old_max(*args)

def get_projects():
    return glob(link("travs", "*.json"))

def sorting(x):
    return 0-int("1"+x.replace("_", ""))

def get_project(title):
    if not title.endswith(".json"):
        title += ".json"
    try:
        data = load_file("travs", title)
        return data
    except IOError:
        return dumps({"error": "File not found"})

def save_project(title, content={"points": {"0": {"children": []}}}):
    dump_to_file(content, "travs", title+".json")

def add_child(project, parent_id, content={}):
    content.update({"children": []})
    dic = get_project(project)

    new = parent_id + "_" + str( max( [ int(n.split("_")[-1]) for n in dic['points'][parent_id]['children'] ] ) + 1 )
    if new in dic['points']:
        dic['points'][new].update(content)
    else:
        dic['points'][new] = content
    dic['points'][parent_id]['children'].append(new)
    save_project(project, dic)
    return dic#dic['points'][parent_id]
    
def change_field(project, item_id, key, value):
    dic = get_project(project)
    dic['points'][item_id][key] = value
    save_project(project, dic)

def save_point(project, item_id, item):
    dic = get_project(project)
    dic['points'][item_id].update(item)
    save_project(project, dic)
    return dic#dic['points'][item_id]

def new_iata(project, item_id, code):
    dic = get_project(project)
    dic['points'][item_id]["iata"] = code
    save_project(project, dic)
    return dic
    
def del_point(project, item_id):
    dic = get_project(project)
    for n in dic['points'][item_id]["children"]:
        del_point(project, n)
    try:
        del dic['points'][item_id]
        dic['points'][item_id.rsplit('_', 1)[0]]['children'].remove(item_id)
    except KeyError:
        pass
    save_project(project, dic)
    return True




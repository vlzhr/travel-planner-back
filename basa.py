from service import link, load_file, dump_to_file
import time
import work
import os

def get_users():
    return load_file("users", "users.json")

def save_users(dic):
    dump_to_file(dic, "users", "users.json")

def init_user(ui):
    users = get_users()
    users[ui] = {"projects": [], "auth_at": time.time()}
    save_users(users)

def get_uprojects(ui):
    users = get_users()
    if ui in users:
        return users[ui]['projects']
    init_user(ui)
    return []

def add_uproject(ui, pid, name):
    users = get_users()
    users[ui]['projects'].append({"id": pid, "name": name})
    save_users(users)

def add_project(ui, name):
    li = work.get_projects()
    current = max([int(os.path.split(n)[-1].split(".")[0]) for n in li]) + 1
    work.save_project(str(current), {"name": name, "points": {"0": {"id": "0", "children": [],
                                                                    "title": "Moscow", "desc": "Our house"}}})
    add_uproject(ui, current, name)
    return get_uprojects(ui)

def del_project(ui, pid):
    users = get_users()
    users[ui]['projects'] = [n for n in users[ui]['projects'] if not int(n['id']) == int(pid)]
    save_users(users)
    return users[ui]['projects']
    

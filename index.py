from flask import Flask, jsonify, request
import work
import basa
from urllib2 import urlopen
from json import loads
import prices_saver as flights

app = Flask(__name__)
app.debug = True

old_j = jsonify
def jsonify(li):
    answer = old_j({"response": li})
    answer.headers['Access-Control-Allow-Origin'] = '*'
    return answer

def get_project(title):
    project = work.get_project(title)
    project['id'] = title
    return project

@app.route("/")
def index():
    return "This is API of travel planner! Made by Vladimir Zhuravlev"

@app.route("/load_uprojects")
def load_uprojects():
    return jsonify( basa.get_uprojects(request.args['id']) )

@app.route("/load_project")
def load_project():
    project = work.get_project(request.args['id'])
    project['id'] = request.args['id']
    return jsonify( project )

@app.route("/add_project")
def add_project():
    i = basa.add_project(request.args['ui'], request.args['name'])
    return jsonify( i )

@app.route("/del_project")
def del_project():
    prs = basa.del_project(request.args['ui'], request.args['id'])
    return jsonify( prs )

@app.route("/save_point")
def save_point():
    point = work.save_point(request.args['pid'], request.args['id'],
                            {"title": request.args['title'],
                             "desc": request.args['desc']})
    point['id'] = request.args['id']
    return jsonify( get_project(request.args['pid'])) #point )
    
@app.route("/del_point")
def del_point():
    work.del_point(request.args['pid'], request.args['id'])
    return jsonify( {"success": "true"} )

@app.route("/replace_point")
def replace_point():
    point = work.save_point(request.args['pid'], request.args['id'],
                            {"x": request.args['x'],
                             "y": request.args['y']})
    return jsonify( get_project(request.args['pid']))

@app.route("/add_child")
def add_child():
    parent = work.add_child(request.args['pid'], request.args['parent_id'],
                   {'title': request.args['title'], 'desc': request.args['desc'],
                             "x": 50,
                             "y": 20})
    return jsonify( get_project(request.args['pid']))

@app.route("/add_traveller")
def add_traveller():
    pr = basa.add_uproject(request.args['ui'], request.args['pid'], request.args['name'])
    return jsonify( {"success": "true"} )

@app.route("/get_friends")
def get_friends():
    resp = urlopen("http://api.vk.com/method/friends.get?fields=city&user_id="+request.args['ui'])
    text = resp.read().decode("utf-8")
    return jsonify( loads(text) )

@app.route("/get_iata")
def get_iata():
    """ unused because of problems with coding ; realised in js """
    return jsonify(flights.find_iata(request.args['q']))

@app.route("/new_iata")
def new_iata():
    work.new_iata(request.args['pid'], request.args['id'], request.args['code'])
    return jsonify( {"success": "true"} )

@app.route("/get_dest")
def get_dest():
    return jsonify( flights.get_dest_info(request.args['from'], request.args['to']) )

@app.route("/g", methods=["POST"])
def g():
    json = request.get_json()
    try:
        flights.pot_test(json)
        return "success-not"
    except Exception as e:
        return "error " + str(e)

if __name__ == "__main__":
    app.run(port=80)

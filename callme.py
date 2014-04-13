#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
 
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    surname = db.Column(db.String(80), unique=True)
    number = db.Column(db.String(80), unique=True)
    
    def __init__(self, name, surname, number):
        self.name = name
        self.surname = surname
        self.number = number
        self.home = home
        self.work = work
        self.phone = phone
        self.phone2 = phone2
        self.address = address

    def __repr__(self):
        return '<User %r>' % self.name
 
@auth.get_password
def get_password(username):
    if username == 'daniele':
        return 'python'
    return None
 
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
contacts = [
    {
        'id': 1,
        'name': u'Daniele',
        'surname': u'Costarella',
        'number': u'3891234567',
        'label': u'red'
    }
]
 
def make_public_contact(contact):
    new_contact = {}
    for field in contact:
        if field == 'id':
            new_contact['uri'] = url_for('get_task', contact_id = contact['id'], _external = True)
        else:
            new_contact[field] = contact[field]
    return new_contact
    
@app.route('/callme/api/v1.0/contacts', methods = ['GET'])
#@auth.login_required
def get_tasks():
    return jsonify( { 'contacts': map(make_public_contact, contacts) } )
 
@app.route('/callme/api/v1.0/contacts/<int:contact_id>', methods = ['GET'])
#@auth.login_required
def get_task(contact_id):
    contact = filter(lambda t: t['id'] == contact_id, contacts)
    if len(contact) == 0:
        abort(404)
    return jsonify( { 'contact': make_public_contact(contact[0]) } )
 
@app.route('/callme/api/v1.0/contacts', methods = ['POST'])
#@auth.login_required
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    contact = {
        'id': tasks[-1]['id'] + 1,
        'name': request.json['name'],
        'surname': request.json['surname'],
        'number': request.json['number'],
        'label': request.json.get('label', ""),
        #'description': request.json.get('description', ""),
        #'done': False
    }
    contacts.append(contact)
    return jsonify( { 'contact': make_public_contact(contact) } ), 201
 
@app.route('/callme/api/v1.0/contacts/<int:contact_id>', methods = ['PUT'])
#@auth.login_required
def update_task(contact_id):
    task = filter(lambda t: t['id'] == contact_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_contact(task[0]) } )
    
@app.route('/callme/api/v1.0/contacts/<int:contact_id>', methods = ['DELETE'])
#@auth.login_required
def delete_task(contact_id):
    task = filter(lambda t: t['id'] == contact_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)

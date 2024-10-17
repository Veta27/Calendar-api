rom flask import Flask, jsonify, request, abort
from db import init_db
from model import db, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных
init_db(app)

@app.route('/api/v1/calendar/', methods=['POST'])
def create_event():
    data = request.get_json()
    if not all(k in data for k in ('date', 'title', 'text')):
        abort(400, 'Missing data')

    if len(data['title']) > 30:
        abort(400, 'Title must be up to 30 characters')
    if len(data['text']) > 200:
        abort(400, 'Text must be up to 200 characters')

    if Event.query.filter_by(date=data['date']).first():
        abort(400, 'An event is already scheduled for this date')

    new_event = Event(date=data['date'], title=data['title'], text=data['text'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'id': new_event.id}), 201

@app.route('/api/v1/calendar/', methods=['GET'])
def list_events():
    events = Event.query.all()
    return jsonify([{'id': event.id, 'date': event.date, 'title': event.title, 'text': event.text} for event in events])

@app.route('/api/v1/calendar/<int:event_id>/', methods=['GET'])
def read_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        abort(404)
    return jsonify({'id': event.id, 'date': event.date, 'title': event.title, 'text': event.text})

@app.route('/api/v1/calendar/<int:event_id>/', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        if len(data['title']) > 30:
            abort(400, 'Title must be up to 30 characters')
        event.title = data['title']

    if 'text' in data:
        if len(data['text']) > 200:
            abort(400, 'Text must be up to 200 characters')
        event.text = data['text']

    db.session.commit()
    return jsonify({'id': event.id, 'date': event.date, 'title': event.title, 'text': event.text})

@app.route('/api/v1/calendar/<int:event_id>/', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        abort(404)

    db.session.delete(event)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False, unique=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'text': self.text
        }
@app.route('/')
def index():
    return "Welcome to the Calendar API!"

@app.route('/api/v1/calendar', methods=['GET'])
def list_events():
    events = Event.query.all()
    return jsonify([event.serialize() for event in events]), 200

@app.route('/api/v1/calendar', methods=['POST'])
def add_event():
    data = request.get_json()
    date = data.get('date')
    title = data.get('title')
    text = data.get('text')

    if Event.query.filter_by(date=date).first():
        return jsonify({'message': 'Event already exists for this date.'}), 400

    if len(title) > 30:
        return jsonify({'message': 'Title exceeds maximum length.'}), 400

    if len(text) > 200:
        return jsonify({'message': 'Text exceeds maximum length.'}), 400

    event = Event(date=date, title=title, text=text)
    db.session.add(event)

    try:
        db.session.commit()
        return jsonify(event.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Event could not be created.'}), 400

@app.route('/api/v1/calendar/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.serialize()), 200

@app.route('/api/v1/calendar/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get_or_404(event_id)

    title = data.get('title', event.title)
    text = data.get('text', event.text)

    if len(title) > 30:
        return jsonify({'message': 'Title exceeds maximum length.'}), 400

    if len(text) > 200:
        return jsonify({'message': 'Text exceeds maximum length.'}), 400

    event.title = title
    event.text = text

    db.session.commit()
    return jsonify(event.serialize()), 200

@app.route('/api/v1/calendar/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully.'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание всех таблиц базы данных
    app.run(debug=True)

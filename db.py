from flask import Flask
from model import db

def init_db(app: Flask):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Создаём все таблицы

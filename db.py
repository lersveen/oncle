import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oncall.db'  # SQLite connection string
db = SQLAlchemy(app)


# Define the models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    shifts = db.relationship('Shift', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route('/', methods=['GET'])
def root():
    return "OK"


# API endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(result)


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    shifts = [{'id': shift.id, 'team_id': shift.team_id, 'user_id': shift.user_id, 'start_time': shift.start_time,
               'end_time': shift.end_time} for shift in user.shifts]

    notifications = [{'id': notification.id, 'shift_id': notification.shift_id, 'message': notification.message,
                      'is_read': notification.is_read, 'created_at': notification.created_at}
                     for notification in user.notifications]

    result = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'shifts': shifts,
        'notifications': notifications
    }
    return jsonify(result)


@app.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    result = [{'id': team.id, 'name': team.name} for team in teams]
    return jsonify(result)


@app.route('/shifts', methods=['GET'])
def get_shifts():
    shifts = Shift.query.all()
    result = [{'id': shift.id, 'team_id': shift.team_id, 'user_id': shift.user_id, 'start_time': shift.start_time,
               'end_time': shift.end_time} for shift in shifts]
    return jsonify(result)


@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    result = [{'id': notification.id, 'shift_id': notification.shift_id, 'message': notification.message,
               'is_read': notification.is_read, 'created_at': notification.created_at} for notification in notifications]
    return jsonify(result)


def populate_db():
    with app.app_context():
        db.create_all()

        db.session.add(Team(name='Bifrost'))
        db.session.add(Shift(team_id='1', user_id='1', start_time=datetime.datetime.now(), end_time=(datetime.datetime.now() - datetime.timedelta(hours=1))))
        db.session.add(User(name='André', email='lersveen@gmail.com', password='123456'))
        db.session.commit()


if __name__ == '__main__':
    populate_db()
    app.run()

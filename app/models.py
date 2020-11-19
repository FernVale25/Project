from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#The helper association table for users and devices
userDevicesTable = db.Table('UserDevices', 
    db.Column('userID', db.Integer, db.ForeignKey('userTable.id')),
    db.Column('deviceID', db.Integer, db.ForeignKey('deviceTable.id'))
)


#The User Model
#Many users can have many devices
#One user can have many unlocks
class User(UserMixin, db.Model):
    __tablename__= 'userTable'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    userDevices = db.relationship("Device", secondary=userDevicesTable, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        s = ""
        for d in self.devices.devices:
            s += "{}".format(d) + " "
        return '<User {}'.format(self.username) + s + ">"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#The Device model. 
#Many devices can have many users (many-to-many)
#One device can have many unlocks (one-to-many)
class Device(db.Model):
    __tablename__ = 'deviceTable'
    id = db.Column(db.Integer, primary_key=True)
    deviceUsers = db.relationship("User", secondary=userDevicesTable, backref=db.backref('devices', lazy='dynamic'))   
    unlocks = db.relationship('Unlock', backref = 'device', lazy='dynamic') 

    def __repr__(self):
        return '<device_id {}>'.format(self.id)

    #This method is useful for showing all the times a device was unlocked
    def stringUnlocks(self):
        s = "Device ID {}:\n".format(self.id)
        flag = 0
        for u in self.unlocks:
            flag = 1
            username = User.query.filter_by(id=u.user_id).first().username
            s += " " + str(username) + " at " + str(u.timestamp) + "\n"
        if flag == 0:
            return "Device ID {} has not been unlocked in the given timeframe".format(self.id)
        else:
            return s
        
class Unlock(db.Model):
    __tablename__ = 'unlockTable'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    dID = db.Column(db.Integer, db.ForeignKey('deviceTable.id'))
    username = db.Column(db.Integer, db.ForeignKey('userTable.username'))

    def __repr__(self):
        return '<user_id {}'.format(self.user_id) + ' at {}'.format(self.timestamp)
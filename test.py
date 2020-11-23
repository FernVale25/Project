from app.models import User, Device, Unlock
from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
import urllib.parse



meta = MetaData()

#This connects to the azure sql server
params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};" +
        "SERVER=tcp:fau-se.database.windows.net,1433;" +
        "DATABASE=FAUSELOGVIEWER;" +
        "UID=fause;" +
        "PWD=esuaf123!@#;" + 
        "Connection Timeout=30"
        )
engine = create_engine('mssql+pyodbc:///?odbc_connect=' + params, echo=True)
connection = engine.connect()
print('connection is ok')

#This instantiates a session so we can make changes to the database
Session = sessionmaker(bind=engine)
session = Session()

#This is an example of querying to check if a user exists
user = session.query(User).filter_by(username='susan').first()
if user is not None:
        print("The user susan exists")
else:
        print("No joy on user susan")

#This is an example of querying to check if a device exists
device = session.query(Device).filter_by(id='123').first()
if device is not None:
        print("The device 123 exists")
else:
        print("No joy on device 123")

#This is an example of adding an unlock event by user susan to device 123 at time now
unlock = Unlock(dID='123', username='susan')
session.add(unlock)
device.unlocks.append(unlock)
session.commit()
print("You did it! Log onto http://fau-se-logviewer.azurewebsites.net/index with username susan and password cat.")
print("You should see the results of the database addition on the main screen")
print("Be advised that the first attempt to log onto the server may result in a 502 error")
print("This is because Microsoft probably does not commit any resources to maintaining the server until you try to login")
print("Try again and you should get the website")
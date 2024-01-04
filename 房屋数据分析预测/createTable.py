from app import app
from db import db

from model.Usser import User
from model.History import History
from model.Hourse_info import Hourse_info

app.app_context().push()
db.create_all()
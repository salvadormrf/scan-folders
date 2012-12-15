'''
Created on Dec 15, 2012

@author: Salvador Faria
'''

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from celeryconfig import CELERY_RESULT_DBURI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = CELERY_RESULT_DBURI
db = SQLAlchemy(app)

class FileEntry(db.Model):
    __tablename__ = 'fileentry'
    file_size = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(1000), primary_key=True)
    file_type = db.Column(db.String(100), default="")
    file_date_created = db.Column(db.Integer)
    file_date_modified = db.Column(db.Integer)
    
    def __init__(self, file_path, file_size=0, file_type=None, 
                 file_date_created=None, file_date_modified=None):
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.file_date_created = file_date_created
        self.file_date_modified = file_date_modified
        
    def __repr__(self):
        return "%s path=%s size=%s" % (self.__class__.__name__,
                                self.file_path, self.file_size)


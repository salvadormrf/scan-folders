'''
Created on Dec 13, 2012

@author: Salvador Faria
'''

import os
import simplejson

from flask import Flask, render_template, request, jsonify
#from sqlalchemy.exc import SQLAlchemyError

from models import FileEntry, db
from tasks import scan_folder

app = Flask(__name__)

DEFAULT_FOLDER_PATH = "/tmp"

@app.route("/", methods=['GET', 'POST'])
def index():
    tpl_ctx = {}
    
    if request.method == 'POST':
        path = request.form.get('path', "").strip()
        if path == "": path = DEFAULT_FOLDER_PATH
        
        # send task to celery
        scan_folder.delay(path=path)
        tpl_ctx["task_sent"] = True
    
    return render_template("index.html", **tpl_ctx)

@app.route("/api/v<int:api_version>/files")
def files(api_version):
    """ API endpoint to return list of all files """
    
    # TODO pagination
    # we can have lots of data records, so we need json pagination
    try:
        res = db.session.query(FileEntry).all()
    except Exception as e:
        # TODO drill down more on exception type, check SQLAlchemyError
        app.logger.warning("Could not retrive file list, reason: '%s'" % e)
        return json_response({}, 500, "A problem occurred")    
    
    files = [{"path": f.file_path} for f in res]
    return json_response({"files": files})

@app.route("/api/v<int:api_version>/file")
def file_info(api_version):
    """ API endpoint to return information about a single file """
    
    res = None
    path = request.args.get('path', None)
    
    # parameter validation
    if path is None:
        app.logger.debug("Missing 'path' parameter!")
        return json_response({}, 400, "Parameter 'path' is required")
    
    # do database call
    try:
        res = db.session.query(FileEntry).get(path)
    except Exception as e:
        # TODO drill down more on exception type, check SQLAlchemyError
        app.logger.warning("Could not load file '%s' information, reason: '%s'" % (path, e))
        return json_response({}, 500, "A problem occurred")         
    else:
        # check if has found any object
        if res is None:
            app.logger.debug("File with path '%s' not found!" % path)
            return json_response({}, 404, "File not found")
    
    # return object information
    file_info = {
                 "path": res.file_path, 
                 "size": res.file_size, 
                 "created": res.file_date_created,
                 "modified": res.file_date_modified
                 }
    return json_response({"file_info": file_info})

def json_response(json_obj, result_code=200, errors=[]):
    """ Simple utility to wrap "body content" into API response wrapper """
    error_list = errors if isinstance(errors, list) else [errors]
    res = {"result" : json_obj, "result_code": result_code, "errors": error_list}
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)


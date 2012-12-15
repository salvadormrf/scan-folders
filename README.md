##Python Technical Test - Scan local folders
__Using Python, Flask, Celery and SQlite3__

    Using Python, Celery, Flask, and SQLite - could you please create a small web application, which 
    will scan the local folders and get information about the files, size, age, etc. 
    Can you then save it to the database and create 2 API endpoints:
      - list of all files
      - information about single file.
    result should be displayed in JSON format


###How to setup?
    NOTE using python-celery 2.4 (stable on ubuntu packaging)

    sudo apt-get install python-flask python-pysqlite2 python-celery python-sqlalchemy rabbitmq-server
    
    git clone https://github.com/salvadormrf/scan-folders.git
    cd scan-folders
    touch /tmp/test
    python create_db.py 
    celeryd &
    python main.py

    Go to the following URL http://127.0.0.1:5000/

##API DOCUMENTATION

###End points:
    /api/v1/files Return the list of all files and subfolders
    /api/v1/file   Returns file information
        Filter option: path
        How to use: /api/v1/file?path=/tmp/test/a.bng

###Api response:
    result_code: integer, like HTTP response codes
    result: response payload
    erros: list of errors
    
<pre>
{
  "errors": [],
  "result": {
    "file_info": {
      "path": "/tmp/test",
      "created": 1355571883,
      "modified": 1355571883,
      "size": 4096
    }
  },
  "result_code": 200
}
</pre>

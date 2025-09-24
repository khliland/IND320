"""
A simple Flask API server for testing POST and GET. Start from terminal with:

conda activate IND320_2024
python /Users/kristian/Documents/GitHub/IND320/D2D/D2Dbook/3_Data_sources/3_APIs/flask_API.py

Change path to your local install.
"""
from flask import Flask
from flask import request

app = Flask(__name__)

class LocalData(object):
    records = {}

# POST endpoint
@app.post('/api/post/<id>')
def create_entry(id):
    data = request.get_json(force=True)
    LocalData.records[id] = data
    return data

# GET endpoint
@app.get('/api/get/<id>')
def get_record(id):
    return LocalData.records[id]

# UPDATE endpoint
@app.post('/api/update/<id>')
def update_entry(id):
    data = request.get_json(force=True)
    LocalData.records[id] = data
    return data

# DELETE endpoint
@app.delete('/api/delete/<id>')
def delete_entry(id):
    d = LocalData.records[id]
    LocalData.records.pop(id)
    return d

if __name__ == '__main__':
    app.run(port=8000)
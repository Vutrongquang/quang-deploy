import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds131312.mlab.com:31312/c4e10_dat

#mongodb://<dbuser>:<dbpassword>@ds129402.mlab.com:29402/trungtam

host = "ds129402.mlab.com"
port = 29402
db_name = "trungtam"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
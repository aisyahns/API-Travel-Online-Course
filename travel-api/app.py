from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

users = [
    {
        'id': 1,
        'username': u'aisyahns',
        'nama' : u'aisyah',
        'email' : u'aisyah@example.com',
        'password': u'123456'
    },
    {
        'id' : 2,
        'username' : u'susan',
        'nama' : u'susan',
        'email': u'susan@example.com',
        'password' : u'cat'
    }
]

@app.route('/travel/api/v1.0/users', methods=['GET'])
def get_user_all():
    return jsonify({'users': users})

@app.route('/travel/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/travel/api/v1.0/users', methods=['POST'])
def create_user():
    if not request.json or not 'password' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.json.get('username'),
        'email': request.json.get('email'),
        'password': request.json.get('password'),
    }
    users.append(user)
    return jsonify({'user': user}), 201

@app.route('/travel/api/v1.0/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)

    user[0]['username'] = request.args.get('username', user[0]['username']) 
    user[0]['email'] = request.args.get('email', user[0]['email'])   
    user[0]['password'] = request.args.get('password')
    return jsonify({'user': user[0]})

@app.route('/todo/api/v1.0/tasks/<username>', methods=['DELETE'])
def delete_user(username):
    user = [user for user in users if user['username'] == username]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})


travels = [
    {
        "id" : 1,
        "name" : u"Pamitran",
        "asal" : u"Bandung",
        "tujuan" : u"Purwokerto",
        "tanggal_berangkat" : u"17-12-2018",
        "jumlah_kursi" : 8
    }, 
    {
        "id" : 2,
        "name" : u"Pamitran",
        "asal" : u"Purwokerto",
        "tujuan" : u"Bandung",
        "tanggal_berangkat" : u"17-12-2018",
        "jumlah_kursi" : 5
    }
]

@app.route('/travel/api/v1.0/travels', methods=['GET'])
def get_travel_all():
    return jsonify({'travels': travels})

@app.route('/travel/api/v1.0/travels/<asal>/<tujuan>/<tanggal>', methods=['GET'])
def get_travel_syarat(asal,tujuan, tanggal):
    travel = [travel for travel in travels if ((travel['asal'] == asal) & (travel['tujuan'] == tujuan) & (travel['tanggal_berangkat'] == tanggal))]
    if len(travel) == 0:
        abort(404)
    return jsonify({'travel': travel[0]})

@app.route('/travel/api/v1.0/travels', methods=['POST'])
def create_travel():
    if not request.args or not 'tanggal' in request.args:
        abort(400)
    travel = {
        'id': travels[-1]['id'] + 1,
        'name': request.args.get('name'),
        'asal': request.args.get('asal'),
        'tujuan': request.args.get('tujuan'),
        'tanggal_berangkat' :request.args.get('tanggal'),
        'jumlah_kursi' : 8
    }
    kursi = []
    for i in range(1, 9) :
        k = {
            'id' : i,
            'status' : False,
            'id_travel' : travel['id']
        }
        kursi.append(k)
    kursis.append(kursi)
    travels.append(travel)
    return jsonify({'travel': travel}), 201

@app.route('/travel/api/v1.0/travel/<int:id_travel>', methods=['PUT'])
def update_kursi_travel(id_travel):
    i = 0
    for kursi in kursis :
        if kursi['id_travel'] == id_travel:
            if kursi['status'] == False :
                i = i+1
    for travel in travels :
        if travel['id'] == id_travel :
            travel['jumlah_kursi'] = i
    return jsonify({'travel': travel}), 201

@app.route('/travel/api/v1.0/travel/<int:id_travel>', methods=['DELETE'])
def delete_travel(id_travel):
    travel = [travel for travel in travels if travel['id'] == id_travel]
    if len(travel) == 0:
        abort(404)
    delete_kursi(int(id_travel))
    travels.remove(travel[0])
    return jsonify({'result': True})



kursis = [
    {
        "id" : 1,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 2,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 3,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 4,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 5,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 6,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 7,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 8,
        "status" : False,
        "id_travel" : 1
    },
    {
        "id" : 1,
        "status" : True,
        "id_travel" : 2
    },
    {
        "id" : 2,
        "status" : False,
        "id_travel" : 2
    },
    {
        "id" : 3,
        "status" : True,
        "id_travel" : 2
    },
    {
        "id" : 4,
        "status" : True,
        "id_travel" : 2
    },
    {
        "id" : 5,
        "status" : False,
        "id_travel" : 2
    },
    {
        "id" : 6,
        "status" : False,
        "id_travel" : 2
    },
    {
        "id" : 7,
        "status" : False,
        "id_travel" : 2
    },
    {
        "id" : 8,
        "status" : False,
        "id_travel" : 2
    }
]

@app.route('/travel/api/v1.0/kursi', methods=['GET'])
def get_kursi_all():
    return jsonify({'kursi': kursis})

@app.route('/travel/api/v1.0/kursi/<int:travel_id>', methods=['GET'])
def get_kursi_syarat(travel_id):
    kursi_list =[]
    for kursi in kursis :
        if kursi['id_travel'] == travel_id :
            kursi_list.append(kursi)
    if len(kursi_list) == 0:
        abort(404)
    return jsonify({'kursi': kursi_list})

@app.route('/travel/api/v1.0/kursi/<int:id_travel>/<int:id_kursi>', methods=['PUT'])
def update_kursi(id_travel, id_kursi):
    kursi = [kursi for kursi in kursis if ((kursi['id_travel'] == id_travel) & (kursi['id'] == id_kursi))]
    if len(kursi) == 0:
        abort(404)

    kursi[0]['id'] = request.args.get('id', kursi[0]['id']) 
    kursi[0]['status'] = True   
    kursi[0]['id_travel'] = request.args.get('id_travel', kursi[0]['id_travel'])
    return jsonify({'kursi': kursi[0]})

@app.route('/travel/api/v1.0/kursi/<id_travel>', methods=['DELETE'])
def delete_kursi(id_travel):
    hasil =[]
    for kursi in kursis :
        if kursi['id_travel'] == id_travel :
            hasil.append(kursi)
    if len(kursi) == 0:
        abort(404)
    for h in hasil :
        kursis.remove(h)
    return jsonify({'result': True})


pesanans = [
    {
        'id' : 1,
        'nama_penumpang' : 'aisyah',
        'no_identitas' : '18216013',
        'user_id' : 1,
        'travel_id' : 2,
        'kursi' : 3
    },
    {
        'id' : 2,
        'nama_penumpang' : 'aisyah',
        'no_identitas' : '18216013',
        'user_id' : 1,
        'travel_id' : 2,
        'kursi' : 4
    }
]

@app.route('/travel/api/v1.0/pesanan', methods=['GET'])
def get_pesanan_all():
    return jsonify({'pesanan': pesanans})

@app.route('/travel/api/v1.0/pesanan/<int:user_id>', methods=['GET'])
def get_pesanan_syarat(user_id) :
    hasil = []
    for pesanan in pesanans :
        if pesanan['user_id'] == user_id :
            hasil.append(pesanan)
    if len(hasil) == 0:
        abort(404)
    return jsonify({'pesanan': hasil})

@app.route('/travel/api/v1.0/pesanan', methods=['POST'])
def create_pesanan():
    if not request.args or not 'kursi' in request.args:
        abort(400)
    pesanan = {
        'id': pesanans[-1]['id'] + 1,
        'nama_penumpang': request.args.get('nama'),
        'no_identitas': request.args.get('no_identitas'),
        'travel_id' :request.args.get('no.travel'), 
        'kursi' :request.args.get('kursi')
    }
    kursi = update_kursi(int(pesanan['travel_id']), int(pesanan['kursi']))
    pesanans.append(pesanan)
    return jsonify({'pesanan': pesanan})

@app.route('/travel/api/v1.0/pesanan/<int:id_travel>/<int:id_kursi>', methods=['DELETE'])
def delete_pesanan(id_travel, id_kursi):
    pesanan = [pesanan for pesanan in pesanans if ((pesanan['travel_id'] == id_travel) & (pesanan['kursi'] == id_kursi))]
    if len(pesanan) == 0:
        abort(404)
    pesanans.remove(pesanan[0])
    for kursi in kursis :
        if kursi['id'] == id_kursi :
            kursi['status'] == False
    update_kursi_travel(int(id_travel))
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)

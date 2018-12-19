Dokumentasi Travel API

API ini menggunakan library Flask pada bahasa Python yang diimport pada file utama API. Selain itu, beberapa library juga diimport untuk menunjang API ini:
a.  jsonify : mengembalikan respon obyek kepada pengguna dengan menggunakan format json 
b.  abort : menggugurkan permintaan dengan menggunakan kode error http
c.  make_response :  mengkonversi tampilan hasil fungsi ke sebuah instance dari kelas obyek
d.  request : mengambil nilai dari permintaan yang dibuat oleh pengguna


Travel API ini menggunakan 4 resource, yaitu :
1. User : data pengguna yang menggunakan layanan pemesanan Travel. Atribut yang ada pada resource ini sebagai berikut :
    a. id : indeks unik pengenal masing-masing pengguna yang mendaftar
    b. username : nama pengguna yang didaftarkan pada saar 
    c. nama : nama asli dari pengguna
    d. email : email pengguna yang akan digunakan untuk login ke aplikasi
    e. password : password dari akun yang didaftarkan pengguna untuk login
2. Travel : data travel yang disediakan oleh pihak ke-3
    a. id : indeks unik pengenal suatu travel
    b. name : nama dari travel
    c. asal : daerah asal travel akan berangkat 
    d. tujuan : daerah tujuan travel yang akan dituju
    e. tanggal_berangkat : tanggal keberangkatan dari travel
    f. jumlah_kursi : jumlah kursi yang tersedia pada travel tersebut
3. Kursi : data kursi yang ada pada travel. Setiap travel memiliki data kursinya masing-masing 
    a. id : indeks unik pengenal suatu kursi
    b. status : status pemesanan kursi. False jika kursi belum dipesan, True untuk sebaliknya 
    c. id_travel : id dari travel yang memiliki kursi tersebut
    primary key pada resource ini ialah id dan id_travel
4. Pesanan : data pesanan yang terjadi pada aplikasi
    a. id : indeks unik pengenal suatu pesanan
    b. nama_penumpang : nama dari pemesan travel yang didapatkan dari nama pada resource user
    c. no_identitas : nomor identitas dari pengguna yang memesan travel sebagai tanda pengenal saat keberangkatan
    d. user_id : id dari user pemesan
    e. travel_id : id dari travel yang dipesan oleh pengguna
    f. kursi : nomor kursi yang dipesan pengguna


Ada beberapa hal yang perlu diperhatikan pada penggunaan API ini, yaitu sebagai berikut :
1. Penggunaan data pada method belum diintegrasikan dengan database SQLAlchemy sehingga masih menggunakan dictionary yang dibuat secara manual
2. Data kursi tidak dapat dihapus oleh user, hanya dapat terhapus ketika suatu travel dihapus dari data yang ada
3. 


Pada API ini, ada beberapa respon yang diberikan oleh server. Berikut respon yang dimaksud:
1. 200,OK. Permintaan sudah berhasil dilakukan.
2. 201,CREATED. Permintaan sudah dipenuhi dan menghasilkan 1 atau lebih resource dibuat. 
2. 400,BAD REQUEST ERROR. Permintaan yang diminta ke server tidak benar, terkorup atau server tidak bisa memahami permintaan tersebut. 
3. 404,NOT FOUND. Server tidak memahami permintaan yang dilakukan oleh pengguna. Pada respon 404, server akan memunculkan respon json yang bertuliskan : ("error : not found")



Travel API menyediakan beberapa method yang dapat digunakan oleh pihak ke-3 untuk pengembangan aplikasinya. Berikut penjelasan method yang disediakan API ini:
1.  @app.route('/travel/api/v1.0/users', methods=['GET'])
    def get_user_all():
        return jsonify({'users': users})

    Method get_user_all akan mengembalikan semua user yang terdaftar pada aplikasi. Method ini menggunakan method http 'GET'.
    Pengguna dapat menggunakan method ini dengan cara memanggil http://localhost:5000/travel/api/v1.0/users.
    Hasil yang akan didapat oleh pengguna ialah sebagai berikut :

    { 
        "users": [ 
            { 
                "email": "aisyah@example.com", 
                "id": 1, "nama": "aisyah", 
                "password": "123456", 
                "username": "aisyahns" 
            }, 
            { 
                "email": "susan@example.com", 
                "id": 2, "nama": "susan", 
                "password": "cat", 
                "username": "susan" 
            } 
        ] 
    }

    Hasil yang ditampilkan menggunakan format json.

2.  @app.route('/travel/api/v1.0/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = [user for user in users if user['id'] == user_id]
        if len(user) == 0:
            abort(404)
        return jsonify({'user': user[0]})

    Method ini menggunakan method 'get' http.
    Method get_user digunakan untuk mengambil data user terhadap suatu id tertentu yang dimasukan oleh pengguna. 
    Pengguna dapat memanggil method ini menggunakan url http://localhost:5000/travel/api/v1.0/users/2.
    2 pada contoh url di atas merupakan id dari user yang akan diambil datanya. 
    Id tersebut haruslah berupa angka karena pada pendefinisian @app.route, user_id bertipekan integer. 

    Hasil yang didapat pengguna ialah :
    { 
        "user": { 
            "email": "susan@example.com", 
            "id": 2, 
            "nama": "susan", 
            "password": "cat", 
            "username": "susan" 
        } 
    }


    user = [user for user in users if user['id'] == user_id]
    >>  Pseudocode ini mencari data yang sesuai dari data dictionary yang ada disesuaikan dengan user_id yang dimasukan oleh pengguna. 
        Hasil pencarian disimpan pada variable user. 

    if len(user) == 0:
        abort(404)
    >>  Jika hasil dari pencarian yang sudah disimpan pada variable user panjangnya 0, maka akan gagal yang diterima oleh error handler 404.

    return jsonify({'user': user[0]})
    >>  Method akan mengembalikan data user dari hasil yang pertama kali didapat dengan menggunakan format json

3.  @app.route('/travel/api/v1.0/users', methods=['POST'])
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
    
    Method ini digunakan untuk membuat data user baru. Ia memanfaatkan method 'post' http. 
    Pemanggilan method ini dapat menggunakan aplikasi bantuan yaitu POSTMAN dan menggunakan method POST serta url berikut sebagai contoh :
    http://localhost:5000/travel/api/v1.0/users?username=bububu&nama=bubububu&email=bubu@example.com&password=123456789.
    Pemanggilan method ini hanya dapat dilakukan jika menggunakan argumen yang dituliskan pada url yang dipanggil pada @app.route.
    
    Hasil yang didapat pengguna ialah :
    { 
        "user": { 
            "email": "bubu@example.com", 
            "id": 4, 
            "nama": "bubububu", 
            "password": "123456789", 
            "username": "bububu" 
        } 
    }


    if not request.json or not 'password' in request.json:
        abort(400)
    >>  Pseudocode ini memastikan bahwa permintaan pengguna berupa format json atau atribut 'password' harus terdapat pada permintaan yang dilakukan pengguna.
        Jika tidak sesuai dengan pesyaratan di atas, maka akan diteruskan ke halaman error 400. 
    
    user = {
            'id': users[-1]['id'] + 1,
            'username': request.args.get('username'),
            'email': request.args.get('email'),
            'password': request.args.get('password'),
        }
    >>  variable user menyimpan masukan atribut dari pengguna. Masukan dari pengguna didapat dari method request.args pada masing-masing atribut.
        Atribut 'id' akan tergenerate secara otomatis sesuai dengan data id pada dictionary user yang ada. 
    
    users.append(user)
    >>  User yang sudah menyimpan data dari masukan pengguna di append, atau ditambahkan ke dictionary users yang ada. 

    return jsonify({'user': user}), 201
    >>  Method akan mengembalikan data user tersebut dengan format json dan menggunakan respon http 201


4.  @app.route('/travel/api/v1.0/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = [user for user in users if user['id'] == user_id]
        if len(user) == 0:
            abort(404)

        user[0]['username'] = request.args.get('username', user[0]['username']) 
        user[0]['nama'] = request.args.get('nama', user[0]['nama'])
        user[0]['email'] = request.args.get('email', user[0]['email'])   
        user[0]['password'] = request.args.get('password')
        return jsonify({'user': user[0]})

    Method update_user digunakan untuk mengupdate data user yang dimasukan oleh pengguna. 
    Seperti pada method sebelumnya, pemanggilan method ini menggunakan argumen pada url yang dipanggil oleh pengguna. 
    Berikut contoh pemanggilan method ini dengan menggunakan POSTMAN method PUT : 
    http://localhost:5000/travel/api/v1.0/users/3?password=haihai.

    URL di atas akan mengubah data user pada id 3. 3 di sini berarti user_id pada format @app.route, ia harus angka karena didefinisikan sebagai integer.
    Lalu, data yang dapat diubah ialah password dengan tipe string. Password yang diset baru pada url di atas adalah 'haihai'.

    Hasil yang didapat pengguna ialah :
    { 
        "user": { 
            "email": "bubu@example.com", 
            "id": 3, 
            "nama": "bubububu", 
            "password": "haihai", 
            "username": "bububu" 
        } 
    }

    
    user = [user for user in users if user['id'] == user_id]
    >>  Pseudocode ini mencari data id dari user yang sesuai dengan user_id yang diminta oleh pengguna. Hasil ini disimpan pada variable user.

    if len(user) == 0:
        abort(404)
    >>  Jika panjang dari hasil yang didapat 0, maka menandakan bahwa tidak ada data user yang cocok dengan user_id yang diminta. 
        Jika terjadi hal tersebut, maka akan diteruskan ke halaman error 404. 

    user[0]['username'] = request.args.get('username', user[0]['username']) 
    user[0]['nama'] = request.args.get('nama', user[0]['nama'])
    user[0]['email'] = request.args.get('email', user[0]['email'])   
    user[0]['password'] = request.args.get('password')
    return jsonify({'user': user[0]})
    >> Pseudocode ini menset masing-masing atribut user dengan menggunakan data user yang dipunya sebelumnya (ex : user[0]['username']). 
        Pengecualian terjadi pada atribut password yang diambil nilainya dari masukan url pengguna. 
        Method ini akan mengembalikan data user yang baru.

5.  @app.route('/travel/api/v1.0/users/<username>', methods=['DELETE'])
    def delete_user(username):
        user = [user for user in users if user['username'] == username]
        if len(user) == 0:
            abort(404)
        users.remove(user[0])
        return jsonify({'result': True})

    Method ini digunakan untuk menghapus data sebuah user, sesuai dengan username yang dimasukan oleh pengguna.
    Ia menggunakan method 'delete' http. Tipe dari username yang ditulis pada url haruslah string. 
    Pemanggilan method ini dapat dicontohkan sebagai berikut yang dilakukan dengan POSTMAN :
    http://localhost:5000/travel/api/v1.0/users/aisyahns.

    Hasil yang akan didapat pengguna :
    { "result": true }
    Dan data user dari username 'aisyahns' terhapus pada dictionary users.


    user = [user for user in users if user['username'] == username]
    >>  Pseudocode ini mencari data user yang username- nya sesuai dengan username yang dimasukan oleh pengguna lalu disimpan pada variable user. 

    if len(user) == 0:
        abort(404)
    >>  Jika panjang dari hasil yang didapat 0, maka menandakan bahwa tidak ada data user yang cocok dengan username yang diminta. 
        Jika terjadi hal tersebut, maka akan diteruskan ke halaman error 404. 

    users.remove(user[0])
    >>  Pseudocode ini akan menghapus data dari user hasil pencarian di atas dari dictionary users.

    return jsonify({'result': True})
    >>  Jika penghapusan berhasil dilakukan (tidak diteruskan ke error handler 404), maka akan dikembalikan format json yang tulisannya 
        "result" : True
    

6.  @app.route('/travel/api/v1.0/travels', methods=['GET'])
    def get_travel_all():
        return jsonify({'travels': travels})

    Method get_travel_all akan mengembalikan semua travel yang tersedia pada aplikasi. Method ini menggunakan method http 'GET'.
    Pengguna dapat menggunakan method ini dengan cara memanggil http://localhost:5000/travel/api/v1.0/travels.
    Hasil yang akan didapat oleh pengguna ialah sebagai berikut :

    { 
        "travels": [ 
            { 
                "asal": "Bandung", 
                "id": 1, 
                "jumlah_kursi": 8, 
                "name": "Pamitran", 
                "tanggal_berangkat": "17-12-2018", 
                "tujuan": "Purwokerto" 
            }, 
            { 
                "asal": "Purwokerto", 
                "id": 2, 
                "jumlah_kursi": 5, 
                "name": "Pamitran", 
                "tanggal_berangkat": "17-12-2018", 
                "tujuan": "Bandung" 
            } 
        ] 
    }


7.  @app.route('/travel/api/v1.0/travels/<asal>/<tujuan>/<tanggal>', methods=['GET'])
    def get_travel_syarat(asal,tujuan, tanggal):
        travel = [travel for travel in travels if ((travel['asal'] == asal) & (travel['tujuan'] == tujuan) & (travel['tanggal_berangkat'] == tanggal))]
        if len(travel) == 0:
            abort(404)
        return jsonify({'travel': travel[0]})

    Method ini akan mengeluarkan data travel yang sesuai dengan syarat yang diberikan oleh pengguna. 

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


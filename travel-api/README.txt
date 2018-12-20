Dokumentasi Travel API

API ini menggunakan library Flask pada bahasa Python yang diimport pada file utama API. Selain itu, beberapa library juga diimport untuk menunjang API ini:
a.  jsonify : mengembalikan respon obyek kepada pengguna dengan menggunakan format json 
b.  abort : menggugurkan permintaan dengan menggunakan kode error http
c.  make_response :  mengkonversi tampilan hasil fungsi ke sebuah instance dari kelas obyek
d.  request : mengambil nilai dari permintaan yang dibuat oleh pengguna

Untuk pengujian method digunakan aplikasi POSTMAN yang dapat didownload pada link berikut : https://www.getpostman.com/

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
    Syarat yang akan dimasukan oleh pengguna ialah sebagai berikut :
    a.  asal : asal daerah keberangkatan travel. Formatnya string.
    b.  tujuan :  tujuan daerah perjalanan travel. Formatnya string.
    c.  tanggal : tanggal keberangkatan travel. Formatnya dd-mm-yyyy. Contoh 18-12-2018

    Berikut contoh pemanggilan method ini. 
    http://localhost:5000/travel/api/v1.0/travels/Purwokerto/Bandung/17-12-2018

    Hasil yang akan didapat oleh pengguna adalah data travel yang memiliki syarat tersebut.
    { 
        "travel": { 
            "asal": "Purwokerto", 
            "id": 2, 
            "jumlah_kursi": 5, 
            "name": "Pamitran", 
            "tanggal_berangkat": "17-12-2018", 
            "tujuan": "Bandung" 
        } 
    }


    travel = [travel for travel in travels if ((travel['asal'] == asal) & (travel['tujuan'] == tujuan) & (travel['tanggal_berangkat'] == tanggal))]
    >>  Pseudocode ini mencari data travel yang sesuai dengan asal, tujuan dan tanggal yang dimasukan oleh pengguna lalu disimpan ke variable travel.

    if len(travel) == 0:
        abort(404)
    >>  Jika panjang dari hasil yang didapat 0, maka menandakan bahwa tidak ada data user yang cocok dengan username yang diminta. 
        Jika terjadi hal tersebut, maka akan diteruskan ke halaman error 404. 

    return jsonify({'travel': travel[0]})
    >>  Method akan mengembalikan hasil pencarian data yang dilakukan dengan format json.


8.  @app.route('/travel/api/v1.0/travels', methods=['POST'])
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


    Method ini akan melakukan pembuatan data user sesuai dengan data masukan pengguna. Ada beberapa data yang harus dimasukan pengguna dengan method POST :
    name, asal, tujuan dan tanggal keberangkatan. Untuk id dan jumlah kursi, datanya sudah default dari server.
    Setelah dictionary travel dibentuk, dibuat pula dictionary kursi yang baru. Data id dan status diset secara default oleh method. 
    Data id_travel dari kursi didapat dari masukan pengguna pada data travel sebelumnya.

    Setelah itu data travel dan kursi tadi ditambahkan ke dictionary travels dan kursis dengan method append.

    Method akan mengembalikan data travel dengan http respon 201.

    Contoh pemanggilan method menggunakan POSTMAN dan method POST http :
    http://localhost:5000/travel/api/v1.0/travels?name=Karuna&asal=Purwokerto&tujuan=Bandung&tanggal=22-12-2018
    Pemanggilan hanya dapat dilakukan dengan format url, tidak dapat menggunakan format json. 

    Hasil yang didapat oleh pengguna :
    { 
        "travel": { 
            "asal": "Purwokerto", 
            "id": 3, 
            "jumlah_kursi": 8, 
            "name": Karuna, 
            "tanggal_berangkat": "22-12-2018", 
            "tujuan": "Bandung" 
        } 
    }


9.  @app.route('/travel/api/v1.0/travel/<int:id_travel>', methods=['PUT'])
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

    Method update_kursi_travel akan mengupdate data jumlah_kursi dari travel. 
    Method ini memerlukan data id_travel yang akan diupdate dari pengguna dengan menggunakan angka karena diidentifikasi dengan tipe integer.
    
    Lalu ia akan melakukan looping terhadap data kursi untuk mencari data yang sesuai dengan id_travel.
    Setelah menemukan data yang sesuai, dilihat apakah status dari kursi tersebut False atau True. 
    
    Jika True, maka nilai i akan dinaikan nilainya. 
    False berarti kursi tersebut belum ada yang memesan, dan True jika sudah ada yang memesan. 

    Hasil penghitungan jumlah kursi dengan status False disimpan dalam variable i.
    Setelah penghitungan selesai dilakukan, method akan melakukan pencarian terhadap data travel yang sesuai dengan id_travel dan akan melakukan peng-update-an
    data jumlah_kursi dari hasil penghitungan. 

    Method akan mengeluarkan data travel yang di-update tersebut dengan http respon 201. 

    Berikut contoh pemanggilan method ini dengan menggunakan POSTMAN :
    http://localhost:5000/travel/api/v1.0/travel/2.
    
    Hasil yang akan didapat oleh pengguna ialah :
    { 
        "travel": { 
            "asal": "Purwokerto", 
            "id": 2, 
            "jumlah_kursi": 5, 
            "name": "Pamitran", 
            "tanggal_berangkat": "17-12-2018", 
            "tujuan": "Bandung" 
        } 
    }


10. @app.route('/travel/api/v1.0/travel/<int:id_travel>', methods=['DELETE'])
    def delete_travel(id_travel):
        travel = [travel for travel in travels if travel['id'] == id_travel]
        if len(travel) == 0:
            abort(404)
        delete_kursi(int(id_travel))
        travels.remove(travel[0])
        return jsonify({'result': True})

    Method ini akan menghapus data dari travel sesuai dengan id_travel yang dimasukan oleh pengguna. 
    Masukan pengguna harus berupa angka karena diidentifikasi sebagai integer. 
    Method ini menggunakan method 'DELETE' http.

    Contoh penggunaan method ini ialah :
    http://localhost:5000/travel/api/v1.0/travel/2

    Hasil yang didapat pengguna :
    { "result": true }


    travel = [travel for travel in travels if travel['id'] == id_travel]
    >>  Pseudocode ini akan mencari data travel yang sesuai dengan id_travel

    if len(travel) == 0:
        abort(404)
    >>  jika tidak ada data travel yang sesuai, maka akan diteruskan ke error page 404

    delete_kursi(int(id_travel))
    >>  Method akan memanggil method delete_kursi dengan parameter id_travel yang didapat dari masukan pengguna

    travels.remove(travel[0])
    >>  menghapus data travel hasil dari dictionary travels

    return jsonify({'result': True})
    >>  Mengembalikan format json dengan tulisan {'result' : True }

11. @app.route('/travel/api/v1.0/kursi', methods=['GET'])
    def get_kursi_all():
        return jsonify({'kursi': kursis}) 

    Method get_kursi_all akan mengembalikan semua kursi yang tersedia pada travel. Method ini menggunakan method http 'GET'.
    Pengguna dapat menggunakan method ini dengan cara memanggil http://localhost:5000/travel/api/v1.0/travels.
    Hasil yang akan didapat oleh pengguna ialah sebagai berikut :

    { "kursi": [ 
        { "id": 1, "id_travel": 1, "status": false }, 
        { "id": 2, "id_travel": 1, "status": false }, 
        { "id": 3, "id_travel": 1, "status": false }, 
        { "id": 4, "id_travel": 1, "status": false }, 
        { "id": 5, "id_travel": 1, "status": false }, 
        { "id": 6, "id_travel": 1, "status": false }, 
        { "id": 7, "id_travel": 1, "status": false }, 
        { "id": 8, "id_travel": 1, "status": false }, [ 
        { "id": 1, "id_travel": 2, "status": true }, 
        { "id": 2, "id_travel": 2, "status": false }, 
        { "id": 3, "id_travel": 2, "status": true }, 
        { "id": 4, "id_travel": 2, "status": true }, 
        { "id": 5, "id_travel": 2, "status": false }, 
        { "id": 6, "id_travel": 2, "status": false }, 
        { "id": 7, "id_travel": 2, "status": false }, 
        { "id": 8, "id_travel": 2, "status": false } ] ] }


12. @app.route('/travel/api/v1.0/kursi/<int:travel_id>', methods=['GET'])
    def get_kursi_syarat(travel_id):
        kursi_list =[]
        for kursi in kursis :
            if kursi['id_travel'] == travel_id :
                kursi_list.append(kursi)
        if len(kursi_list) == 0:
            abort(404)
        return jsonify({'kursi': kursi_list})

    Method ini akan mengembalikan semua data kursi yang ada pada id_travel tertentu yang dimasukan oleh pengguna. 
    id_travel yang dimasukan haruslah angka atau bertipe integer.
    Jika tidak ditemukan data kursi yang sesuai, maka akan diteruskan ke error handler http 404.

    Pemanggilan dapat dilakukan sebagai berikut :
    http://localhost:5000/travel/api/v1.0/kursi/2

    Hasil yang didapat pengguna :
    { "kursi": [ 
        { "id": 1, "id_travel": 2, "status": true }, 
        { "id": 2, "id_travel": 2, "status": false }, 
        { "id": 3, "id_travel": 2, "status": true }, 
        { "id": 4, "id_travel": 2, "status": true }, 
        { "id": 5, "id_travel": 2, "status": false }, 
        { "id": 6, "id_travel": 2, "status": false }, 
        { "id": 7, "id_travel": 2, "status": false }, 
        { "id": 8, "id_travel": 2, "status": false } ] }


13. @app.route('/travel/api/v1.0/kursi/<int:id_travel>/<int:id_kursi>', methods=['PUT'])
    def update_kursi(id_travel, id_kursi):
        kursi = [kursi for kursi in kursis if ((kursi['id_travel'] == id_travel) & (kursi['id'] == id_kursi))]
        if len(kursi) == 0:
            abort(404)

        kursi[0]['id'] = request.args.get('id', kursi[0]['id']) 
        kursi[0]['status'] = True   
        kursi[0]['id_travel'] = request.args.get('id_travel', kursi[0]['id_travel'])
        return jsonify({'kursi': kursi[0]})
    
    Method ini akan melakukan pembaharuan data status kursi pada sebuah id_travel yang dimasukan oleh pengguna. 
    Masukan dari pengguna berupa angka yang bertipe integer.

    Method akan melakukan pencarian data kursi yang sesuai dengan masukan id_travel dan id_kursi dari pengguna.
    Jika tidak ditemukan data yang sesuai, maka akan diteruskan ke error handler 404.

    Setelah itu akan dilakukan pen-set-an atribut pada kursi. Namun, atribut id dan id_travel didapat dari data kursi sebelumnya. 
    Hanya data status dari kursi yang diubah, dari False menjadi True, yang berarti kursi itu dipesan oleh pengguna. 

    Pemanggilan method dapat dilakukan sebagai berikut :
    http://localhost:5000/travel/api/v1.0/kursi/2/8

    Hasil yang akan didapat oleh pengguna :
    { "kursi": { 
        "id": 8, "id_travel": 2, "status": true } }


14. @app.route('/travel/api/v1.0/kursi/<id_travel>', methods=['DELETE'])
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

    Method ini akan menghapus semua data kursi yang ada pada travel dengan id_travel tertentu. id_travel bertipe integer.
    Method akan melakukan pencarian data kursi yang sesuai dengan id_travel.
    Jika tidak ditemukan data yang sesuai maka akan diteruskan ke error handler http 404.
    Setelah ditemukan data yang sesuai, maka datanya akan dihapus dari dictionary kursis. 
    Lalu, method akan mengembalikan dengan format json { 'result' : True }

    Pemanggilan penghapusan kursi pada id_travel 2 ialah :
    http://localhost:5000/travel/api/v1.0/kursi/2

    Hasil yang akan didapat pengguna :
    { "result": true }


15. @app.route('/travel/api/v1.0/pesanan', methods=['GET'])
    def get_pesanan_all():
        return jsonify({'pesanan': pesanans})

    Method get_pesanan_all akan mengembalikan semua pesanan yang dilakukan pada travel. Method ini menggunakan method http 'GET'.
    Pengguna dapat menggunakan method ini dengan cara memanggil http://localhost:5000/travel/api/v1.0/pesanan.
    Hasil yang akan didapat oleh pengguna ialah sebagai berikut :

    { "pesanan": [ { 
        "id": 1, "kursi": 3, 
        "nama_penumpang": "aisyah", 
        "no_identitas": "18216013", 
        "travel_id": 2, 
        "user_id": 1 }, { 
        "id": 2, 
        "kursi": 4, 
        "nama_penumpang": 
        "aisyah", 
        "no_identitas": "18216013", 
        "travel_id": 2, "user_id": 1 } ] 
    }

16. @app.route('/travel/api/v1.0/pesanan/<int:user_id>', methods=['GET'])
    def get_pesanan_syarat(user_id) :
        hasil = []
        for pesanan in pesanans :
            if pesanan['user_id'] == user_id :
                hasil.append(pesanan)
        if len(hasil) == 0:
            abort(404)
        return jsonify({'pesanan': hasil})

    Method ini akan mengembalikan data semua pesanan yang dipesan oleh user_id tertentu. user_id tersebut merupakan masukan dari pengguna dalam bentuk angka atau integer.

    Method akan mencari data pesanan yang sesuai.
    Jika tidak ditemukan data yang sesuai, maka akan diteruskan ke error handler http 404.

    Method akan mengembalikan data semua pesanan dalam format json.

    Berikut pemanggilan method ini :
    http://localhost:5000/travel/api/v1.0/pesanan/1
    1 adalah id_user yang diminta pengguna. 

    Hasil yang akan didapat oleh pengguna :
    { "pesanan": [ { 
        "id": 1, 
        "kursi": 3, 
        "nama_penumpang": "aisyah", 
        "no_identitas": "18216013", 
        "travel_id": 2, 
        "user_id": 1 }, { 
        "id": 2, 
        "kursi": 4, 
        "nama_penumpang": "aisyah", 
        "no_identitas": "18216013", 
        "travel_id": 2, 
        "user_id": 1 } ] }


17. @app.route('/travel/api/v1.0/pesanan', methods=['POST'])
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

    Method ini digunakan untuk membuat data pesanan baru dari pengguna. 
    Pertama kali akan dilakukan pengecekan apakah permintaan yang dilakukan dalam bentuk url atau bukan dan apakah parameter kursi ada pada permintaan.
    Jika tidak sesuai, maka akan diteruskan ke error handler 400. 

    list pesanan akan dibuat sesuai dengan masukan dari pengguna. Variable yang dimasukan oleh pengguna ialah nama untuk nama_penumpang, 
    no_identitas, no.travel dan kursi.
    Atribut id akan secara otomatis ditambahkan ketika permintaan dilakukan.

    Setelah itu dilakukan pengupdatean data kursi dengan pemanggilan method update_kursi dengan parameter travel_id dan kursi yang didapat sebelumnya.
    dictionary pesanans akan ditambahkan data pesanan tersebut.

    Method akan mengembalikan data pesanan yang dibuat. 

    Pemanggilan dapat dilakukan sebagai berikut.
    http://localhost:5000/travel/api/v1.0/pesanan?nama=qoni&no_identitas=18216023&no.travel=1&kursi=5

    Hasil yang akan didapat oleh pengguna ialah :
    { "pesanan": { 
        "id": 3, 
        "kursi": "5", 
        "nama_penumpang": "qoni", 
        "no_identitas": "18216023", 
        "travel_id": "1" } }


18. @app.route('/travel/api/v1.0/pesanan/<int:id_travel>/<int:id_kursi>', methods=['DELETE'])
    def cancel_pesanan(id_travel, id_kursi):
        pesanan = [pesanan for pesanan in pesanans if ((pesanan['travel_id'] == id_travel) & (pesanan['kursi'] == id_kursi))]
        if len(pesanan) == 0:
            abort(404)
        pesanans.remove(pesanan[0])
        for kursi in kursis :
            if kursi['id'] == id_kursi :
                kursi['status'] == False
        update_kursi_travel(int(id_travel))
        return jsonify({'result': True})

    Method ini dilakukan untuk membatalkan pesanan dengan menghapus data tersebut pada data pesanans yang ada.
    Masukan dari pengguna ialah id_travel dengan tipe integer dan id_kursi dengan tipe integer.

    Method akan melakukan pencarian data travel yang sesuai dengan masukan pengguna.
    Jika tidak ditemukan maka akan diteruskan ke error handler http 404.

    Setelah ditemukan data yang sesuai, maka data tersebut akan dihapus dari data dictionary pesanan dengan menggunakan method remove.

    Data status dari kursi pun akan diubah yang tadinya True menjadi False.
    Lalu dilakukan update_kursi_travel yang mana akan mengupdate jumlah kursi pada suatu id_travel.

    Method akan mengembalikan dengan format json { 'result' : True }

    Berikut pemanggilan dari method ini :
    http://localhost:5000/travel/api/v1.0/pesanan/2/3

    Hasil dari pemanggilan tersebut ialah :
    { "result": true }

19. @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    Method ini akan mengatur hasil dari pemanggilan error handler 404 dengan menggunakan format json.

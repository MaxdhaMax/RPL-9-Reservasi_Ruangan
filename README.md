# RPL-9-Reservasi_Ruangan

# **RoomBook**
> RoomBook adalah sebuah website reservasi ruangan di IPB. Situs ini dapat membantu civitas IPB dalam mencari informasi ruangan serta memberikan layanan pemesanan ruangan yang tersentralisasi.

* **Link Aplikasi RoomBook**

https://roombook.pythonanywhere.com/

# **Laporan Akhir Projek**
* KOM 331 | Rekayasa Perangkat Lunak | P2
* Kelompok 9

# **Dibimbing Oleh :**
* Ali Naufal Ammarullah
* Levina S
* Muhammad Fauzan Ramadhan

# **Tim Pengembang RoomBook**
| Nama | NIM | Role |
| ---- | --- | ---- |
| Jevon Sanoturia | G64190056 | UI/UX Reseacher |
| Muammar Naufal Pramudya | G64190057 | Front-end Developer |
| Muhammad Dafa Athaullah | G64190073 | Back-end Developer |
| Maxdha Maxiwinata | G64190105 | Front-end Developer |

# **Latar Belakang**
> Institut Pertanian Bogor memiliki banyak organisasi dan UKM untuk menjadi kegiatan ekstrakurikuler mahasiswa di luar pembelajaran biasa. Organisasi dan UKM ini seringkali menggelar acara di lingkungan kampus. Oleh karena itu, reservasi ruangan menjadi hal yang dibutuhkan. Sayangnya, reservasi ruangan di IPB masih memiliki banyak masalah, kurangnya akses informasi tentang ruangan yang bisa direservasi, tata cara dan birokrasi reservasi yang tidak jelas, harga yang kurang transparan, dan penanggung jawab ruangan yang susah dihubungi menjadi hal-hal yang mempersulit mahasiswa untuk menggunakan ruangan yang ada di IPB, terutama untuk mahasiswa baru yang belum memiliki banyak pengalaman. Solusi dari masalah ini adalah sentralisasi informasi dan pemesanan reservasi ruangan, penerapan dari solusi ini adalah dengan dibuatnya ​web application khusus untuk mencari informasi atau reservasi ruangan yang ada di IPB

# **Tujuan**
* Mempermudah dalam reservasi ruangan yang tersedia di lingkup kampus IPB.
* Mempermudah mahasiswa dalam mencari informasi tentang ruangan yang terletak di IPB

# **Spesifikasi teknis lingkungan pengembangan**
**1. Software**
* **Framework:** Bootstrap, React, dan Flask
* **Database:** MySQL
* **Server:** Apache
* **TextEditor/IDE:** Visual Studio Code atau SublimeText3

**2. Hardware**
* **Ram :** 4gb
* **Prosesor :** 2.5GHz
* **Graphiccard :** NvidiaGeForceGT930MX2GB

**3. Tech Stack**
* **Version Control and Collaboration Platform :** Github,Trello
* **Teknologi :** CSS, HTML, JavaScript, dan Python

# **Hasil dan pembahasan**

### **User Stories**
* Sebagai RoomBook User , saya perlu memilih ruangan yang tersedia di platform sehingga saya dapat melakukan reservasi
* Sebagai Pengembang Aplikasi Web RoomBook , kami ingin dapat memudahkan civitas IPB University dalam proses reservasi ruangan di IPB sehingga kami dapat membantu mencarikan ruangan di IPB University yang dapat direservasi untuk segala macam keperluan

### **Use Case Diagram**
![](https://imgur.com/YbKzxmr.png)

### **Activity Diagram**
![](https://imgur.com/3Mxl0a1.png)

### **Class Diagram**
![](https://i.imgur.com/R9SddAY.png)

### **Entity Relationship Diagram**
![](https://i.imgur.com/U5XNoRo.png)

### **Architecture Diagram**
![](https://i.imgur.com/yliT3k5.png)

### **Fungsi Utama yang Dikembangkan**
1. **Pencarian Ruangan**, pengguna dapat menggunakan fitur ini untuk mencari ruangan yang ingin dipesan.
![](https://i.imgur.com/Ltz5zOm.png)

2. **Informasi Ruangan**, pengguna dapat mengetahui informasi ruangan seperti gambaran mengenai ruangan, lokasi dari ruangan, harga, serta kontak dari penanggung jawab ruangan.
![](https://i.imgur.com/xOpQAD0.png)

3. **Memilih Tanggal Pemesanan**, pengguna dapat menentukan tanggal kapan ruangan ingin dipesan serta durasi dalam satuan hari. Tak hanya itu pengguna juga dapat mengetahui ketersediaan ruangan.
![](https://i.imgur.com/jCBcFpL.png)

4. **Informasi Pemesan**, pengguna akan diminta untuk mengisi form, seperti nama pemesan, nama event, nomor telepon,dan email sehingga lebih mudah dihubungi oleh penanggungjawab ruangan. Pengguna juga dapat memilih metode pembayaran.
![](https://i.imgur.com/Mj3K3EC.png)

5. **Confirmation**, pengguna akan diminta untuk mengkonfirmasi pesanan yang baru saja dibuat. Pengguna juga akan diberi tahu langkah-langkah yang diperlukan untuk pembayaran.
![](https://i.imgur.com/Kg4Aa9K.png)


6. **Waiting Payment**, pengguna dapat melihat status dari pesanan yang telah dibuat.
![](https://i.imgur.com/DTCBStX.png)

7. **Book History**, pengguna dapat melihat historis pesanan yang pernah dibuat.
![](https://i.imgur.com/XfESaya.png)

## How to Run
1. Download dan install [python](https://www.python.org/downloads/)
2. Install pip, ini [tutorialnya](https://www.liquidweb.com/kb/install-pip-windows/)
3. Clone repository ini
   - Buka terminal
   - cd ke directory yang diinginkan
   - Lakukan command `git clone https://github.com/MaxdhaMax/RPL-9-Reservasi_Ruangan.git RoomBook`
4. Copy file .env yang diberikan ke folder `WebApp` di `RoomBook\WebApp`
5. Install requirementnya
   - `cd RoomBook`
   - `pip install -r requirements.txt`
6. Buat databasenya (cukup jalankan ini sekali saja)
   - `python createdatabase.py`
7. Semua selesai, tinggal jalankan program
   - `python run.py`, jika ingin menjalankan programnya lagi, hanya tinggal lakukan command ini lagi
8. Buka alamat ini di web browser `http://127.0.0.1:5000/`

## Mengedit tampilan website
Buka file RoomBook yang sudah di clone tadi, lalu masuk ke directory
```
...\RoomBook\WebApp\templates
```
Itu adalah tempat untuk mengedit html yang ada, untuk dasar template htmlnya adalah `base.html`

Untuk CSS, masuk ke directory:
```
...\RoomBook\WebApp\static\styles
```


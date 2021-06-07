# RPL-9-Reservasi_Ruangan

# **RoomBook**
> RoomBook adalah sebuah website reservasi ruangan di IPB. Situs ini dapat membantu civitas IPB dalam mencari informasi ruangan serta memberikan layanan pemesanan ruangan yang tersentralisasi.

* **Link Aplikasi RoomBook**

https://roombook.pythonanywhere.com/

# **Laporan Akhir Projek**
* KOM 331 | Rekayasa Perangkat Lunak | P2
* Kelompok 9

# **Dibimbing Oleh :**
* 
* 

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


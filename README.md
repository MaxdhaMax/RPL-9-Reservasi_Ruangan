# **RoomBook**
![](https://i.imgur.com/IipwvCl.jpg)

> RoomBook adalah sebuah website reservasi ruangan di IPB. Situs ini dapat membantu civitas IPB dalam mencari informasi ruangan serta memberikan layanan pemesanan ruangan yang tersentralisasi.
* **Link Aplikasi RoomBook**

https://roombook.pythonanywhere.com/

## **Laporan Akhir Projek**
* KOM 331 | Rekayasa Perangkat Lunak | P2
* Kelompok 9

## **Dibimbing Oleh :**
* Ali Naufal Ammarullah
* Levina S
* Muhammad Fauzan Ramadhan

## **Tim Pengembang RoomBook**
| Nama | NIM | Role |
| ---- | --- | ---- |
| Jevon Sanoturia | G64190056 | UI/UX Reseacher |
| Muammar Naufal Pramudya | G64190057 | Front-end Developer |
| Muhammad Dafa Athaullah | G64190073 | Back-end Developer |
| Maxdha Maxiwinata | G64190105 | Front-end Developer |

## **Latar Belakang**
> Institut Pertanian Bogor memiliki banyak organisasi dan UKM untuk menjadi kegiatan ekstrakurikuler mahasiswa di luar pembelajaran biasa. Organisasi dan UKM ini seringkali menggelar acara di lingkungan kampus. Oleh karena itu, reservasi ruangan menjadi hal yang dibutuhkan. Sayangnya, reservasi ruangan di IPB masih memiliki banyak masalah, kurangnya akses informasi tentang ruangan yang bisa direservasi, tata cara dan birokrasi reservasi yang tidak jelas, harga yang kurang transparan, dan penanggung jawab ruangan yang susah dihubungi menjadi hal-hal yang mempersulit mahasiswa untuk menggunakan ruangan yang ada di IPB, terutama untuk mahasiswa baru yang belum memiliki banyak pengalaman. Solusi dari masalah ini adalah sentralisasi informasi dan pemesanan reservasi ruangan, penerapan dari solusi ini adalah dengan dibuatnya ​web application khusus untuk mencari informasi atau reservasi ruangan yang ada di IPB.

## **Tujuan**
* Mempermudah dalam reservasi ruangan yang tersedia di lingkup kampus IPB.
* Mempermudah mahasiswa dalam mencari informasi tentang ruangan yang terletak di IPB.

## **User analysis**
### **User Stories**
* Sebagai User , agar dapat memesan ruangan, saya dapat melihat list ruangan yang ada di database
* Sebagai User, agar dapat mempermudah mencari ruangan, saya dapat mencari ruangan yang saya inginkan dan memfilter ruangan yang saya butuhkan
* Sebagai User, agar dapat mudah memilih ruangan, saya dapat melihat informasi detail tentang suatu ruangan
* Sebagai User, agar dapat memesan ruangan, saya dapat melihat jadwal hari yang masih kosong dan belum di booking oleh orang lain
* Sebagai User, untuk mempermudah pembayaran ruangan yang sudah dipesan, saya bisa memilih cara pembayaran dan mendapat informasi bagaimana cara membayar
* Sebagai User, untuk mendapatkan informasi dan mengelola akun saya, saya butuh cara agar saya bisa mengubah informasi yang ada di akun saya
* Sebagai Person In Charge, untuk bisa memperbarui informasi tentang ruangan yang saya tanggung jawabi, saya dapat mengubah informasi ruangan hanya di ruangan yang saya tanggung jawabi
* Sebagai admin roombook, untuk bisa mengelola database ruangan, saya bisa mengedit semua ruangan dan membuat ruangan baru

## **Spesifikasi teknis lingkungan pengembangan**
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

## **Hasil dan pembahasan**


### **Use Case Diagram**
![](https://i.imgur.com/FUwou77.jpg)


### **Activity Diagram**
![](https://i.imgur.com/ai5g0f6.jpg)


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

### **Fungsi CRUD**
- User

| CRUD | Verfied Use Case |
| -------- | -------- | 
| Create     | Membuat akun, membuat booking ruangan, membuat transaksi |
| Read     | Membaca booking ruangan orang lain, melihat daftar ruangan, melihat daftar sejarah booking, melihat transaksi beserta statusnya |
| Update     | Mengganti status transaksi dengan cara membayar   |
| Delete     | Membatalkan booking order, membatalkan transaksi |

- Person In Charge

| CRUD | Verfied Use Case |
| -------- | -------- | 
| Create     | Membuat akun, membuat booking ruangan, membuat transaksi |
| Read     | Membaca booking ruangan orang lain, melihat daftar ruangan, melihat daftar sejarah booking, melihat transaksi beserta statusnya |
| Update     | Mengganti status transaksi dengan cara membayar, mengubah informasi ruangan yang ditanggungjawabi   |
| Delete     | Membatalkan booking order, membatalkan transaksi |

- Admin

| CRUD | Verfied Use Case |
| -------- | -------- | 
| Create     | Membuat ruangan baru, membuat akun Person In Charge untuk suatu ruangan |
| Read     | Membaca daftar ruangan, booking ruangan tersebut, dan daftar transaksi ruangan tersebut |
| Update     | Mengubah informasi ruangan    |
| Delete     | Menghapus ruangan |


## **Hasil implementasi**
### **Screenshot sistem**
**1. Landing Page**
![](https://i.imgur.com/XvbvwJY.png)

**2. Login Page**
![](https://i.imgur.com/AtOesHI.png)

**3. Home Page**
![](https://i.imgur.com/dwRdlBk.jpg)

![](https://i.imgur.com/oR6aRy8.png)

**4. Information Page**
![](https://i.imgur.com/YKDv8Xi.png)

**5. Reservation Page**
![](https://i.imgur.com/WjihdXI.png)

**6. Payment Page**
![](https://i.imgur.com/6WPkmgS.png)

**7. Book History Page**
![](https://i.imgur.com/ra3wY9F.png)


## **Testing (Test cases)**
### **Positive Cases**
**1. Forget password benar benar mengirim langsung ke email untuk merubah password**

**2. Bisa dipakai dengan hp dan laptop secara bersamaan**

**3. Register akan mengirim activate account terlebih dahulu ke email**

**4. Update foto profile sudah dapat dilakukan**


### **Negative Cases**
**1. Satu akun gmail bisa dipakai untuk buat banyak akun**

**2. Dalam pemesanan ruangan jika memilih beberapa hari, dan hari ditengahnya sudah di booking orang, masih bisa dipesan**


## **Saran untuk pengembangan selanjutnya**
1. Membuat Mobile app version dari RoomBook
2. Membuat web RoomBook menjadi responsive 

# RPL-9-Reservasi_Ruangan

Kelompok 9
-------------
| NIM | Nama  |
| :-----: | :-: |
| G64190056  | Jevon Sanoturia |
| G64190057	 | Muammar Naufal Pramudya |	
| G64190073	| Muhammad Dafa Athaullah |
|G64190105 |	Maxdha Maxiwinata |

## How to Run
1. Download dan install [python](https://www.python.org/downloads/)
2. Install pip, ini [tutorialnya](https://www.liquidweb.com/kb/install-pip-windows/)
3. Clone repository ini
   - Buka terminal
   - cd ke directory yang diinginkan
   - Lakukan command `git clone https://github.com/MaxdhaMax/RPL-9-Reservasi_Ruangan.git RoomBook'
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


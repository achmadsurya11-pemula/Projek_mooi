import psycopg2
import os
import pyfiglet as pf
from tabulate import tabulate
import datetime as dt
import questionary


def clear():
    os.system("cls")

def pagar ():
    print ("="*70)
    
def KoneksiDB():
    valHost = "localhost"
    valUser = "postgres"
    valPassword = "1111"
    valDatabase = "UASprojek"
    valPort = "5432"
    
    try:
        conn = psycopg2.connect(host=valHost,user=valUser,password=valPassword,database=valDatabase, port=valPort)
        kursor = conn.cursor ()
        return conn, kursor
    except Exception:
        print ("Koneksi Belum Tersambung,harap coba lagi...")
        return None

def enter():
    input ("Tekan [enter] untuk lanjut >>>")
    
def logo():
    print ("""
+======================================================================================+
|   ███╗   ███╗ ██████╗  ██████╗ ██╗    ██████╗  ██████╗ ███╗   ██╗ █████╗ ████████╗   |
|   ████╗ ████║██╔═══██╗██╔═══██╗██║    ██╔══██╗██╔═══██╗████╗  ██║██╔══██╗╚══██╔══╝   |
|   ██╔████╔██║██║   ██║██║   ██║██║    ██║  ██║██║   ██║██╔██╗ ██║███████║   ██║      |
|   ██║╚██╔╝██║██║   ██║██║   ██║██║    ██║  ██║██║   ██║██║╚██╗██║██╔══██║   ██║      |
|   ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║    ██████╔╝╚██████╔╝██║ ╚████║██║  ██║   ██║      |
|   ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝      |
+======================================================================================+  
       """)

def login():
    logo()
    while True:
        print ("====== Login Akun Sebagai ======")
        print ("1. Login sebagai admin\n2. Login sebagai customer\n3. Login sebagai karyawan")
        akun_pengguna = input ("Pilih Login Sebagai:")
        try:
            if akun_pengguna == "1":
                login_admin()
            elif akun_pengguna == "2":
                pilihan_log_cust()
            elif akun_pengguna == "3":
                login_karyawan()
                break
        except:
            print ("Pilihan yang anda masukan salah, silahkan pilih kembali..")

#Cek-Cek--------------------------------------------------
def cek_nama(nama):
    simbol =['!','@','#','$','%','^','&','*','(',')',',']
    while True:
        try:
            if any(s in username for s in simbol):
                print('Username Tidak Sesuai Harus Terdiri Dari Huruf dan angka')
                username = input('Masukkan Username: ')
                continue
            if len(username) < 2:
                print("Username minimal 3 karakter")
                username = input("Masukkan Username: ")
                continue
            if not username.strip():
                print("Username tidak boleh kosong atau spasi saja!")
                username = input("Masukkan Username: ")
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        break
    return nama

def cek_username(username):
    conn, kursor = KoneksiDB()
    simbol =['!','@','#','$','%','^','&','*','(',')',',']
    while True:
        try:
            if any(s in username for s in simbol):
                print('Username Tidak Sesuai Harus Terdiri Dari Huruf dan Angka')
                username = input('Masukkan Username: ')
                continue
            if len(username) < 2:
                print("Username minimal 3 karakter")
                username = input("Masukkan Username: ")
                continue
            if not username.strip():
                print("Username tidak boleh kosong atau spasi saja!")
                username = input("Masukkan Username: ")
                continue
            query = "select * from akun where username = %s"
            kursor.execute(query, (username,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('Username Tidak Sesuai')
                username = input('Masukkan Username: ')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        break
    kursor.close()
    conn.close()
    return username

def cek_nama_produk(nama_produk):
    conn, kursor = KoneksiDB()
    simbol =['!','@','#','$','%','^','&','*','(',')',',']
    while True:
        try:
            if any(s in nama_produk for s in simbol):
                print('nama_produk Tidak Sesuai Harus Terdiri Dari Huruf dan Angka')
                nama_produk = input('Masukkan nama_produk: ')
                continue
            if len(nama_produk) < 2:
                print("nama_produk minimal 3 karakter")
                nama_produk = input("Masukkan nama_produk: ")
                continue
            if not nama_produk.strip():
                print("nama_produk tidak boleh kosong atau spasi saja!")
                nama_produk = input("Masukkan nama_produk: ")
                continue
            query = "select * from produk where nama_produk = %s"
            kursor.execute(query, (nama_produk,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('nama_produk Sudah Dipakai')
                nama_produk = input('Masukkan nama_produk: ')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        break
    kursor.close()
    conn.close()
    return nama_produk

def cek_password(password):
    while True:
        try:
            if not password.strip():
                print("Password tidak boleh kosong atau spasi saja!")
                password = input("Masukkan Password Anda: ")
                continue
            if len(password) < 6:
                print('Password  Minimal 6 Karater')
                password = input('Masukkan Password Anda: ')
                continue
            if password.isalpha():
                print('Password Gabungan Huruf dan Angka')
                password = input('Masukkan Password Anda: ')
                continue
            if password.isnumeric():
                print('Password Gabungan Huruf dan Angka')
                password = input('Masukkan Password Anda: ')
                continue
        except:
            print('Input tidak Valid')
        break
    return password

def cek_email(email):
    while True:
        try:
            if email.endwith('@gmail.com') == False:
                print('Email harus mengunakan @gmail.com')
                email = input('Masukkan Email Anda: ')
                continue
            if not email.strip():
                print("Email tidak boleh kosong atau spasi saja!")
                email = input("Masukkan Email Anda: ")
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    return email

def cek_no_telp(no_telp):
    while True:
        try:
            if no_telp.isalpha() == False:
                print('Nomer Telp harus angka semua')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            if not no_telp.strip():
                print("Nomer Telp tidak boleh kosong atau spasi saja!")
                no_telp = input("Masukkan NO Telp Anda: ")
                continue
            if not (len(no_telp) >= 10 and len(no_telp) <= 13):
                print('Nomer Telp harus 10-13 digit')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    return no_telp

def cek_tanggal(tanggal):
    while True:
        try:
            if not tanggal.strip():
                print("Tanggal Tidak Boleh Kosong")
                tanggal = questionary.text("Tanggal: ").ask()
                continue
            tanggal = int(tanggal)
            if not(tanggal in range(1,32)):
                print('Tanggal Yang Anda Harus 1-31')
                tanggal = questionary.text("Tanggal: ").ask()
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            print('Tanggal Harus Angka')
            tanggal = questionary.text("Tanggal: ").ask()
    return tanggal

def cek_bulan(bulan):
    while True:
        try:
            if not bulan.strip():
                print("bulan Tidak Boleh Kosong")
                bulan = questionary.text("bulan: ").ask()
                continue
            bulan = int(bulan)
            if not(bulan in range(1,13)):
                print('bulan Yang Anda Harus 1-12')
                bulan = questionary.text("bulan: ").ask()
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            print('Tanggal Harus Angka')
            bulan = questionary.text("bulan: ").ask()
    return bulan

def cek_tahun(tahun):
    while True:
        try:
            if not tahun.strip():
                print("Tahun tidak boleh kosong atau spasi saja")
                tahun = questionary.text("Tanggal: ").ask()
                continue
            tahun = int(tahun)
            tanggal_sekarang = dt.date.today()
            tahun_saja = tanggal_sekarang.year
            if tahun <= tahun_saja:
                print('Tahun Yang Anda Masukkan Salah')
                tahun = questionary.text("Tanggal: ").ask()
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            print('Tahun Harus Berupa Angka')
            tahun = questionary.text("Tanggal: ").ask()
    return tahun

def cek_harga(harga):
    while True:
        try:
            if not harga.strip():
                print('Harga Tidak Boleh Kosong') 
                harga = (input('Masukkan Harga Produk(ex:3000): '))
                continue
            harga = int(harga)
            if len(harga) > 4:
                print('Harga Terlalu Rendah')
                harga = (input('Masukkan Harga Produk(ex:3000): '))
                continue
            if harga.isnumeric() == False:
                print('Harga harus terdiri dari angka')
                harga = (input('Masukkan Harga Produk(ex:3000): '))
        except:
            print('Harga harus terdiri dari angka')
            harga = (input('Masukkan Harga Produk(ex:3000): '))
#-------------------------------------------------------------------------------
# Menu Customer

def buat_akun_customer():
    conn, kursor = KoneksiDB()
    while True:
        username_customer = input('Masukkan Username Anda: ')
        password_customer = input('Masukkan Password Anda: ')
        gmail_customer = input('Masukkan Email Anda: ')
        no_telp_customer = input('Masukkan NO_Telp Anda: ')
        username_customer = cek_username(username_customer)
        password_customer = cek_password(password_customer)
        gmail_customer = cek_email(gmail_customer)
        no_telp_customer = cek_no_telp(no_telp_customer)
        query1 = "insert into customer (no_telp, email, akun_id_akun) values (%s, %s, %s);"
        query2 = "insert into akun (username, password, role_id_role) values (%s, %s, 3) returning id_akun;"
        # query3 = "select id_akun from akun where username = %s and password = %s"
        try:    
            kursor.execute(query2, (username_customer, password_customer))
            # kursor.execute(query3, (username_customer, password_customer))
            cocokan = kursor.fetchone()
            id_akun = cocokan[0]
            kursor.execute(query1, (no_telp_customer, gmail_customer, id_akun))
            conn.commit()
            print('BUAT AKUN BERHASIL')
            conn.close()
            break
        except Exception as e:
            conn.rollback()
            print(f"Terjadi Kesalahan : {e}")

def pilihan_log_cust():
    while True:
        print ("====== Login Akun Customer ======")
        print ("1. Sudah punya akun\n2. Belum punya akun")
        akun_cust = input("Masukan pilihan akun:")
        
        try:
            if akun_cust == "1":
                login_customer()
                break
            elif akun_cust == "2":
                buat_akun_customer()
            else: 
                print ("pilihan tidak ada")
        except:
            print("pilihan tidak valid")
            
def login_customer():
    conn, kursor = KoneksiDB()
    while True:
        username_customer = input('Masukkan Username Anda: ')
        password_customer = input('Masukkan Password Anda: ')
        query = "select id_akun from akun where username = %s and password = %s and role_id_role = 3"
        try:
            kursor.execute(query, (username_customer, password_customer))
            cek_akun = kursor.fetchone()
            if cek_akun is not None:
                print('======LOGIN BERHASIL======')
                idcustomer = cek_akun[0]
                menu_customer(idcustomer)
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def area_customer():
    conn, kursor = KoneksiDB()
    query = "select id_area from area where nama_area = %s"
    while True:
        area_pilih = questionary.select(
        "Masukkan Area Kecamatan Anda:",
        choices=['Kaliwates', 'Sumbersari', 'Patrang', 'Ajung', 'Sukorambi', 'Rambipuji', 'Jenggawah', 'Pakusari', 'Arjasa', 'Panti', 'Mumbulsari', 'Mayang', 'Kalisat', 'Bangsalsari', 'Jelbuk', 'Sukowono', 'Umbulsari', 'Balung', 'Ledokombo', 'Silo', 'Semboro', 'Sumberbaru', 'Puger', 'Tanggul', 'Sumberjambe', 'Wuluhan', 'Ambulu', 'Tempurejo', 'Jombang', 'Kencong','Gumukmas']
        ).ask()
        try:
            kursor.execute(query)
            data = kursor.fetchone()
            id_area_pesanan = data[0]
            break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue
    kursor.close()
    conn.close()
    return area_pilih, id_area_pesanan

def pesanan_customer(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga from produk where status_produk = 'Aktif' order by id_produk"
    query2 = "select id_produk from produk where status_produk = 'Aktif' order by id_produk"
    query3 = "select nama_produk from produk where id_produk = %s"
    query4 = "select stock from produk where id_produk = %s"
    produk_dipesan = []
    id_produk = []
    jumlah = []
    sisa_stock = []
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            kursor.execute(query2)
            data = kursor.fetchall()
            data_list = [i[0] for i in data]
            print(f"Produk yang Sudah Dipesan : {produk_dipesan}")
            print(f"Jumlah yang Sudah Dipesan : {jumlah}")
            print('=====PILIH ID PRODUK YANG MAU DIPESAN=====')
            while True:
                try:
                    customer_input = int(input('Masukkan ID Produk Yang Mau Dibeli >> '))
                    if customer_input not in data_list:
                        print('Inputan ID Produk Tidak valid')
                        continue
                    if customer_input in id_produk:
                        print('ID Produk Sudah Dipilih')
                        continue
                    break
                except:
                    print("Input Harus Berupa ID Produk(angka)")
                    continue
            id_produk.append(customer_input)
            kursor.execute(query3, (customer_input,))
            data1 = kursor.fetchone()
            produk_dipesan.append(data1[0])
            kursor.execute(query4, (customer_input,))
            data2 = kursor.fetchone()
            jumlah_stock = data2[0]
            while True:
                try:
                    banyak_produk = int(input('Masukkan Berapa Banyak yang mau dibeli >> '))
                    if banyak_produk == 0:
                        print('Pesanan Tidak Boleh 0')
                        continue
                    if banyak_produk>jumlah_stock:
                        print('Stock Tiidak Mencukupi')
                        continue
                    break
                except:
                    print("Input Harus Berupa Angka")
                    continue
            jumlah.append(banyak_produk)
            data_update = jumlah_stock - banyak_produk
            sisa_stock.append(data_update)
            lanjut_pilih = questionary.select(
            "Mau tambah Produk:",
            choices=["iya,Pilih lagi", "Tidak,Cukup sudah"]
            ).ask()
            if lanjut_pilih == "iya,Pilih lagi":
                continue
            elif lanjut_pilih == "Tidak,Cukup sudah":
                transaksi_pesanan(idakun, produk_dipesan, jumlah, sisa_stock, id_produk)
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue
    kursor.close()
    conn.close()

def identitas_customer():
    while True:
        nama_pemesan = input('Masukkan Pesanan Atas Nama >> ')
        nama_pemesan = cek_nama(nama_pemesan)
        while True:
            alamat_pesanan = input('Masukkan alamat tujuan Pesanan Secara Detail(ex:jalan ahmad yani): ')
            if not alamat_pesanan.strip():
                print("Alamat Pesanan tidak boleh kosong atau spasi saja!")
                continue
            break
        area_pesanan, id_area_pesanan = area_customer()
        metode_pembayaran = questionary.select(
        "Pilih Metode Pembayaran",
        choices=["Cash", "Transfer"]
        ).ask()
        print(f"Pesanan Atas Nama : {nama_pemesan}")
        print(f"Alamat pesanan : {alamat_pesanan}")
        print(f"Area Pesanan : {area_pesanan}")
        print(f"Metode Pembayaran : {metode_pembayaran}")
        detail_customer = questionary.select(
        "Apakah Nama Pemesan, Alamat Pesanan, Area Pesanan, Metode Pesanan Sudah benar",
        choices=["Benar", "Salah"]
        ).ask()
        if detail_customer == "benar":
            if metode_pembayaran == 'Cash':
                Status_Transaksi = "Belum Lunas"
            elif metode_pembayaran == 'Transfer':
                Status_Transaksi = "Lunas"
            break
        elif detail_customer == "Salah":
            continue
    return nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, Status_Transaksi

def struk_pesanan(nama_pemesan, alamat_pesanan, area_pesanan, metode_pembayaran, produk_dipesan, jumlah, harga_pesanan):
    conn, kursor = KoneksiDB()
    query = "select harga from produk where nama_produk = %s"
    try:
        print(f"Nama Pemesan adalah {nama_pemesan}")
        banyak = len(produk_dipesan)
        simpan_pesanan = []
        harga_pesanan = 0
        for i in range(banyak):
            kursor.execute(query, (produk_dipesan[i],))
            data = kursor.fetchone()
            harga_produk = data[0]
            pesanan = [produk_dipesan[i], jumlah[i], harga_produk]
            simpan_pesanan.append(pesanan)
            harga_pesanan = harga_pesanan + (harga_produk * jumlah[i])
        print(tabulate(simpan_pesanan, headers =["Produk","jumlah", "Harga Produk"]))
        print(f'Total Harga Pesanan = {harga_pesanan}')
        print(f"Alamat Pesanan Berada Di {alamat_pesanan} dan Berada di area {area_pesanan}")
        print(f"Metode Pembayaran Menggunakan {metode_pembayaran}")
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def transaksi_pesanan(idakun, produk_dipesan, jumlah, sisa_stock, id_produk):
    conn, kursor = KoneksiDB()
    query = "select harga from produk where nama_produk = %s"
    try:
        banyak = len(produk_dipesan)
        simpan_pesanan = []
        harga_pesanan = 0
        for i in range(banyak):
            pesanan = [produk_dipesan[i], jumlah[i]]
            simpan_pesanan.append(pesanan)
            kursor.execute(query, (produk_dipesan[i],))
            data = kursor.fetchone()
            harga_produk = data[0]
            harga_pesanan = harga_pesanan + (harga_produk * jumlah[i])
        print(tabulate(simpan_pesanan, headers =["Produk","jumlah"]))
        print(f'Total Harga Pesanan = {harga_pesanan}')
        customer_pilih = questionary.select(
            "Apakah sudaah benar Pesanan anda:",
            choices=["iya,Sudah Benar", "Tidak"]
            ).ask()
        if customer_pilih == "iya,Sudah Benar":
            nama_pemesan, alamat_pesanan, area_pesanan, metode_pembayaran, Status_Transaksi = identitas_customer()
            struk_pesanan(nama_pemesan, alamat_pesanan, area_pesanan, metode_pembayaran, produk_dipesan, jumlah, harga_pesanan)
            tanggal = dt.date.today()
            simpan_data(idakun, produk_dipesan, jumlah, sisa_stock, nama_pemesan, alamat_pesanan, area_pesanan, metode_pembayaran, id_produk, tanggal, Status_Transaksi)
        elif customer_pilih == "Tidak":
            pesanan_customer(idakun)
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def simpan_data(idakun, jumlah, sisa_stock, nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, id_produk, tanggal, Status_Transaksi, harga):
    conn, kursor = KoneksiDB()
    query1 = "insert into Transaksi (Status_Transaksi, tanggal_Transaksi, Metode_Pembayaran) values (%s, %s, %s) returning ID_Transaksi;"
    query2 = "insert into Alamat_Pesanan (Jalan_Pesanan, Area_ID_Area) values (%s, %s) returning ID_Alamat_Pesanan;"
    query3 = "insert into Pesanan (Nama_Pemesan, Status_Pesanan, customer_ID_Customer, Alamat_Pesanan_ID_Alamat_Pesanan, Transaksi_ID_Transaksi, Karyawan_ID_Karyawan) values (%s, %s, %s, %s, %s, %s) returning ID_Pesanan;"
    query4 = "insert into Detail_Pesanan (Harga, Jumlah_Produk, Produk_ID_Produk, Pesanan_ID_Pesanan) values (%s, %s, %s, %s)"
    query5 = "update produk set Stock = %s where id_produk = %s"
    try: 
        kursor.execute(query1, (Status_Transaksi, tanggal, metode_pembayaran))
        id_transaksi = kursor.fetchone()
        if id_transaksi is not None:
            id_transaksi = id_transaksi[0]
            kursor.execute(query2, (alamat_pesanan, id_area_pesanan))
            id_alamat = kursor.fetchone()
            if id_alamat is not None:
                id_alamat = id_alamat[0]
                status_pesanan_customer = "Menunggu"
                kursor.execute(query3, (nama_pemesan, status_pesanan_customer, idakun, id_alamat, id_transaksi, None))
                id_pesanan = kursor.fetchone()
                if id_pesanan is not None:
                    id_pesanan = id_pesanan[0]
                    banyak_data = len(id_produk)
                    for i in range(banyak_data):
                        kursor.execute(query4, (harga[i], jumlah[i], id_produk[i], id_pesanan))
                        kursor.execute(query5, (sisa_stock[i], id_produk[i]))
                        conn.commit()
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def menu_customer(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga from produk where status_produk = 'Aktif order by id_produk'"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            print("=====Menu Customer=====")
            pilih_menu = questionary.select(
            "Mau tambah Produk:",
            choices=["Pilih Produk", "Lihat Pesanan", "Keluar"]
            ).ask()
            if pilih_menu == "Pilih Produk":
                pesanan_customer(idakun)
                continue
            elif pilih_menu == "Lihat Pesanan":
                lihat_pesanan(idakun)
                continue
            elif pilih_menu == "Keluar":
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue

#Menu Admin----------------------------------------------------------------------------------------------------------------
def login_admin():
    conn, kursor = KoneksiDB()
    while True:
        username_admin = input('Masukkan Username Anda: ')
        password_admin = input('Masukkan Password Anda: ')
        query = "select id_akun from akun where username = %s and password = %s and role_id_role = 1"
        try:
            kursor.execute(query, (username_admin, password_admin))
            cek_akun = kursor.fetchone()
            if cek_akun is not None:
                print('======LOGIN BERHASIL======')
                idakun = cek_akun[0]
                menu_admin(idakun)
                conn.close()
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")   
            
def lihat_produkA(idakun):
    conn, kursor = KoneksiDB()
    query = "select * from produk order by id_produk"
    try:
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close() 

def lihat_pesanan(idakun):
    conn, kursor = KoneksiDB()
    try:
        query = "select * from pesanan"
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")

    kursor.close()
    conn.close() 
    
def lihat_detail_pesanan(idakun):
    conn, kursor = KoneksiDB()
    try:
        query = "select * from detail_pesanan"
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
        
    kursor.close()
    conn.close() 
    
def laporan(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.quantity) as jumlah_terjual from produk p join detail_pesanan dp using (produk_id) where p.status_pruduk = 'Aktif' group by p.nama_produk order by sum(dp.harga * dp.quantity)"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            print("=====MENU LAPORAN=====")
            print("(1). Tampilkan 5 Produk Terlaris 1 Minggu Terkhir\n(2). Tampilkan 5 Produk Terlaris 1 Bulan Terakhir\n(3). Tampilkan 5 Produk Kurang Diminati 1 Minggu Terakhir\n(4). Tampilkan 5 Produk Kurang Diminati 1 Bulan Terakhir\n(5). Exit")
            admin_pilih = input('Masukkan Pilihan Anda >> ')
            if admin_pilih == '1':
                produk_laris_1minggu(idakun)
                continue
            elif admin_pilih == '2':
                produk_laris_1bulan(idakun)
                continue
            elif admin_pilih == '3':
                produk_kurang_1minggu(idakun)
                continue
            elif admin_pilih == '4':
                produk_kurang_1bulan(idakun)
                continue
            elif admin_pilih == '5':
                break
            else:
                print('Pilihan Tidak Ada')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")

def produk_laris_1minggu(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.quantity) as jumlah_terjual from produk p join detail_pesanan dp using (id_produk) where p.status_produk = 'Aktif' and tanggal_pesanan <= %s and tanggal_pesanan >= %s group by p.nama_produk order by sum(dp.harga * dp.quantity) desc limit 5"
    try:
        tanggal_awal = dt.date.today()
        tanggal_akhir = tanggal_awal - dt.timedelta(days=7)
        kursor.execute(query1, (tanggal_awal, tanggal_akhir))
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    finally:
        kursor.close()
        conn.close()
        
def produk_laris_1bulan(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.quantity) as jumlah_terjual from produk p join detail_pesanan dp using (id_produk) where p.status_produk = 'Aktif' and tanggal_pesanan <= %s and tanggal_pesanan >= %s group by p.nama_produk order by sum(dp.harga * dp.quantity) desc limit 5"
    try:
        tanggal_awal = dt.date.today()
        tanggal_akhir = tanggal_awal - dt.timedelta(days=30)
        kursor.execute(query1, (tanggal_awal, tanggal_akhir))
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    finally:
        kursor.close()
        conn.close()
        
def produk_kurang_1minggu(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.quantity) as jumlah_terjual from produk p join detail_pesanan dp using (id_produk) where p.status_produk = 'Aktif' and tanggal_pesanan <= %s and tanggal_pesanan >= %s group by p.nama_produk order by sum(dp.harga * dp.quantity) asc limit 5"
    try:
        tanggal_awal = dt.date.today()
        tanggal_akhir = tanggal_awal - dt.timedelta(days=7)
        kursor.execute(query1, (tanggal_awal, tanggal_akhir))
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    finally:
        kursor.close()
        conn.close()

def produk_kurang_1bulan(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.quantity) as jumlah_terjual from produk p join detail_pesanan dp using (id_produk) where p.status_produk = 'Aktif' and tanggal_pesanan <= %s and tanggal_pesanan >= %s group by p.nama_produk order by sum(dp.harga * dp.quantity) asc limit 5"
    try:
        tanggal_awal = dt.date.today()
        tanggal_akhir = tanggal_awal - dt.timedelta(days=30)
        kursor.execute(query1, (tanggal_awal, tanggal_akhir))
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    finally:
        kursor.close()
        conn.close()
        
#Ubah Produk Admin
def hapus_produk(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga, stock from produk where status_produk = 'Aktif' order by id_produk;"
    query2 = "select id_produk from produk where status_produk = 'Aktif' order by id_produk;"
    query3 = "update produk set status_produk = 'Tidak Aktif' where id_produk = %s"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print(tabulate(data, headers=header, tablefmt='psql'))
            kursor.execute(query2)
            data = kursor.fetchall()
            data_list = [i[0] for i in data]
            print('===PILIH ID PRODUK YANG MAU DIHAPUS===')
            while True:
                try:
                    admin_input = int(input('Pilih Id Produk yang mau dihilangkan: '))
                    if admin_input not in data_list:
                        print('Id Produk yang anda masukkan salah')                     
                        continue
                    break
                except ValueError:
                    print("Input harus berupa angka!")
                    continue
            kursor.execute(query3, (admin_input,))
            conn.commit()
            print('Penghapusan Berhasil')
            admin_pilih = questionary.select(
            "Apakah Ada Produk Lagi Yang Mau Dihapus?:",
            choices=['iya', 'tidak']).ask()
            if admin_pilih == 'iya':
                continue
            elif admin_pilih == 'tidak':
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def kembali_produk(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga, stock from produk where status_produk = 'Tidak Aktif' order by id_produk;"
    query2 = "select id_produk from produk where status_produk = 'Tidak Aktif' order by id_produk;"
    query3 = "update produk set status_produk = 'Aktif' where id_produk = %s"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print(tabulate(data, headers=header, tablefmt='psql'))
            kursor.execute(query2)
            data = kursor.fetchall()
            data_list = [i[0] for i in data]
            print('===PILIH ID PRODUK YANG MAU DIKEMBALIKAN===')
            while True:
                try:
                    admin_input = int(input('Pilih Id Produk yang mau dikembalikan: '))
                    if admin_input not in data_list:
                        print('Id produk yang anda masukkan salah')
                        continue
                    break
                except ValueError:
                    print("Input harus berupa angka!")
                    continue
            kursor.execute(query3, (admin_input,))
            conn.commit()
            print('Pengembalian Berhasil')
            admin_pilih = questionary.select(
            "Apakah Ada Produk Lagi Yang Mau Dikembalikan?:",
            choices=['iya', 'tidak']).ask()
            if admin_pilih == 'iya':
                continue
            elif admin_pilih == 'tidak':
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def tambah_produk(idakun):
    conn, kursor = KoneksiDB()
    nama_produk = input('Masukkan Nama Produk Yang Mau Ditambahkan: ')
    harga = input('Masukkan Harga Produk: ')
    query = "insert into produk (nama_produk, harga, stock, status_produk) values (%s, %s, 0, 'Aktif)"
    while True:
        try:
            nama_produk = cek_nama_produk(nama_produk)
            harga = cek_harga(harga)
            kursor.execute(query)
            conn.commit()
            print('Penambahan Produk Berhasil')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def ubah_harga(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga from produk where status_produk = 'Aktif' order by id_produk;"
    query2 = "update produk set harga = %s where id_produk = %s"
    query3 = "select id_produk from produk where status_produk = 'Aktif' order by id_produk;"
    while True:
        try:
            harga_admin = 0
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            kursor.execute(query3)
            data = kursor.fetchall()
            data_list = [i[0] for i in data]
            print('======Id Produk======')
            for i in data:
                print(f'id Produk {i[0]}')
            try:
                admin_input = int(input('Pilih Id Produk yang mau diubah Harganya: '))
                while True:
                    if admin_input not in data_list:
                        print('Id Produk yang anda masukkan salah')
                        admin_input = int(input('Pilih Id Produk yang mau diubah Harganya: '))
                        continue
                    break
            except ValueError:
                print("Input harus berupa angka!")
                continue
            harga_admin = input('Masukkan harga Terbaru: ')
            while True:
                try:
                    if not harga_admin.strip():
                        print("Harga tidak boleh kosong atau spasi saja!")
                        harga_admin = input("Masukkan harga Terbaru: ")
                        continue
                    harga_admin = int(harga_admin)
                    if harga_admin < 1000:
                        print('Harga Terlalu Rendah')
                        harga_admin = input("Masukkan harga Terbaru: ")
                        continue
                    break
                except:
                    print('Harga Harus Berupa Angka')
                    harga_admin = input("Masukkan harga Terbaru: ")
            kursor.execute(query2, (harga_admin, admin_input))
            conn.commit()
            print('Perubahan Harga Berhasil')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue
        ubah_lagi = questionary.select(
        "Apakah Mau Lanjut Ubah Harga:",
        choices=["Lanjut", "Tidak"]
        ).ask()
        if ubah_lagi == 'Lanjut':
            continue
        elif ubah_lagi == 'Tidak':
            break
    kursor.close()
    conn.close()

def perbarui_produk(idakun):
    conn, kursor = KoneksiDB()
    query1 = "select id_produk, nama_produk, harga, stock from produk where status_produk = 'Aktif' order by id_produk;"
    try:
        while True:
            print('=====PRODUK DIJUAL=====')
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            print('=====PILIH MENU PRODUK=====')
            print('(1). Hapus Produk\n(2). Kembalikan Produk\n(3). Tambah Produk\n(4). Ubah Harga Produk\n(5). Exit')
            admin_input = input('Masukkan Pilihan Anda >> ')
            if admin_input == '1':
                hapus_produk(idakun)
                continue
            elif admin_input == '2':
                kembali_produk(idakun)
                continue
            elif admin_input == '3':
                tambah_produk(idakun)
                continue
            elif admin_input == '4':
                ubah_harga(idakun)
            elif admin_input == '5':
                break
            else:
                print('Pilhan Tidak Ada')
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

#Menu admin ngubah karyawan-------------------------------------------------------------------------------------------------
def lihat_karyawan(idakun):
    conn, kursor = KoneksiDB()
    try:
        query = "select * from karyawan"
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")

    kursor.close()
    conn.close() 

def pecat_karyawan(idakun):
    conn, kursor = KoneksiDB()
    try:
        query1 = "select * from karyawan where status_karyawan = 'Aktif' and jabatan_id_jabata <> 5"
        query2 = "select id_karyawan from karyawan where status_karyawan = 'Aktif' and jabatan_id_jabata <> 5"
        query3 = "update karyawan set status_karyawan = 'Tidak Aktif' where id_karyawan = %s"
        while True:
            kursor.execute(query1)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            kursor.execute(query2)
            data = kursor.fetchall()
            data_list = [i[0] for i in data]
            print('======Id Karyawan======')
            for i in data:
                print(f'id karyawan {i[0]}')
            try:
                admin_input = int(input('Pilih Id Karyawan yang mau dipecat: '))
                while True:
                    if admin_input not in data_list:
                        print('Id Karyawan yang anda masukkan salah')
                        admin_input = int(input('Pilih Id Karyawan yang mau dipecat: '))
                        continue
                    break
            except ValueError:
                print("Input harus berupa angka!")
                continue
            kursor.execute(query3, (admin_input,))
            conn.commit()
            print('Pemecatan Berhasil')
            break
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    finally:
        kursor.close()
        conn.close()

def tambah_karyawan(idakun):
    conn, kursor = KoneksiDB()
    while True:
        nama_karyawan = input('Masukkan Nama Karyawan: ')
        ttl_karyawan = tanggal_karyawan()
        email_karyawan = input('Masukkan email karyawan: ')
        no_telp_karyawan = input('Masukkan NO Telp karyawan: ')
        password_karyawan = input('Masukkan Password karyawan: ')
        jabatan = questionary.select(
        "Jabatan Karyawan:",
        choices=["Pengantar", "Kasir", "kebersihan", "koki"]
        ).ask()
        if jabatan == "Pengantar":
            jabatan_id = 1
        elif jabatan == "kasir":
            jabatan_id = 2
        elif jabatan == "kebersihan":
            jabatan_id = 3
        elif jabatan == "koki":
            jabatan_id = 4
        nama_karyawan = cek_username(nama_karyawan)
        password_karyawan = cek_password(password_karyawan)
        email_karyawan = cek_email(email_karyawan)
        no_telp_karyawan = cek_no_telp(no_telp_karyawan)
        ttl_karyawan = cek_tanggal(ttl_karyawan)
        query1 = "insert into karyawan (nama_karyawan, tanggal_lahir, email, no_telp, akun_id_akun, jabatan_id_jabatan) values (%s, %s, %s, %s, %s, %s);"
        query2 = "insert into akun (username, password, role_id_role) values (%s, %s, 2) returning id_akun;"
        try:
            kursor.execute(query2, (nama_karyawan, password_karyawan))
            cocokan = kursor.fetchone()
            id_akun = cocokan[0]
            kursor.execute(query1, (nama_karyawan, ttl_karyawan, email_karyawan, no_telp_karyawan, id_akun, jabatan_id))
            conn.commit()
            print('BUAT AKUN BERHASIL')
            break
        except Exception as e:
            conn.rollback()
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def tanggal_karyawan(idakun):
    tanggal = questionary.text("Tanggal: ").ask()
    bulan = questionary.text("Bulan: ").ask()
    tahun = questionary.text("Tahun: ").ask()
    try:
        tanggal = cek_tanggal(tanggal)
        bulan = cek_bulan(bulan)
        tahun = cek_tahun(tahun)
        karyawan_date = dt.date(tahun, bulan, tanggal)
        return karyawan_date
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            
def detail_karyawan(idakun):
    conn, kursor = KoneksiDB()
    query = "select * from karyawan where status_karyawan = 'Aktif' and jabatan_id_jabata <> 'owner'"
    while True:
        try:
            kursor.execute(query)
            data = kursor.fetchall()
            header= [d[0]for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            print('=====MENU KARYAWAN=====')
            print("""
            (1). Melihat Semua Karyawan
            (2). Menambahkan Karyawan
            (3). Memecat Karyawan
            (4). Exit
            """)
            data = input('Masukkan Pilihan Menu >> ')
            if data == '1':
                lihat_karyawan(idakun)
            elif data == '2':
                tambah_karyawan(idakun)
            elif data == '3':
                pecat_karyawan(idakun)
            elif data == '4':
                break
            else:
                print('Pilihan Tidak Ada')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")

    kursor.close()
    conn.close() 

def menu_admin(idakun):
    while True:
        print('======MENU ADMIN======')
        print("""
    (1). Melihat Produk
    (2). Memperbarui Produk
    (3). Laporan
    (4). Melihat pesanan
    (5). Melihat Detail Pesanan
    (6). Detail Karyawan
    (7). Diskon
    (8). Exit
        """)
        input_admin = input('Pilih Menu Yang Diinginkan >> ')
        if input_admin == '1':
            lihat_produkA(idakun)
            continue
        elif input_admin == '2':
            perbarui_produk(idakun)
            continue
        elif input_admin == '3':
            laporan(idakun)
            continue
        elif input_admin == '4':
            lihat_pesanan(idakun)
            continue
        elif input_admin == '5':
            lihat_detail_pesanan(idakun)
            continue
        elif input_admin == '6':
            detail_karyawan(idakun)
            continue
        elif input_admin == '7':
            diskon(idakun)
            continue
        elif input_admin == '8':
            break
        else:
            print("Pilihan Tidak Ada")
#Menu Karyawan----------------------------------------------------------------------------------------------------------------

def login_karyawan():
    conn, kursor = KoneksiDB()
    while True:
        username_karyawan = input('Masukkan Username Anda: ')
        password_karyawan = input('Masukkan Password Anda: ')
        query = "select id_akun from akun where username = %s and password = %s and role_id_role = 2"
        try:
            kursor.execute(query, (username_karyawan, password_karyawan))
            cek_akun = kursor.fetchone()
            if cek_akun is not None:
                print('======LOGIN BERHASIL======\n')
                idkaryawan = cek_akun[0]
                menu_karyawan(idkaryawan)
                conn.close()
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")

def lihat_produk_karyawan(idkaryawan):
    conn, kursor = KoneksiDB()
    try:
        query = "SELECT id_produk,nama_produk,harga FROM produk order by id_produk"
        kursor.execute(query)
        
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
        
        kursor.close(), conn.close()
    except Exception as e:
        print (f"Terjadi Kesalahan : {e}")

def update_stock(idkaryawan):
    conn, kursor = KoneksiDB()
    try:
        query = "SELECT id_produk, nama_produk, stock from produk where stock > 0 order by id_produk"
        kursor.execute(query)
        data= kursor.fetchall()
        header= [d[0] for d in kursor.description]
        
        print ("\n==Daftar produk==")
        print (tabulate(data, headers=header, tablefmt='psql'))
        
        
        print ("\n==Update Produk==")
        id_produk = input ("Masukan id Produk:  ")
        kursor.execute("SELECT stock from produk where id_produk = %s", (id_produk,))
        baris = kursor.fetchone()
        
        if not baris:
            print ("ID produk tidak ditemukan")
            return
        
        stock_sekarang= baris [0]
        print (f"Stock saat ini:     {stock_sekarang}")
        
        print ("\n==Pilih Metode Update==")
        print ("1. Set Stock Langsung")
        print ("2. Tambah Stock")
        print ("3. Kurangi Stock")
        pilihan = input ("masukan pilihan:")

        if pilihan == "1":
            stock_baru = int(input("Masukan stok baru:"))
            if stock_baru < 0:
                print("Tidak boleh negatif")
                return
            query2 ="UPDATE produk SET stock = %s WHERE id_produk = %s"
            kursor.execute(query2, (stock_baru, id_produk))

        elif pilihan == "2":
            tambah = int(input("Tambah Stock: "))
            stock_baru = stock_sekarang + tambah
            
            query3 ="UPDATE produk SET stock = %s WHERE id_produk = %s"
            kursor.execute(query3, (stock_baru, id_produk))
            
        elif pilihan == "3":
            kurang = int(input("Mengurangi Stock: "))
            stock_baru = stock_sekarang - kurang
            if stock_baru < 0:
                print("Tidak Boleh negatif")
                return
            query4="UPDATE produk SET stock = %s WHERE id_produk = %s"
            kursor.execute(query4, (stock_baru, id_produk))
        else:
            print ("Tidak Valid")
            return
        
        conn.commit()
        print (f"Stock berhasil di perbarui: {stock_baru}")
        
    except Exception as e:
        print (f"Terjadi kesalahan: {e}")
        conn.rollback()
        
    finally:
        kursor.close()
        conn.close() 
                        
def kelola_pesanan_cust(idkaryawan):
    clear()
    conn, kursor = KoneksiDB()
    query1 = "SELECT id_pesanan, nama_pemesan from pesanan order by id_pesanan"
    query2 = '''
    select pr.nama_produk, dp.jumlah_produk, dp.harga
    from pesanan p
    join detail_pesanan dp on p.id_pesanan=dp.pesanan_id_pesanan
    join produk pr on dp.produk_id_produk = pr.id_produk 
    where id_pesanan = %s
    '''
    query3 = "update pesanan set status_pesanan = 'Diantar' where id_pesanan = %s"
    query4 = '''
    select p.nama_pemesan, pr.nama_produk, dp.jumlah_produk, dp.harga, p.status_pesanan
    from pesanan p
    join detail_pesanan dp on p.id_pesanan=dp.pesanan_id_pesanan
    join produk pr on dp.produk_id_produk = pr.id_produk 
    where p.status_pesanan = 'Diantar' and id_pesanan = %s
    '''
    
    while True:
        try:
            #Menampilkan List pesanan
            kursor.execute(query1)
            data = kursor.fetchall()
            header = [d[0] for d in kursor.description]
            print (tabulate(data, headers=header, tablefmt='psql'))
            
            #Validasi ID
            data_list = [i[0] for i in data]
            print ("==========PILIH ID PESANAN=========")    
            try:
                input_id = int (input("Pilih ID pesanan yang mau diproses: "))
                while input_id not in data_list:
                    print ("ID Pesanan yang anda masukan salah..")
                    input_id = int (input("Pilih ID pesanan yang mau diproses: "))
                    continue
            except ValueError:
                print ("Inputan harus berupa angka!!")
                continue
            clear()
            #Menampilkan Nama Pemesan & No Telp
            query_info = '''
            SELECT p.nama_pemesan AS nama,c.no_telp AS no_telp
            FROM pesanan p
            JOIN customer c ON p.customer_id_customer = c.id_customer
            WHERE p.id_pesanan = %s
            '''
            kursor.execute(query_info, (input_id,))
            hasil = kursor.fetchone()
            nama, no_telp = hasil
            print("\n========== DATA PEMESAN ==========")
            print(f"Nama Pemesan : {nama}")
            print(f"No Telp      : {no_telp}")
            print("====================================\n")
        
            #Menampilkan Detail Pesanan
            kursor.execute(query2, (input_id,))
            data2 = kursor.fetchall()
            header2 = [d[0] for d in kursor.description]
            print (tabulate(data2, headers=header2, tablefmt='psql'))
            
            #Konfirmasi
            print ("Apakah pesanan akan dikirimkan?")
            enter()
            
            # Insert tanggal pengantaran ke DB
            tanggal_sekarang = dt.date.today()
            queryy = "insert into pengantar (tanggal_pengantar, karyawan_id_karyawan) VALUES (%s, %s)"
            kursor.execute(queryy, (tanggal_sekarang, idkaryawan))
            conn.commit()
            print ("Berhasil ditambah")
            
           
            #Update Status
            kursor.execute(query3, (input_id,))
            conn.commit()
            print ("Pesanan segera dikirimkan!!")
            
            #Menampilkan Pesanan yang mau diantar
            kursor.execute(query4, (input_id,))
            data3 = kursor.fetchall()
            header3 = [d[0] for d in kursor.description]
            print (tabulate(data3, headers=header3, tablefmt='psql'))
            
            
        except Exception as e:
            print (f"Terjadi Kesalahan : {e}")
            
        finally:
            kursor.close()
            conn.close()           
        break

def menu_karyawan(idkaryawan):
    while True:
        try:
            print ("======MENU======")
            print ("1. Melihat Produk\n2. Mengelola Stock\n3. Mengelola Pesanan\n4. Keluar")
            pilihan_karyawan = input ("Masukan pilihan:")
            if pilihan_karyawan == "1":
                lihat_produk_karyawan(idkaryawan)
                enter()
                continue
            elif pilihan_karyawan == "2":
                update_stock(idkaryawan)
                enter()
                continue
            elif pilihan_karyawan == "3":  
                kelola_pesanan_cust(idkaryawan)
                continue
            elif pilihan_karyawan == "4":  
                break
            else:
                print("Pilihan Tidak Valid!")
        except:
            print ("Terjadi Kesalahan")

login()

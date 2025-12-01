import psycopg2 
from tabulate import tabulate
import datetime as dt
import questionary
import os

def koneksiDB():
    nilaihost = 'localhost'
    nilaiDB = 'Algo_Basda'
    nilaiuser = 'postgres'
    nilaipass = '1111'
    nilaiport = '5432'
    try:
        conn = psycopg2.connect(
                host = nilaihost,
                database = nilaiDB,  
                user = nilaiuser,
                password = nilaipass,
                port = nilaiport
            )
        kursor = conn.cursor()
        return kursor, conn
    except:
        print('Koneksi ke Database Gagal, Silahkan Check Lagi')

def batas():
    print('='*64)

def clear():
    os.system("cls")
    
def enter():
    input ("Tekan [enter] untuk lanjut >>>")

def login():
    while True:
        print('======LOGIN AKUN SEBAGAI======')
        print('(1).Login Sebagai Admin\n(2). Login Sebagai Customer\n(3). Login Sebagai Karyawan')
        akunpengguna = input('Pilih Login Sebagai >> ')
        try:
            if akunpengguna == '1':
                loginadmin()
                break
            elif akunpengguna == '2':
                pilihan_login_cust()
                break
            elif akunpengguna == '3':
                loginkaryawan()
                break
        except:
            print('Pilihan Login Yang Anda Masukkan Salah\nSilahkan Masukkan Pilihan Login lagi ')

def pilihan_login_cust():
    while True:
        print('======LOGIN AKUN CUSTOMER======')
        print('(1). Sudah Punya Akun\n(2). Belum Punya Akun')
        akun_customer = input('Masukkan Pilihan Akun')
        try:
            if akun_customer == '1':
                logincustomer()
                break
            elif akun_customer == '2':
                buat_akun_customer()
            else:
                print('Pilihan Tidak Ada')
        except:
            print('Inputan Yang Dimasukkan Tidak Valid')

def loginadmin():
    kursor, conn = koneksiDB()
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
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def logincustomer():
    kursor, conn = koneksiDB()
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

def loginkaryawan():
    kursor, conn = koneksiDB()
    while True:
        username_karyawan = input('Masukkan Username Anda: ')
        password_karyawan = input('Masukkan Password Anda: ')
        query = "select id_akun from akun where username = %s and password = %s and role_id_role = 2"
        try:
            kursor.execute(query, (username_karyawan, password_karyawan))
            cek_akun = kursor.fetchone()
            if cek_akun is not None:
                print('======LOGIN BERHASIL======')
                idkaryawan = cek_akun[0]
                menu_karyawan(idkaryawan)
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    
        kursor.close()
        conn.close()

#--------------------------------------------------------------------------------

def cek_nama(nama):
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
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        break
    return nama

def cek_username(username):
    kursor, conn = koneksiDB()
    simbol =['!','@','#','$','%','^','&','*','(',')',',']
    while True:
        try:
            if any(s in username for s in simbol):
                print('Username Tidak Sesuai Harus Terdiri Dari Huruf')
                username = input('Masukkan Username: ')
                continue
            if username.isdigit():
                print("username tidak boleh pakai angka")
                username = input('Masukkan Username: ')
                continue
            if len(username) < 3:
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
                print('Username Sudah Dipakai')
                username = input('Masukkan Username: ')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            username = input("Masukkan Username: ")
            continue
        break
    kursor.close()
    conn.close()
    return username

def cek_nama_produk(nama_produk):
    kursor, conn = koneksiDB()
    simbol =['!','@','#','$','%','^','&','*','(',')',',']
    while True:
        try:
            if any(s in nama_produk for s in simbol):
                print('nama_produk Tidak Sesuai Harus Terdiri Dari Huruf')
                nama_produk = input('Masukkan nama_produk: ')
                continue
            if len(nama_produk) < 2:
                print("nama_produk minimal 3 karakter")
                nama_produk = input("Masukkan nama_produk: ")
                continue
            if nama_produk.isdigit():
                print("Nama Tidak Boleh Ada Angka")
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
            continue
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

def cek_email_customer(email):
    kursor, conn = koneksiDB()
    while True:
        try:
            if not email.endswith('@gmail.com'):
                print('Email harus mengunakan @gmail.com')
                email = input('Masukkan Email Anda: ')
                continue
            if not email.strip():
                print("Email tidak boleh kosong atau spasi saja!")
                email = input("Masukkan Email Anda: ")
                continue
            query = "select * from customer where email = %s"
            kursor.execute(query, (email,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('Email Sudah Dipakai')
                email = input('Masukkan Email: ')
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            email = input("Masukkan Email Anda: ")
            continue
    kursor.close()
    conn.close()
    return email

def cek_email_karyawan(email):
    kursor, conn = koneksiDB()
    while True:
        try:
            if not email.endswith('@gmail.com'):
                print('Email harus mengunakan @gmail.com')
                email = input('Masukkan Email Anda: ')
                continue
            if not email.strip():
                print("Email tidak boleh kosong atau spasi saja!")
                email = input("Masukkan Email Anda: ")
                continue
            query = "select * from karyawan where email = %s"
            kursor.execute(query, (email,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('Email Sudah Dipakai')
                email = input('Masukkan Email: ')
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            email = input("Masukkan Email Anda: ")
            continue
    kursor.close()
    conn.close()
    return email

def cek_no_telp_customer(no_telp):
    kursor, conn = koneksiDB()
    while True:
        try:
            if not no_telp.strip():
                print("Nomer Telp tidak boleh kosong atau spasi saja!")
                no_telp = input("Masukkan NO Telp Anda: ")
                continue
            if not no_telp.isdigit():
                print('Nomer Telp harus angka semua')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            if not (len(no_telp) >= 10 and len(no_telp) <= 13):
                print('Nomer Telp harus 10-13 digit')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            query = "select * from customer where no_telp = %s"
            kursor.execute(query, (no_telp,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('NO TELP Sudah Dipakai')
                no_telp = input('Masukkan NO TELP Anda: ')
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            continue
    kursor.close()
    conn.close()
    return no_telp

def cek_no_telp_karyawan(no_telp):
    kursor, conn = koneksiDB()
    while True:
        try:
            if not no_telp.strip():
                print("Nomer Telp tidak boleh kosong atau spasi saja!")
                no_telp = input("Masukkan NO Telp Anda: ")
                continue
            if not no_telp.isdigit():
                print('Nomer Telp harus angka semua')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            if not (len(no_telp) >= 10 and len(no_telp) <= 13):
                print('Nomer Telp harus 10-13 digit')
                no_telp = input('Masukkan NO Telp Anda: ')
                continue
            query = "select * from karyawan where no_telp = %s"
            kursor.execute(query, (no_telp,))
            cocok = kursor.fetchone()
            if cocok is not None:
                print('NO TELP Sudah Dipakai')
                no_telp = input('Masukkan NO TELP Anda: ')
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            continue
    kursor.close()
    conn.close()
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
            continue
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
            continue
    return bulan

def cek_tahun(tahun):
    while True:
        try:
            if not tahun.strip():
                print("Tahun tidak boleh kosong atau spasi saja")
                tahun = questionary.text("Tahun: ").ask()
                continue
            if not tahun.isdigit():
                print('Tahun Harus Berupa Angka')
                tahun = questionary.text("Tahun: ").ask()
                continue
            tahun = int(tahun)
            if tahun >= tahun + 100:
                print("tahun terlalu panjang")
                tahun = questionary.text("Tahun: ").ask()
                continue
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            tahun = questionary.text("Tahun: ").ask()
            continue
    return tahun

def cek_harga(harga):
    while True:
        try:
            if not harga.strip():
                print('Harga Tidak Boleh Kosong') 
                harga = (input('Masukkan Harga Produk(ex:3000): '))
                continue
            if not harga.isnumeric():
                print('Harga harus terdiri dari angka')
                harga = (input('Masukkan Harga Produk(ex:3000): '))
                continue
            harga = int(harga)
            if harga < 1000:
                print('Harga Terlalu Rendah')
                harga = (input('Masukkan Harga Produk(ex:3000): '))
                continue
            break
        except:
            print('Harga harus terdiri dari angka')
            harga = (input('Masukkan Harga Produk(ex:3000): '))
    return harga

#-----------------------------------------------------------------------------------------------
def buat_akun_customer():
    kursor, conn = koneksiDB()
    while True:
        username_customer = input('Masukkan Username Anda: ')
        username_customer = cek_username(username_customer)
        password_customer = input('Masukkan Password Anda: ')
        password_customer = cek_password(password_customer)
        gmail_customer = input('Masukkan Email Anda: ')
        gmail_customer = cek_email_customer(gmail_customer)
        no_telp_customer = input('Masukkan NO_Telp Anda: ')
        no_telp_customer = cek_no_telp_customer(no_telp_customer)
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

def laporan(idakun):
    kursor, conn = koneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.jumlah_produk) as jumlah_terjual from produk p join detail_pesanan dp on dp.Produk_ID_Produk = p.ID_Produk where p.status_produk = 'Aktif' group by p.nama_produk order by jumlah_terjual desc"
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
    kursor.close()
    conn.close()

def produk_laris_1minggu(idakun):
    kursor, conn = koneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.Jumlah_produk) as jumlah_terjual from produk p join detail_pesanan dp on dp.Produk_ID_Produk = p.ID_Produk join pesanan ps on ps.id_pesanan = dp.pesanan_id_pesanan join pengantar pe on ps.pengantar_id_pengantar = pe.id_pengantar where p.status_produk = 'Aktif' and pe.tanggal_pengantar <= %s and pe.tanggal_pengantar >= %s group by p.nama_produk order by jumlah_terjual desc limit 5"
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
    kursor, conn = koneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.Jumlah_produk) as jumlah_terjual from produk p join detail_pesanan dp on dp.Produk_ID_Produk = p.ID_Produk join pesanan ps on ps.id_pesanan = dp.pesanan_id_pesanan join pengantar pe on ps.pengantar_id_pengantar = pe.id_pengantar where p.status_produk = 'Aktif' and pe.tanggal_pengantar <= %s and pe.tanggal_pengantar >= %s group by p.nama_produk order by jumlah_terjual desc limit 5"
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
    kursor, conn = koneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.Jumlah_produk) as jumlah_terjual from produk p join detail_pesanan dp on dp.Produk_ID_Produk = p.ID_Produk join pesanan ps on ps.id_pesanan = dp.pesanan_id_pesanan join pengantar pe on ps.pengantar_id_pengantar = pe.id_pengantar where p.status_produk = 'Aktif' and pe.tanggal_pengantar <= %s and pe.tanggal_pengantar >= %s group by p.nama_produk order by jumlah_terjual asc limit 5"
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
    kursor, conn = koneksiDB()
    query1 = "select p.nama_produk, sum(dp.harga * dp.Jumlah_produk) as jumlah_terjual from produk p join detail_pesanan dp on dp.Produk_ID_Produk = p.ID_Produk join pesanan ps on ps.id_pesanan = dp.pesanan_id_pesanan join pengantar pe on ps.pengantar_id_pengantar = pe.id_pengantar where p.status_produk = 'Aktif' and pe.tanggal_pengantar <= %s and pe.tanggal_pengantar >= %s group by p.nama_produk order by jumlah_terjual asc limit 5"
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

def lihat_produkA(idakun):
    kursor, conn = koneksiDB()
    query = "select * from produk order by status_produk"
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
    kursor, conn = koneksiDB()
    try:
        query = """select p.id_pesanan, p.nama_pemesan, p.status_pesanan, k.nama_karyawan, c.email
        from pesanan p
        join karyawan k on k.id_karyawan = p.karyawan_id_karyawan
        join customer c on c.id_customer = p.customer_id_customer
        join transaksi t on t.id_transaksi = p.transaksi_id_transaksi
        """
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def lihat_detail_pesanan(idakun):
    kursor, conn = koneksiDB()
    try:
        query = """select p.nama_produk, p.harga, dp.jumlah_produk, d.diskon, dp.pesanan_id_pesanan as id_pesanan
        from detail_pesanan dp
        join produk p on p.id_produk = dp.produk_id_produk
        left join diskon d on d.id_diskon = dp.diskon_id_diskon
        """
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def detail_karyawan(idakun):
    kursor, conn = koneksiDB()
    query = """select k.id_karyawan, k.nama_karyawan, k.tanggal_lahir, k.email, k.no_telp, j.nama_jabatan
    from karyawan k 
    join jabatan j on j.id_jabatan = k.jabatan_id_jabatan
    where k.status_karyawan = 'Aktif' and k.jabatan_id_jabatan <> '5'"""
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

def lihat_karyawan(idakun):
    try:
        kursor, conn = koneksiDB()
        query = """select k.nama_karyawan, k.tanggal_lahir, k.email, k.no_telp, j.nama_jabatan, k.status_karyawan
        from karyawan k 
        join jabatan j on j.id_jabatan = k.jabatan_id_jabatan
        where k.jabatan_id_jabatan <> '5'
        order by k.status_karyawan"""
        kursor.execute(query)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def pecat_karyawan(idakun):
    try:
        kursor, conn = koneksiDB()
        query1 = """select k.id_karyawan, k.nama_karyawan, k.tanggal_lahir, k.email, k.no_telp, j.nama_jabatan
        from karyawan k 
        join jabatan j on j.id_jabatan = k.jabatan_id_jabatan
        where k.status_karyawan = 'Aktif' and k.jabatan_id_jabatan <> '5'"""
        query2 = "select id_karyawan from karyawan where status_karyawan = 'Aktif' and jabatan_id_jabatan <> 5"
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
    kursor, conn = koneksiDB()
    while True:
        nama_karyawan = input('Masukkan Nama Karyawan: ')
        nama_karyawan = cek_username(nama_karyawan)
        print('Masukkan Tanggal Lahir Karyawan')
        ttl_karyawan = tanggal()
        email_karyawan = input('Masukkan email karyawan: ')
        email_karyawan = cek_email_karyawan(email_karyawan)
        no_telp_karyawan = input('Masukkan NO Telp karyawan: ')
        no_telp_karyawan = cek_no_telp_karyawan(no_telp_karyawan)
        password_karyawan = input('Masukkan Password karyawan: ')
        password_karyawan = cek_password(password_karyawan)
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
        query1 = "insert into karyawan (nama_karyawan, tanggal_lahir, email, no_telp, jabatan_id_jabatan, akun_id_akun, status_karyawan) values (%s, %s, %s, %s, %s, %s, 'Aktif');"
        query2 = "insert into akun (username, password, role_id_role) values (%s, %s, 2) returning id_akun;"
        try:
            kursor.execute(query2, (nama_karyawan, password_karyawan))
            cocokan = kursor.fetchone()
            id_akun = cocokan[0]
            kursor.execute(query1, (nama_karyawan, ttl_karyawan, email_karyawan, no_telp_karyawan, jabatan_id, id_akun))
            conn.commit()
            print('BUAT AKUN BERHASIL')
            break
        except Exception as e:
            conn.rollback()
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def tanggal():
    try:
        tanggal = questionary.text("Tanggal: ").ask()
        tanggal = cek_tanggal(tanggal)
        bulan = questionary.text("Bulan: ").ask()
        bulan = cek_bulan(bulan)
        tahun = questionary.text("Tahun: ").ask()
        tahun = cek_tahun(tahun)
        hasil_tanggal = dt.date(tahun, bulan, tanggal)
        return hasil_tanggal
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")

def perbarui_produk(idakun):
    kursor, conn = koneksiDB()
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

def hapus_produk(idakun):
    kursor, conn = koneksiDB()
    query1 = "select id_produk, nama_produk, harga, stock from produk where status_produk = 'Aktif' order by id_produk;"
    query2 = "select id_produk from produk where status_produk = 'Aktif' order by id_produk;"
    query3 = "update produk set status_produk = 'Tidak Aktif' where id_produk = %s"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            if data is None:
                print('Tidak Ada Data Yang Bisa Dihapus')
                break
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
    kursor, conn = koneksiDB()
    query1 = "select id_produk, nama_produk, harga, stock from produk where status_produk = 'Tidak Aktif' order by id_produk;"
    query2 = "select id_produk from produk where status_produk = 'Tidak Aktif' order by id_produk;"
    query3 = "update produk set status_produk = 'Aktif' where id_produk = %s"
    while True:
        try:
            kursor.execute(query1)
            data = kursor.fetchall()
            if data is None:
                print('Tidak Ada Data Yang Bisa Dikembalikan')
                break
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
    kursor, conn = koneksiDB()
    query = "insert into produk (nama_produk, harga, stock, status_produk) values (%s, %s, 0, 'Aktif')"
    while True:
        try:
            nama_produk = input('Masukkan Nama Produk Yang Mau Ditambahkan: ')
            nama_produk = cek_nama_produk(nama_produk)
            harga = input('Masukkan Harga Produk: ')
            harga = cek_harga(harga)
            kursor.execute(query, (nama_produk, harga))
            conn.commit()
            print('Penambahan Produk Berhasil')
            admin_pilih = questionary.select(
            "Apakah Ada Produk Lagi Yang Mau Ditambah?:",
            choices=['iya', 'tidak']).ask()
            if admin_pilih == 'iya':
                continue
            elif admin_pilih == 'tidak':
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
        finally:
            kursor.close()
            conn.close()

def ubah_harga(idakun):
    kursor, conn = koneksiDB()
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
            admin_pilih = questionary.select(
            "Apakah Ada Produk Lagi Yang Mau Diubah Harganya?:",
            choices=['iya', 'tidak']).ask()
            if admin_pilih == 'iya':
                continue
            elif admin_pilih == 'tidak':
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue
    kursor.close()
    conn.close()

#Customerr---------------------------------------------------------------------------------------------------------------
def menu_customer(idakun):
    kursor, conn = koneksiDB()
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
                lihat_pesanan_customer(idakun)
                continue
            elif pilih_menu == "Keluar":
                break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            continue

def lihat_pesanan_customer(idakun):
    kursor, conn = koneksiDB()
    query1 = "select p.ID_Pesanan from pesanan p join customer c on c.ID_Customer = p.customer_ID_Customer where c.ID_Customer = %s"
    query2 = "select p.ID_Pesanan, p.nama_pemesan, p.status_pesanan from pesanan p join customer c on c.ID_Customer = p.customer_ID_Customer where c.ID_Customer = %s"
    try:
        kursor.execute(query2)
        data = kursor.fetchall()
        header= [d[0]for d in kursor.description]
        print (tabulate(data, headers=header, tablefmt='psql'))
        kursor.execute(query1)
        data = kursor.fetchall()
        data_list = [i[0] for i in data]
        print('======Id Pesanan Produk======')
        for i in data:
            print(f'Id Pesanan {i[0]}')
        while True:
            try:
                customer_input = int(input('Pilih Id Pesanan Yang Mau Dicek: '))
                if customer_input not in data_list:
                    customer_input = int(input('Pilih Id Pesanan Yang Mau Dicek: '))
                    continue
                break
            except ValueError:
                print("Input harus berupa angka!")
                continue
        lihat_satu_pesanan(idakun, customer_input)
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()
        
def lihat_satu_pesanan(idakun, idpesanan):
    kursor, conn = koneksiDB()
    query2 = "select nama_pemesan from pesanan where ID_Pesanan = %s"
    query3 = """select pr.nama_produk, dp.harga, dp.Jumlah_Produk from detail_pesanan dp 
    join pesanan p on p.ID_Pesanan = dp.Pesanan_ID_Pesanan 
    join customer c on c.ID_Customer = p.customer_ID_Customer
    join produk pr on pr.ID_Produk = dp.Produk_ID_Produk
    where p.ID_Pesanan = %s"""
    query4 = "select ap.Jalan_Pesanan, a.Nama_Area from Alamat_Pesanan ap join Area a on a.ID_Area = ap.Area_ID_Area join pesanan p on p.Alamat_Pesanan_ID_Alamat_Pesanan = ap.ID_Alamat_Pesanan where p.ID_pesanan = %s"
    query5 = "select t.tanggal_transaksi from transaksi t join pesanan p on p.Transaksi_ID_Transaksi = t.ID_Transaksi where p.id_pesanan = %s"
    query6 = "select a.Harga_antar from area a join alamat_pesanan ap on ap.Area_ID_Area = a.ID_Area join pesanan p on p.Alamat_Pesanan_ID_Alamat_Pesanan = ap.ID_Alamat_Pesanan where ID_pesanan = %s"
    query7 = "select sum(dp.produk_id_produk) from detail_pesanan dp join pesanan p on p.id_pesanan = dp.pesanan_id_pesanan where id_pesanan = %s"
    query8 = "select d.diskon from diskon d join detail_pesanan dp on dp.diskon_ID_Diskon = d.id_diskon join pesanan p on p.id_pesanan = dp.pesanan_id_pesanan where p.id_pesanan = %s"
    try:
        kursor.execute(query3, (idpesanan,))
        id_pesanan = kursor.fetchall()
        detail_produk = []
        nomor = 0
        harga_semua = 0
        for i in id_pesanan:
            nomor += 1
            harga_satu_produk = i[1] * i[2]
            harga_semua += harga_satu_produk
            data = f"""{nomor}. {i[0]}  
            {i[2]} x RP{i[1]}   {harga_satu_produk}
            """
            detail_produk.append(data)
        kursor.execute(query5, (idpesanan, ))
        tanggal = kursor.fetchone()
        tanggal = tanggal[0]
        kursor.execute(query2, (idpesanan, ))
        nama = kursor.fetchone()
        nama = nama[0]
        batas()
        print(f"{tanggal} {nama:>64}")
        batas()
        for i in detail_produk:
            print(i)
        batas()
        kursor.execute(query7, (idpesanan, ))
        Quantity = kursor.fetchone()
        Quantity = Quantity[0]
        kursor.execute(query6, (idpesanan, ))
        harga_antar = kursor.fetchone()
        harga_antar = harga_antar[0]
        harga_semua += harga_antar
        kursor.execute(query8, (idpesanan, ))
        diskon = kursor.fetchone()
        diskon = diskon[0]
        print(f"Diskon : {diskon:>64}")
        print(f"Total Quantity : {Quantity:>64}")
        print(f"Total {harga_semua:>64}")
        kursor.execute(query4, (idpesanan, ))
        alamat = kursor.fetchone()
        jalan = alamat[0]
        area = alamat[1]
        print(f"Lokasi :{jalan} {area}")
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")

    kursor.close()
    conn.close()

def pesanan_customer(idakun):
    kursor, conn = koneksiDB()
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

def area_customer():
    kursor, conn = koneksiDB()
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
    return nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, Status_Transaksi, area_pesanan
            
def struk_pesanan(nama_pemesan, alamat_pesanan, metode_pembayaran, produk_dipesan, jumlah, harga_pesanan, area_pesanan, diskon_produk_asli):
    kursor, conn = koneksiDB()
    query = "select harga from produk where nama_produk = %s"
    query2 = "select harga_antar from Area where Nama_Area = %s"
    try:
        print(f"Nama Pemesan adalah {nama_pemesan}")
        banyak = len(produk_dipesan)
        simpan_pesanan = []
        kursor.execute(query2, (area_pesanan, ))
        harga_antar = kursor.fetchone()
        harga_antar = harga_antar[0]
        for i in range(banyak):
            kursor.execute(query, (produk_dipesan[i],))
            data = kursor.fetchone()
            harga_produk = data[0]
            pesanan = [produk_dipesan[i], jumlah[i], harga_produk]
            simpan_pesanan.append(pesanan)
        print(tabulate(simpan_pesanan, headers =["Produk","jumlah", "Harga Produk"]))
        print(f'Total Harga Pesanan = {harga_pesanan}')
        print(f"diskon produk : {diskon_produk_asli}")
        print(f"Alamat Pesanan Berada Di {alamat_pesanan} dan Berada di area {area_pesanan}")
        print(f"Metode Pembayaran Menggunakan {metode_pembayaran}")
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def transaksi_pesanan(idakun, produk_dipesan, jumlah, sisa_stock, id_produk):
    kursor, conn = koneksiDB()
    query = "select harga from produk where nama_produk = %s"
    try:
        diskon_produk_asli, id_diskon = diskon_customer()
        diskon_produk = (100 - diskon_produk_asli) / 100
        banyak = len(produk_dipesan)
        simpan_pesanan = []
        harga = []
        harga_pesanan = 0
        for i in range(banyak):
            kursor.execute(query, (produk_dipesan[i],))
            data = kursor.fetchone()
            harga_produk = data[0]
            harga.append(harga_produk)
            pesanan = [produk_dipesan[i], jumlah[i], harga_produk]
            simpan_pesanan.append(pesanan)
            harga_pesanan = harga_pesanan + (harga_produk * jumlah[i])
        harga_pesanan = harga_pesanan * diskon_produk
        print(tabulate(simpan_pesanan, headers =["Produk","jumlah", "Harga"]))
        print(f'Total Harga Pesanan = {harga_pesanan}')
        print(f"diskon : {diskon_produk_asli}%")
        customer_pilih = questionary.select(
            "Apakah sudah benar Pesanan anda:",
            choices=["iya,Sudah Benar", "Tidak"]
            ).ask()
        if customer_pilih == "iya,Sudah Benar":
            nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, Status_Transaksi, area_pesanan = identitas_customer()
            struk_pesanan(nama_pemesan, alamat_pesanan, metode_pembayaran, produk_dipesan, jumlah, harga_pesanan, area_pesanan, diskon_produk_asli)
            tanggal = dt.date.today()
            simpan_data(idakun, jumlah, sisa_stock, nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, id_produk, tanggal, Status_Transaksi, harga, id_diskon)
        elif customer_pilih == "Tidak":
            pesanan_customer(idakun)
    except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def simpan_data(idakun, jumlah, sisa_stock, nama_pemesan, alamat_pesanan, id_area_pesanan, metode_pembayaran, id_produk, tanggal, Status_Transaksi, harga, id_diskon):
    kursor, conn = koneksiDB()
    query1 = "insert into Transaksi (Status_Transaksi, tanggal_Transaksi, Metode_Pembayaran) values (%s, %s, %s) returning ID_Transaksi;"
    query2 = "insert into Alamat_Pesanan (Jalan_Pesanan, Area_ID_Area) values (%s, %s) returning ID_Alamat_Pesanan;"
    query3 = "insert into Pesanan (Nama_Pemesan, Status_Pesanan, Karyawan_ID_Karyawan, customer_ID_Customer, Alamat_Pesanan_ID_Alamat_Pesanan, Pengantar_ID_Pengantar, Transaksi_ID_Transaksi) values (%s, %s, %s, %s, %s, %s, %s) returning ID_Pesanan;"
    query4 = "insert into Detail_Pesanan (Harga, Jumlah_Produk, Produk_ID_Produk, Pesanan_ID_Pesanan, diskon_id_diskon) values (%s, %s, %s, %s, %s)"
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
                kursor.execute(query3, (nama_pemesan, status_pesanan_customer, None, idakun, id_alamat, None, id_transaksi))
                id_pesanan = kursor.fetchone()
                if id_pesanan is not None:
                    id_pesanan = id_pesanan[0]
                    banyak_data = len(id_produk)
                    for i in range(banyak_data):
                        kursor.execute(query4, (harga[i], jumlah[i], id_produk[i], id_pesanan, id_diskon))
                        kursor.execute(query5, (sisa_stock[i], id_produk[i]))
                        conn.commit()
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def diskon(idakun):
    kursor, conn = koneksiDB()
    query1 = "insert into Diskon (Tanggal_Awal, Tanggal_Akhir, Kode_voucher, diskon) values (%s, %s, %s, %s)"
    while True:
        try:
            print(f"Masukkan Tanggal Dimulai Diskon")
            tanggal_awal = tanggal()
            print(f"Masukkan Tanggal Akhir Diskon")
            tanggal_akhir = tanggal()
            if tanggal_akhir >= tanggal_awal:
                while True:
                    kode_voucer = input("Buat Kode Voucher Baru: ")
                    if not kode_voucer.strip():
                        print("kode voucher tidak boleh kosong atau spasi saja")
                        continue
                    break
                diskon_produk = input("Masukkan Diskon Baru: ")
                while True:
                    try:
                        if not diskon_produk.strip():
                            print("Diskon Tidak Boleh Kosong dan Spasi Saja")
                            diskon_produk = input("Masukkan Diskon Baru: ")
                            continue
                        diskon_produk = int(diskon_produk)
                        if diskon_produk > 100:
                            print('diskon terlalu banyak')
                            diskon_produk = input("Masukkan Diskon Baru: ")
                            continue
                        break
                    except:
                        print(f"Diskon Yang Dimasukkan Harus Berupa Angka")
                        diskon_produk = input("Masukkan Diskon Baru: ")
                        continue
            else:
                print("Tanggal Akhir Tidak Boleh Kurang Dari Tanggal Dimulai Diskon")
                continue
            kursor.execute(query1, (tanggal_awal, tanggal_akhir, kode_voucer, diskon_produk))
            conn.commit()
            print("Penambahan Diskon Berhasil")
            break
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()

def diskon_customer():
    kursor, conn = koneksiDB()
    query = "select id_diskon from diskon where kode_voucher = %s"
    query2 = "select diskon from diskon where id_diskon = %s"
    query3 = "select tanggal_awal from diskon where id_diskon = %s"
    query4 = "select tanggal_akhir from diskon where id_diskon = %s"
    customer_diskon = questionary.select(
    "Apakah Kamu Punya Kode Voucher:",
    choices=["iya, Saya Punya", "Tidak, Saya Tidak Punya"]
    ).ask()
    try:
        tanggal_sekarang = dt.date.today()
        if customer_diskon == "Tidak, Saya Tidak Punya":
            harga_diskon = 0
        elif customer_diskon == "iya, Saya Punya":
            customer_kode = input("Masukkan Kode Voucher Yang kamu punya: ")
            while True:
                if not customer_kode.strip():
                    print("Kode Voucher Tidak Boleh Kosong atau Spasi")
                    customer_kode = input("Masukkan Kode Voucher Yang kamu punya: ")
                    continue
                break
            kursor.execute(query, (customer_kode, ))
            data = kursor.fetchone()
            if data is not None:
                data = data[0]
                kursor.execute(query3, (data, ))
                tanggal_awal = kursor.fetchone()
                tanggal_awal = tanggal_awal[0]
                kursor.execute(query4, (data, ))
                tanggal_akhir = kursor.fetchone()
                tanggal_akhir = tanggal_akhir[0]
                if tanggal_awal <= tanggal_sekarang <= tanggal_akhir:
                    kursor.execute(query2, (data, ))
                    diskon_produk = kursor.fetchone()
                    harga_diskon = diskon_produk[0]
            else:
                print("kode voucher tidak ada")
                harga_diskon = 0
    except Exception as e:
        print(f"Terjadi Kesalahan : {e}")
    kursor.close()
    conn.close()
    return harga_diskon, data

#--------------------------
def lihat_produk_karyawan(idkaryawan):
    kursor, conn = koneksiDB()
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
    kursor, conn = koneksiDB()
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
    kursor, conn = koneksiDB()
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
        

login()


def konfirmasi_pesanan(idkaryawan):
    kursor, conn = koneksiDB()
    query1 = "SELECT id_pesanan, nama_pemesan from pesanan order by id_pesanan where status_pesanan = 'Diantar' "
    query2 = "update pesanan set status_pesanan = 'Diterima' where id_pesanan = %s"
    
    
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
            
            #Update Status
            kursor.execute(query2, (input_id,))
            conn.commit()
            print ("Pesanan sudah diterima!!")  
        
            
            
        except Exception as e:
            print (f"Terjadi Kesalahan : {e}")
            
        finally:
            kursor.close()
            conn.close()           
        break  

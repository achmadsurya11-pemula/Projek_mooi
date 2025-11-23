import psycopg2
import os
import pyfiglet
from tabulate import tabulate


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
    pagar()
    logo_kami = "MOOI DONAT LEZAT"
    figlogo = pyfiglet.figlet_format(logo_kami, font="standard")
    print (figlogo)
    pagar()


def login():
    while True:
        print ("====== Login Akun Sebagai ======")
        print ("1. Login sebagai admin\n2. Login sebagai customer\n3. Login sebagai karyawan")
        akun_pengguna = input ("Pilih Login Sebagai:")
        try:
            if akun_pengguna == "1":
                login_admin()
            elif akun_pengguna == "2":
                login_customer()
            elif akun_pengguna == "3":
                login_karyawan()
                break
        except:
            print ("Pilihan yang anda masukan salah, silahkan pilih kembali..")
    
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
                register()
            else: 
                print ("pilihan tidak ada")
        except:
            print("pilihan tidak valid")
            
       
def login_customer():
    while True:
        kursor, conn = KoneksiDB()
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
                conn.close()
                break
            else:
                print('======LOGIN GAGAL======\nKesalahan Pada Username atau Password, Silahkan Ulangi Lagi')
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")


def login_admin():
    while True:
        kursor, conn = KoneksiDB()
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
    kursor, conn = KoneksiDB()
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

def lihat_produk_karyawan():
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


def update_stock():
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
        
                
def kelola_pesanan_cust():
    clear()
    conn, kursor = KoneksiDB()
    query1 = "SELECT id_pesanan, nama_pesanan from pesanan order by id_pesanan"
    query2 = '''
    select pr.nama_produk, dp.jumlah_produk, dp.harga
    from pesanan p
    join detail_pesanan dp on p.id_pesanan=dp.pesanan_id_pesanan
    join produk pr on dp.produk_id_produk = pr.id_produk 
    where id_pesanan = %s
    '''
    query3 = "update pesanan set status_pesanan = 'Diantar' where id_pesanan = %s"
    query4 = '''
    select p.nama_pesanan, pr.nama_produk, dp.jumlah_produk, dp.harga, p.status_pesanan
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
            print ("==========PILIH ID PESANAN==========")    
            try:
                input_id = int (input("Pilih ID pesanan yang mau diproses: "))
                while input_id not in data_list:
                    print ("ID Pesanan yang anda masukan salah..")
                    input_id = int (input("Pilih ID pesanan yang mau diproses: "))
                    continue
            except ValueError:
                print ("Inputan harus berupa angka!!")
                continue
            
            #Menampilkan Detail Pesanan
            kursor.execute(query2, (input_id,))
            data2 = kursor.fetchall()
            header2 = [d[0] for d in kursor.description]
            print (tabulate(data2, headers=header2, tablefmt='psql'))
            
            #Konfirmasi
            input_karyawan = (input("Apakah pesanan akan dikirimkan?"))
            enter()
            
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
                lihat_produk_karyawan()
                enter()
                continue
            elif pilihan_karyawan == "2":
                update_stock()
                enter()
                continue
            elif pilihan_karyawan == "3":  
                kelola_pesanan_cust()
                continue
            elif pilihan_karyawan == "4":  
                break
            else:
                print("Pilihan Tidak Valid!")
        except:
            print ("Terjadi Kesalahan")


login()
# kelola_pesanan_cust()

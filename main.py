import pathlib
from tkinter import *
from tkinter import ttk
import tkinter
from tokenize import String
import mysql.connector
from PIL import ImageTk, Image
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")

# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result

# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label3 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input3 = OptionMenu(dframe, input_jurusan, *options)
    input3.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    # Input 4
    label4 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    genders = [
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan")
    ]
    input_gender = StringVar()
    i = 20
    for text, gender in genders:
        input_jk = Radiobutton(dframe, text=text, variable=input_gender, value=gender).grid(row=3, column=1, padx=i, pady=10, sticky="w")
        i+=80
    
    #Input 5
    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    input_hobi = StringVar()
    combo = ttk.Combobox(dframe, width=15, textvariable=input_hobi)
    combo['values'] = ["Ngoding", "Rebahan", "Dengerin Lagu"]
    combo['state'] = 'readonly'
    combo.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_gender, input_hobi), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jenis_kelamin, hobi):
    global mydb
    global dbcursor
    
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jenis_kelamin = jenis_kelamin.get()
    hobi = hobi.get()

    # Input data disini
    if (nama == "" or nim == "" or jurusan == "" or jenis_kelamin == "" or hobi == "") :
        btn_ok = Button(top, text="Masih ada yang kosong!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    else :
        query = "INSERT INTO mahasiswa (nim, nama, jurusan, jenis_kelamin, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, jenis_kelamin, hobi)
        dbcursor.execute(query, val)
        mydb.commit() 

        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

# Menampilkan fasilitas
def showFacilities():
    global root
    root.withdraw()

    global img_list
    global labelImg
    global top

    top = Toplevel()
    top.title("Fasilitas Kampus")

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    fileimg1 = os.path.join(THIS_FOLDER, 'project/auditorium.jpg')
    fileimg2 = os.path.join(THIS_FOLDER, 'project/perpustakaan.jpg')
    fileimg3 = os.path.join(THIS_FOLDER, 'project/ruangkelas.jpg')

    img1 = ImageTk.PhotoImage(Image.open(fileimg1))
    img2 = ImageTk.PhotoImage(Image.open(fileimg2))
    img3 = ImageTk.PhotoImage(Image.open(fileimg3))

    img_list = [img1, img2, img3]

    labelImg = Label(top, image=img_list[0])
    # labelImg.pack()
    labelImg.grid(row=1, column=1)
    
    # Backward, Cancel, dan Forward Button
    btn_prev = Button(top, text="<<", anchor="w", command=lambda: prevImage(), state=DISABLED)
    btn_prev.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    btn_cancel = Button(top, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    btn_next = Button(top, text=">>", anchor="w", command=lambda: nextImage(1))
    btn_next.grid(row=1, column=2, padx=10, pady=10, sticky="w")

# Untuk forward foto
def nextImage(img_number):
    global labelImg
    global btn_prev
    global btn_next

    labelImg.grid_forget()
    labelImg = Label(top, image=img_list[img_number])
    labelImg.grid(row=1, column=1)

    # Backward, Cancel, dan Forward Button
    btn_prev = Button(top, text="<<", anchor="w", command=lambda: prevImage(img_number - 1))
    btn_prev.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    btn_cancel = Button(top, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    if(img_number == (len(img_list) - 1)):
        btn_next = Button(top, text=">>", anchor="w", state=DISABLED)
    else:
        btn_next = Button(top, text=">>", anchor="w", command=lambda: nextImage(img_number + 1))
    btn_next.grid(row=1, column=2, padx=10, pady=10, sticky="w")   

# Untuk backward foto
def prevImage(img_number):
    global labelImg
    global btn_prev
    global btn_next

    labelImg.grid_forget()
    labelImg = Label(top, image=img_list[img_number])
    labelImg.grid(row=1, column=1)

    # Backward, Cancel, dan Forward Button
    btn_cancel = Button(top, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    btn_next = Button(top, text=">>", anchor="w", command=lambda: nextImage(img_number + 1))
    btn_next.grid(row=1, column=2, padx=10, pady=10, sticky="w") 
    if(img_number == 0):
        btn_prev = Button(top, text="<<", anchor="w", state=DISABLED)
    else:
        btn_prev = Button(top, text="<<", anchor="w", command=lambda: prevImage(img_number - 1))
    btn_prev.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
def delAll():
    global mydb
    global dbcursor

    query = "DELETE FROM mahasiswa"
    dbcursor.execute(query)
    mydb.commit()

    top = Toplevel()
    # Delete data disini
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Fasilitas Kampus", command=showFacilities, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()

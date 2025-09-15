from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import fileRE

def afficherFacture():    # pour aficher les valeur dans treeview
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM facture "
    cursor.execute(sql2)
    category=cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in category:
            idFacture = row[0]
            dateFacture = row[1]
            totalFacture = row[2]
            idEmployer = row[3]
            usernameEmployer = row[4]
            treeview.insert("", END, values=(idFacture,dateFacture,totalFacture,idEmployer,usernameEmployer))

def comboboxValues(combobox):  # pour afficher les id_facture dans combobox
    options=[]
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT id_facture FROM facture"
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
        options.append(row[0])
        combobox["values"]=options

def factures():  # pour aficher les valeur dans treeview appartir id_facture
    val = combobox0.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql = "SELECT * FROM facture WHERE id_facture=%s"
    cursor.execute(sql, (val,))
    factures = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    if factures:
        for facture in factures:
                idFacture = facture[0]
                dateFacture = facture[1]
                totalFacture = facture[2]
                idEmployer = facture[3]
                usernameEmployer = facture[4]
                treeview.insert("", END, values=(idFacture,dateFacture,totalFacture,idEmployer,usernameEmployer))
    else:
         messagebox.showerror('GESTION DES FACTURES','NO FOUND FACTURE ')
         afficherFacture()


def selectionLine(event):  # pour afficher nouveau fenetre qui donne treeview de valeur de table detailsfacture apartir id_facture
    selected_item = treeview.focus()
    item_values = treeview.item(selected_item, 'values')  
    if item_values: 
        id_facture = item_values[0] 
        root1=Tk()
        root1.title("details facture")
        root1.resizable(False, False)
        root1.geometry("700x230+410+350")
        area=('idDetail','categoryFacture','produitFacture','stockFacture','prixFacture')
        treeview1=ttk.Treeview(root1,columns=area,show='headings',height=10)
        for i in range(5):
            treeview1.column(area[i],width=143,anchor='center')
            treeview1.heading(area[i],text=area[i])
            treeview1.pack()
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        sql = """SELECT d.id_detail, d.category, d.produits, d.stock, d.prix,f.id_facture
            FROM detailsfacture d
            INNER JOIN facture f ON d.id_facture = f.id_facture
            WHERE f.id_facture = %s"""
        cursor.execute(sql, (id_facture,))
        factures = cursor.fetchall()
        for facture in factures:
            idDetail = facture[0]
            categoryFacture = facture[1]
            produitFacture = facture[2]
            stockFacture = facture[3]
            prixFacture = facture[4]
            treeview1.insert("", END, values=(idDetail,categoryFacture,produitFacture,stockFacture,prixFacture))
        root1.mainloop()

def aficherDetailsFacture(): # pour afficher nouveau fenetre qui donne treeview de tout les valeur  de table detailsfacture 
    root2=Tk()
    root2.title("details facture")
    root2.resizable(False, False)
    root2.geometry("700x400+408+250")
    area=('idDetail','categoryFacture','produitFacture','stockProduit','prixProduit')
    treeview1=ttk.Treeview(root2,columns=area,show='headings',height=100)
    for i in range(5):
        treeview1.column(area[i],width=143,anchor='center')
        treeview1.heading(area[i],text=area[i])
        treeview1.pack()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql = """SELECT d.id_detail, d.category, d.produits, d.stock, d.prix,f.id_facture
            FROM detailsfacture d
            INNER JOIN facture f ON d.id_facture = f.id_facture"""
    cursor.execute(sql)
    factures = cursor.fetchall()
    for facture in factures:
        idDetail = facture[0]
        categoryFacture = facture[1]
        produitFacture = facture[2]
        stockFacture = facture[3]
        prixFacture = facture[4]
        treeview1.insert("", END, values=(idDetail,categoryFacture,produitFacture,stockFacture,prixFacture))
    root2.mainloop()



root = Tk()
root.title("gestion des facture")
root.geometry("920x620+200+30")
root.resizable(False, False)
x_offset = (1920 - root.winfo_width()) // 7
y_offset = (1000 - root.winfo_height()) // 12
image_a=Image.open("images/acceui.jpg")
resised=image_a.resize((1900,800))
new = ImageTk.PhotoImage(resised)
label=Label(root,image=new,bg='red')
label.pack()

style = ttk.Style()
style.theme_use('alt')
txt = "SYSTEME DE GESTION DU SEPERMARCHE"
heading = Label(root, text=txt, font=('yu gothic ui', 15, "bold"), fg='black',bd=5,relief=FLAT)
heading.place(x=260, y=2, width=490, height=30)

detailFacture = Button(root, text="DETAIL FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=aficherDetailsFacture)
detailFacture.place(x=37, y=120, width=140, height=45)


detailButton = Button(root, text="TOUT DETAILS", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=afficherFacture)
detailButton.place(x=37, y=190, width=140, height=45)


combobox0 = ttk.Combobox(root, font=(6),width=19)
combobox0.current() 
combobox0.place(x=36, y=260, width=140, height=45)

chercherButton = Button(root, text="SEARCH ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=factures)
chercherButton.place(x=36, y=330, width=140, height=45)             

retourButton = Button(root, text="RETOUR", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageAdmin(root))
retourButton.place(x=38, y=470, width=140, height=45)

lougoutButton = Button(root, text="LOG OUT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageAdmin(root))
lougoutButton.place(x=38, y=540, width=140, height=45)

contenu=Frame(root,bg='white')
contenu.place(x=200,y=120,width=717,height=466)

label=Label(contenu,image=new,bg='red')
label.pack()


options = []


Label(contenu,text='TOUS LES FACTURES', font=('yu gothic ui', 15, "bold")).place(x=250,y=10)
area=('idFacture','dateFacture','totalFacture','idEmployer','username',)
treeview=ttk.Treeview(contenu,columns=area,show='headings',height=100)
for i in range(5):
    treeview.column(area[i],width=143,anchor='center')
    treeview.heading(area[i],text=area[i])
    treeview.place(x=0,y=50)


comboboxValues(combobox0)
afficherFacture()
treeview.bind('<<TreeviewSelect>>', selectionLine)
date = Label(root, text=txt, font=( 15), fg='black',bd=5,relief=FLAT)
date.place(x=450, y=33)
#fileRE.clock(date)

root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()
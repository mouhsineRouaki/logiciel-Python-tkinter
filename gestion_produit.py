from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import fileRE

def afficherProduct():
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM product ORDER BY ID_product"
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
            id = row[0]
            nom = row[1]
            category = row[2]
            stock = row[3]
            prix = row[4]
            date = row[5]
            treeview.insert("", END, values=(id,nom,category,stock,prix,date))
            
        
def valider_nombre(valeur):
    try:
      number = float(valeur) 
    except ValueError:
      messagebox.showerror("Invalid Input", "stock et prix est un valid number.")

def ajouterProduit():
    val1=comboboxproduit.get()
    val2=comboboxCategory.get()
    val3=comboboxStock.get()
    val4=comboboxPrix.get()
    if val1==''and val2=='' and val3==''and val4=='':
        messagebox.showerror('ERORR !!','rmplir tous les champ')
    elif val1=='':
        messagebox.showerror('ERORR !!','please entre le nom de category ')
    elif val2=='':
        messagebox.showerror('ERORR !!','please entre le nom de product que tu dois inserer ')
    elif val3=='': 
        messagebox.showerror('ERORR !!','please entre le prix de products que tu dois Inserer')
    elif val3.isalpha():
        valider_nombre(val3)
    elif val4=='':
        messagebox.showerror('ERORR !!','please entre le stock de product que tu dois inserer ')
    elif val4.isalpha():
        valider_nombre(val4)
    else:
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        sql1 = "INSERT INTO product (Nom_product,Nom_category,stock,prix) VALUES (%s, %s,%s,%s)"
        values1 = ( val1,val2,val3,val4 )
        cursor.execute(sql1, values1)
        connection.commit()
        treeview.delete(*treeview.get_children())
        afficherProduct()
        messagebox.showerror('GESTION DES ADMIN','INSERTION DES DONNES REUISSIR')

def supprimerProduit():
    valeur=comboboxChercher.get()
    line = treeview.selection()
    values = treeview.item(line, 'values')  
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    if line:
        reponse = messagebox.askokcancel("Question", "Voulez-vous supprimer  cette command ?")
        if (reponse==True):
            id_produit = values[0] 
            sql1 = "DELETE FROM product  WHERE  ID_product=%s"
            cursor.execute(sql1, (id_produit,))
            connection.commit()
            treeview.delete(*treeview.get_children())
            afficherProduct()
            viderCombobox()
            messagebox.showerror('GESTION DES ADMIN',' PRODUCT DELETE AVEC SUCCESS')
    elif valeur :
        sql1 = "DELETE FROM product  WHERE Nom_product = %s or ID_product=%s"
        values = (valeur,valeur)
        cursor.execute(sql1, values)
        connection.commit()
        treeview.delete(*treeview.get_children())
        afficherProduct()
        viderCombobox()
        messagebox.showerror('GESTION DES ADMIN',' PRODUCT DELETE AVEC SUCCESS')
    else:
        messagebox.showerror('GESTION DES DELETE','SELECTIONNER OR TAPER LE NOM DE PRODUIT QUI VOUS SUPPRIMER ') 

def modifierProduit():
    val1=comboboxCategory.get()
    val2=comboboxproduit.get()
    val3=comboboxPrix.get()
    val4=comboboxStock.get()
    val5=comboboxChercher.get()
    if val1=='' or val2=='' or val3=='' or val4=='' or val5=='':
        messagebox.showerror('ERORR !!','please rmplir tous les champs  que pour  modifier ')
    else:
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        sql1 = "UPDATE product SET Nom_product=%s ,Nom_category=%s,stock = %s,prix=%s WHERE Nom_product = %s or ID_product=%s"
        values = (val2,val1,val4,val3,val5,val5)
        cursor.execute(sql1, values)
        connection.commit()
        treeview.delete(*treeview.get_children())
        afficherProduct()
        viderCombobox()
        messagebox.showerror('GESTION DES ADMIN',' PRODUCT UPDATE AVEC SECCUFEL')

def viderCombobox():
    comboboxChercher.set("")
    comboboxCategory.set("")
    comboboxproduit.set("")
    comboboxPrix.set("")
    comboboxStock.set("")
    
def remplirCombobox(event):
    line = treeview.focus()
    values = treeview.item(line, 'values')
    if line:
        comboboxChercher.set(values[0])
        comboboxCategory.set(values[2])
        comboboxproduit.set(values[1])
        comboboxPrix.set(values[4])
        comboboxStock.set(values[3])

def valuesProduit():
    options=[]
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT Nom_product FROM product"
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
        options.append(row[0])
        comboboxproduit["values"]=options

def chercheProduit():
    val1=comboboxChercher.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM product WHERE Nom_product=%s or ID_product=%s "
    cursor.execute(sql2,(val1,val1,))
    category=cursor.fetchall()
    if category :
        treeview.delete(*treeview.get_children())
        for row in category:
                id = row[0]
                nom = row[1]
                category = row[2]
                stock = row[3]
                prix = row[4]
                date = row[5]
                treeview.insert("", END, values=(id,nom,category,stock,prix,date))
                comboboxproduit["values"]=row[1]
                comboboxPrix["values"]=row[3]
                comboboxStock["values"]=row[4]
                viderCombobox()
    else :
        messagebox.showerror('GESTION DES EPRODUCT','NO FOUND PRODUCT ')
        treeview.delete(*treeview.get_children())
        afficherProduct()

root = Tk()
root.title("AJOUTER PRODUCT")
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
style.theme_use('clam')
txt = "AJOUTER PRODUITS"
titre = Label(root, text=txt, font=('yu gothic ui', 15, "bold"),bg='#9a258f', fg='white',bd=5,relief=FLAT)
titre.place(x=250, y=2, width=470, height=30)


ajouterButton = Button(root, text="ADD PRODUCT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :ajouterProduit())
ajouterButton.place(x=37, y=120, width=140, height=45)

modifierButton = Button(root, text="UPDATE PRODUCT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda :modifierProduit())
modifierButton.place(x=37, y=190, width=140, height=45)

supprimerButton = Button(root, text="DELETE PRODUCT  ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:supprimerProduit())
supprimerButton.place(x=36, y=260, width=140, height=45)

comboboxChercher = ttk.Combobox(root, font=(6),width=19)
comboboxChercher.place(x=36, y=330, width=140, height=45)

chercherButton = Button(root, text="SEARCH ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:chercheProduit())
chercherButton.place(x=36, y=400, width=140, height=45)

dateLabel = Label(root, text=txt, font=( 15), fg='black',bd=5,relief=FLAT)
dateLabel.place(x=450, y=33)
fileRE.clock(dateLabel)                


                 
retourButton = Button(root, text="RETOUR", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageAdmin(root))
retourButton.place(x=38, y=470, width=140, height=45)


logoutButton = Button(root, text="LOG OUT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageLogin(root))
logoutButton.place(x=38, y=540, width=140, height=45)

contenu=Frame(root,bg='white')
contenu.place(x=200,y=120,width=717,height=466)

heading=Label(contenu,text='AJOUTER PRODUCT',font=('Areal',19),bg='white',relief=FLAT)
heading.grid(row=0,column=1,padx=10,pady=10)

categoryLabel=Label(contenu,text='  Label product :',font=('Areal',10),bg='white')
categoryLabel.grid(row=1,column=0,sticky='w',padx=20)

comboboxCategory = ttk.Combobox(contenu, font=(6),width=19,state='readonly')
comboboxCategory.grid(row=2,column=0,sticky='w',padx=30)

productLabel=Label(contenu,text='Nom product :',font=('Areal',10),bg='white')
productLabel.grid(row=1,column=1,sticky='w',padx=5)

comboboxproduit = ttk.Combobox(contenu, font=(6),width=19)
comboboxproduit.grid(row=2,column=1,sticky='w',padx=5)

viderButton = Button(contenu, text="VIDER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :viderCombobox())
viderButton.place(x=500, y=80, width=140, height=45)

prixLabel=Label(contenu,text='  prix :',font=('Areal',10),bg='white')
prixLabel.grid(row=3,column=0,sticky='w',padx=20)

comboboxPrix = ttk.Combobox(contenu, font=(6),width=19)
comboboxPrix.grid(row=4,column=0,sticky='w',padx=30)

stockLabel=Label(contenu,text='stock :',font=('Areal',10),bg='white')
stockLabel.grid(row=3,column=1,sticky='w',padx=5)

comboboxStock = ttk.Combobox(contenu, font=(6),width=19)
comboboxStock.grid(row=4,column=1,sticky='w',padx=5)


area=('ProductID','ProductNom','Category','Stock ','Price','date')
treeview=ttk.Treeview(contenu,columns=area,show='headings',height=10)
for i in range(6):
    treeview.column(area[i],width=117,anchor='center')
    treeview.heading(area[i],text=area[i])
    treeview.place(x=0,y=150)

scrollbar_verticale = ttk.Scrollbar(contenu, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar_verticale.set)
    
scrollbar_verticale.place(relx=0, rely=0, relheight=0.95)
treeview.place(relx=0.02, rely=0.02, relwidth=0.97, relheight=0.70) 

treeview.bind('<<TreeviewSelect>>', remplirCombobox)
afficherProduct()
fileRE.values_category(comboboxCategory)
valuesProduit()
root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()
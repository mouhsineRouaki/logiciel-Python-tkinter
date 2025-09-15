from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import fileRE
import json
from datetime import datetime

#---------------------------------------------- les fonctions--------------------------------------------------------------------
def get_info_employer():# pour recuperer les donnes d utilisateur appartir fichier(donnes.json)
        with open("donnes.json", "r") as f:
            json_data = f.read()
        login_data = json.loads(json_data)
        id = login_data["id"]
        email= login_data["email"]
        username= login_data["username"]
        return id,email,username 
id,email,username= get_info_employer() #extrait les les donnes dans des variables 

def values_produit(event): #pour recuperer les nom produit appartir la base de donner et afficher dans combobox
    category = category_combobox.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql = """SELECT p.Nom_product
                FROM product p
                INNER JOIN category c ON p.Nom_category = c.Nom_category
                WHERE c.Nom_category = %s"""
    cursor.execute(sql, (category,))
    products = [row[0] for row in cursor.fetchall()]
    if category:
        produit_combobox.config(state=NORMAL)
        produit_combobox.config(state='readonly')
        produit_combobox['values'] = products


def values_prix(event):#pour recuperer le prix de ce produit appartir la base de donner et afficher dans combobox
    produit = produit_combobox.get()
    connection=fileRE.connectiondb()
    cursor = connection.cursor()
    sql = "SELECT stock FROM product WHERE Nom_product = %s"
    cursor.execute(sql, (produit,))
    stock_available = cursor.fetchone()
    if produit:
        sql = "SELECT * FROM product WHERE Nom_product = %s"
        cursor.execute(sql, (produit,))
        prix = [row[4] for row in cursor.fetchall()]
        prix_combobox.config(state=NORMAL)
        prix_combobox.config(state='readonly')
        quantite_combobox.config(state=NORMAL)
        prix_combobox['values'] = prix
        prix_combobox.current(0)
        if stock_available: 
            stock_value = stock_available[0] 
            label_stock.config(text=f"Stock: {stock_value}") 



def disabledCombobox():#pou disabled stock et prix et produit if category ne pas saisir
    produit = produit_combobox.get()
    category = category_combobox.get()
    prix = prix_combobox.get()
    if produit == '':
        prix_combobox.config(state='disabled')
        quantite_combobox.config(state='disabled')
    else:
        prix_combobox.config(state='normal')
        quantite_combobox.config(state='normal')
    if category != '':
        produit_combobox.config(state='normal')
    else:
        produit_combobox.config(state='disabled')


def valider_stock2(valeur): #pour valide if stock not float
    try:
      number = float(valeur)
    except ValueError:
      messagebox.showerror("Invalid Input", "stock  est un valid number.")

def ajouter_info_facture():# pour ajouter le command de combobox dans facture
    #RECUPERER LES VALEURS DE COMBOBOX
    DATE = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ID_C =ID_entry.get()
    email_C = email_entry.get()
    Nom_C = nom_entry.get()
    category_P=category_combobox.get()
    produit_P=produit_combobox.get()
    prix = prix_combobox.get()
    quantite=quantite_combobox.get()
    valider_stock2(quantite)
    total_P=int(prix) * int(quantite)

    #CONFIGURE LES VALEURS DANS FACTURE DATE ET CLIENT ET NUMERO FACTURE
    date.config(text=DATE)
    client.config(text=Nom_C)
    get_numeroFacture()

    if category_P == "":
        messagebox.showerror('ERROR !!', 'selectionner category tu dois commande')
    else:
        valider_stock(produit_P,category_P,prix,total_P) 
        quantite_combobox.delete(0,END)
        prix_combobox.set("")
        produit_combobox.set("")
        category_combobox.set("")
        disabledCombobox()
        label_stock.config(text="Stock:") 

def get_numeroFacture(): #pour recuperer le numero de facture suivante et aficher dans facture
    connection=fileRE.connectiondb()
    cursor=connection.cursor()
    cursor.execute('SELECT id_facture FROM facture ORDER BY id_facture DESC LIMIT 1;')
    line=cursor.fetchone()
    num_facture=line[0]+1
    numero_facture.config(text=f"{str(num_facture)}")
    return num_facture


def valider_stock(produit_P,category_P,prix,total_P):# pour valider stock et insert les valeur dans treeview et mise a jour stock
    quantite = int(quantite_combobox.get())
    connection=fileRE.connectiondb()
    cursor = connection.cursor()
    sql ="SELECT stock FROM product WHERE Nom_product = %s"
    cursor.execute(sql, (produit_P,))
    stock_available = cursor.fetchone()[0] 
    nouveau_stock=stock_available - quantite
    if quantite > stock_available:
        messagebox.showerror('ERROR !!', 'Desole!! le stock est puise'+str({stock_available}))
    elif quantite <= 0:
        messagebox.showerror('ERROR !!', 'le stock dois etre superieure a 0 pour commander')
    else:
        tree_data = [category_P,produit_P,quantite,prix]
        treeview.insert('', 'end', values=tree_data) # ajouter les valeur dans treeview
        get_total()    # calculer le total appartir de treeview
        update_stock(nouveau_stock) # mise a jour le stock dans la base de donner
    

def delete_command(): # supprimer la command selectionner dans treeview
    line = treeview.selection()
    if line:
        for row in line:
            reponse = messagebox.askokcancel("Question", "Voulez-vous supprimer  cette command ?")
            if (reponse==True):
                treeview.delete(row)
                messagebox.showerror('GESTION DES FACTURE','command va supprimer avec success')
                get_total()
    else:
        messagebox.showerror('GESTION DES FACTURE',' Selectionner line que tu dois supprimer')
       
def get_total(): # pour 
    items = treeview.get_children()
    totalT = 0
    for item in items:
        values = treeview.item(item, "values")
        prix = float(values[2])
        stock = int(values[3])
        totalT += prix * stock
    total.config(text=f"{totalT} Dh")
    return totalT

def vider_facture():
    treeview.delete(*treeview.get_children())
    get_total()

def generer_facture(): # pour ajouter
    num_facture=get_numeroFacture()
    items = treeview.get_children()
    donnees = []
    if not items:
        messagebox.showinfo("Information", "please!! ajouter des command pour generete facture")
    else:
        for item in items:
            values = treeview.item(item, "values")
            category,produit,stock,prix = values
            donnees.append({
                "category": category,
                "produit": produit,
                "stock": int(stock),
                "prix":int(prix),
                "numero_facture":num_facture
            })

        with open("donnees.json", "w") as fichier:
            json.dump(donnees, fichier, indent=4)
            ajouter_facture()
            treeview.delete(*treeview.get_children())
        get_numeroFacture()
        ajouterDetailFacture()
        get_total()
        messagebox.showinfo("Succès", "Données sauvegardées avec succès !")


def update_stock(nouveau_stock): # mise a jour le stock
    produit=produit_combobox.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql1 = "UPDATE product SET stock =%s WHERE Nom_product =%s"
    cursor.execute(sql1, (nouveau_stock,produit,))
    connection.commit()
    
def ajouter_facture(): # ajouter les donnees dans table facture
    total=get_total()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql1 = f"INSERT INTO facture (total,id_employer,username) VALUES ({total},{id},%s)"
    cursor.execute(sql1,(username,))
    connection.commit()

def ajouterDetailFacture(): # ajouter les donnees dans table detailsfacture
        with open('donnees.json', 'r') as file:
            data = file.read().strip()
            if not data:
                raise ValueError("The JSON file is empty")
            data = json.loads(data)
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        insert_query = "INSERT INTO detailsfacture (category, produits, stock,prix,id_facture) VALUES (%s, %s, %s,%s,%s)"
        for entry in data:
            cursor.execute(insert_query, (
                entry['category'],
                entry['produit'],
                entry['stock'],
                entry['prix'],
                entry['numero_facture']
            ))
            connection.commit()
#----------------------fenetre de user---------------------------------------------------------------
root = Tk()

root.title("SUPER Marque")
root.geometry("1250x650")

root.resizable(False,False)

x_offset = (1920 - root.winfo_width()) // 35
y_offset = (1080 - root.winfo_height()) // 30


root.geometry(f"+{x_offset}+{y_offset}") 
root.resizable(False, False)

#----------get id et email et username in donnes.json-----------------------------
titre=Label(root,text=f'Bonjour {username} dans Super Marque',font=('yu gothic ui', 15, "bold"),bg='cyan',fg='black')
titre.pack(side=TOP,fill=X)

lbheure=Label(root,bg='cyan')
lbheure.place(x=0,y=0)

Frame=Frame(root,bd=2,bg='white')
Frame.place(x=0,y=30,width=1400,height=617)
#--------------------------------------------------------client-----------------------------------------------
client=LabelFrame(Frame,text='client',font=('yu gothic ui', 15, "bold"),bg='white')
client.place(x=9,y=1,width=1226,height=80)

ID_client=Label(client,text='ID :',font=('yu gothic ui', 15, "bold"),bg='white')
ID_client.grid(column=0,row=1,sticky=W,padx=40,pady=0)

Email_client=Label(client,text='Email :',font=('yu gothic ui', 15, "bold"),bg='white')
Email_client.grid(column=2,row=1,sticky=W,padx=35,pady=0)

Nom_client=Label(client,text='Username :',font=('yu gothic ui', 15, "bold"),bg='white')
Nom_client.grid(column=4,row=1,sticky=W,padx=0,pady=0)

ID_entry=ttk.Combobox(client,values=id,font=('yu gothic ui', 15, "bold"),state='readonly')
ID_entry.current(0) 
ID_entry.grid(column=1,row=1,sticky=W,padx=5,pady=0)

email_entry=ttk.Combobox(client,values=email,font=('yu gothic ui', 15, "bold"),state='readonly')
email_entry.current(0) 
email_entry.grid(column=3,row=1,sticky=W,padx=40,pady=0)

nom_entry=ttk.Combobox(client,values=username,font=('yu gothic ui', 15, "bold"),state='readonly')
nom_entry.current(0) 
nom_entry.grid(column=5,row=1,sticky=W,padx=40,pady=0)

#-------------------------------------------------------------produit-----------------------------------------------------------------------------------

produits=LabelFrame(Frame,text='produits',font=('yu gothic ui', 15, "bold"),bg='white')
produits.place(x=10,y=80,width=250,height=450)

category=Label(produits,text='Category :',font=('yu gothic ui', 15, "bold"),bg='white')
category.grid(column=0,row=1,sticky=W,padx=10,pady=2)

nom_produits=Label(produits,text='Produit :',font=('yu gothic ui', 15, "bold"),bg='white')
nom_produits.grid(column=0,row=3,sticky=W,padx=10,pady=2)

prix_produits=Label(produits,text='Prix :',font=('yu gothic ui', 15, "bold"),bg='white')
prix_produits.grid(column=0,row=5,sticky=W,padx=10,pady=2)

quantite_produits=Label(produits,text='Quantite :',font=('yu gothic ui', 15, "bold"),bg='white')
quantite_produits.grid(column=0,row=7,sticky=W,padx=10,pady=2)

category_combobox=ttk.Combobox(produits,state='readonly',font=('yu gothic ui', 13, "bold"))
category_combobox.grid(column=0,row=2,sticky=W,padx=10,pady=2)
category_combobox.bind("<<ComboboxSelected>>", values_produit)

produit_combobox=ttk.Combobox(produits,font=('yu gothic ui', 13, "bold"))
produit_combobox.grid(column=0,row=4,sticky=W,padx=10,pady=2)
produit_combobox.bind("<<ComboboxSelected>>", values_prix)

prix_combobox=ttk.Combobox(produits,font=('yu gothic ui', 13, "bold"))
prix_combobox.grid(column=0,row=6,sticky=W,padx=10,pady=2)


quantite_combobox=ttk.Combobox(produits,font=('yu gothic ui', 13, "bold"))
quantite_combobox.grid(column=0,row=8,sticky=W,padx=10,pady=2)

label_stock=Label(produits,text='Stock :',font=('yu gothic ui', 11, "bold"),fg='orange',bg='white')
label_stock.place(x=10,y=288,width=100,height=20,)

btn_ajouter=Button(produits,text='AJOUTER',bd=5,command=ajouter_info_facture)
btn_ajouter.place(x=50,y=330,width=140, height=35)

btn_delete=Button(produits,text=' DELETE ',bd=5,command=delete_command)
btn_delete.place(x=50,y=380,width=140, height=35)

#-------------------------------gestion des facture-------------------------------
facture=LabelFrame(Frame,text='facture',font=('yu gothic ui', 15, "bold") ,bg='white')
facture.place(x=270,y=80,width=700,height=450)

image_a=Image.open("images\Facture.jpg")
resised=image_a.resize((680,420))
new = ImageTk.PhotoImage(resised)

label_facture=Label(facture,image=new,font=('yu gothic ui', 15, "bold") ,bg='white')
label_facture.place(x=0,y=0,width=690,height=410)

date=Label(facture,bg='white',fg='black',font=('yu gothic ui', 15, "bold"))
date.place(x=70,y=-14)

client=Label(facture,bg='white',fg='black',font=('yu gothic ui', 15, "bold"))
client.place(x=80,y=16)

numero_facture=Label(facture,bg='white',fg='black',font=('yu gothic ui', 15, "bold"))
numero_facture.place(x=160,y=48)

total=Label(facture,text=f"0 Dh" ,bg='#a4a4a4',fg='white',font=('yu gothic ui', 15, "bold"))
total.place(x=545,y=360)

facture_frame = ttk.Frame(facture, style='Facture.TFrame')
facture_frame.place(x=0, y=143, width=650, height=200)


facture_style = ttk.Style()
facture_style.configure('Facture.TFrame', background='white')

area=('CATEGORY','PRODUIT','STOCK','PRIX')
treeview=ttk.Treeview(facture_frame,columns=area,show='headings',height=200)
for i in range(4):
    treeview.column(area[i],width=162,anchor='center')
    treeview.heading(area[i],text=area[i])
    treeview.place(x=0,y=0)
scrollbar_verticale = ttk.Scrollbar(facture_frame, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar_verticale.set)
    
scrollbar_verticale.place(relx=0, rely=0, relheight=0.95)
treeview.place(relx=0.03, rely=0.02, relwidth=1, relheight=1)
#------------------------------gestion des button---------------------------------
button=LabelFrame(Frame,text=' Gestion de facture',font=('yu gothic ui', 15, "bold") ,bg='white')
button.place(x=980,y=80,width=254,height=450)


add = Button(button, text="GENERER FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=generer_facture)
add.place(x=30, y=120, width=200, height=45)


update = Button(button, text="VIDER FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=vider_facture)
update.place(x=30, y=210, width=200, height=45)


delete = Button(button, text="LOGOUT  ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageLogin(root))
delete.place(x=30, y=300, width=200, height=45)

messagebox.showinfo("Bonjour", f"Bonjour monsieur {username} a superM meilleure supermarcket")



disabledCombobox()
fileRE.values_category(category_combobox)
root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
fileRE.clock(lbheure)
root.mainloop()
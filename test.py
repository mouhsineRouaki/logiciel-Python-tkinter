from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import fileRE
import json
from datetime import datetime
import subprocess
#---------------------------------------------- les fonctions--------------------------------------------------------------------
def get_info_employer():
        with open("donnes.json", "r") as f:
            json_data = f.read()
        login_data = json.loads(json_data)
        id = login_data["id"]
        email= login_data["email"]
        username= login_data["username"]
        return id,email,username 
id,email,username= get_info_employer()


def values_produit(event):
    category = category_combobox.get()
    if category:
        produit_combobox.config(state=NORMAL)
        produit_combobox.config(state='readonly')
        products = get_produit(category)
        produit_combobox['values'] = products

def get_produit(category):
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql = """SELECT p.Nom_product
            FROM product p
            INNER JOIN category c ON p.Nom_category = c.Nom_category
            WHERE c.Nom_category = %s"""
    cursor.execute(sql, (category,))
    products = [row[0] for row in cursor.fetchall()]
    return products

def values_prix(event):
    produit = produit_combobox.get()
    connection=fileRE.connectiondb()
    cursor = connection.cursor()
    sql = "SELECT stock FROM product WHERE Nom_product = %s"
    cursor.execute(sql, (produit,))
    stock_available = cursor.fetchone()
    if produit:
        prix = get_prix(produit)
        prix_combobox.config(state=NORMAL)
        prix_combobox.config(state='readonly')
        quantite_combobox.config(state=NORMAL)
        prix_combobox['values'] = prix
        prix_combobox.current(0)
        if stock_available: 
            stock_value = stock_available[0] 
            label_stock.config(text=f"Stock: {stock_value}") 
        else:
            messagebox.showerror('STOCK', "Ce produit est épuisé")

def get_prix(produit):
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql = "SELECT * FROM product WHERE Nom_product = %s"
    cursor.execute(sql, (produit,))
    prix = [row[4] for row in cursor.fetchall()]
    return prix


def values_stock():
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





def valider_nombre(valeur):
    try:
      number = float(valeur) 
    except ValueError:
      messagebox.showerror("Invalid Input", "stock  est un valid number.")
total_P1=[]
def ajouter_info_facture():
    #RECUPERER LES VALEURS DE COMBOBOX
    DATE = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ID_C =ID_entry.get()
    email_C = email_entry.get()
    Nom_C = nom_entry.get()
    category_P=category_combobox.get()
    produit_P=produit_combobox.get()
    prix = int(prix_combobox.get())
    valider_nombre(quantite_combobox.get())
    total_P=prix * int(quantite_combobox.get())
    #CONFIGURE LES VALEURS DANS FACTURE DATE ET CLIENT ET NUMERO FACTURE
    date.config(text=DATE)
    client.config(text=Nom_C)
    
    #configure STATE DE TEXTAREA EN NORMAL POUR AJOUTER LES DONNES
    textarea.config(stat=NORMAL)

    valider_stock(produit_P,prix,total_P) 
    quantite_combobox.delete(0,END)
    prix_combobox.set("")
    produit_combobox.set("")
    category_combobox.set("")
    values_stock()
    label_stock.config(text="Stock:") 
    
    textarea.config(stat=DISABLED)

def valider_stock(produit_P,prix,total_P):
    quantite = int(quantite_combobox.get())
    connection=fileRE.connectiondb()
    cursor = connection.cursor()
    sql ="SELECT stock FROM product WHERE Nom_product = %s"
    cursor.execute(sql, (produit_P,))
    stock_available = cursor.fetchone()[0] 
    donnes = f"{produit_P}                     {quantite_combobox.get()}                        {prix}Dh"
    nouveau_stock=stock_available - quantite
    if quantite > stock_available:
        messagebox.showerror('ERROR !!', ' le rester de stock est:'+str({stock_available}))
    else:
        textarea.insert(END, donnes + "\n")
        total_P1.append(total_P)
        total.config(text=f"{sum(total_P1)}Dh")
        update_stock(nouveau_stock)
    

def delete_command():
    textarea.config(stat=NORMAL)
    current_text = textarea.get("1.0", END)  #RECUPERER LE TEXT
    if current_text:  #IF TEXT EXIST
        lines = current_text.splitlines()[:-1]  #SUPPRRIMER DERNIERE LINE 
        textarea.delete("1.0", END)  # Clear existing text
        textarea.insert(END, "\n".join(lines))
        total_P1.pop()
        total.config(text=f"{sum(total_P1)}Dh")
        
    else:
         messagebox.showerror('ERROR !!', ' no found  command')
    textarea.config(stat=DISABLED)

def vider_facture():
    textarea.config(stat=NORMAL)
    textarea.delete("1.0", END)
    textarea.config(stat=DISABLED)

def convertir_en_dictionnaire(texte):
  lignes_texte = texte.splitlines()
  lignes_texte = [ligne.strip() for ligne in lignes_texte if ligne]
  cles_dictionnaire = ["produit", "quantite", "prix"]
  donnees_facture = []
  for ligne in lignes_texte:
    elements_ligne = ligne.split()
    dictionnaire_ligne = {cle: element for cle, element in zip(cles_dictionnaire, elements_ligne)}
    dictionnaire_ligne["prix"] = float(dictionnaire_ligne["prix"][:-2])
    donnees_facture.append(dictionnaire_ligne)
  return donnees_facture

compteur =0
def generer_facture():
  compteur+=1
  numero_facture.config(text=f"{compteur}")
  contenu_texte = textarea.get(1.0, END)
  donnes_facture=convertir_en_dictionnaire(contenu_texte)
  with open("facture.json", "w") as fichier:
    json.dump(donnes_facture,fichier)
    ajouter_facture()
    messagebox.showinfo("Enregistrement", "Facture enregistrée avec succès !")
    textarea.config(stat=NORMAL)
    textarea.delete("1.0", END)
    textarea.config(stat=DISABLED)
    subprocess.Popen(["notepad.exe", "facture.json"])


def update_stock(nouveau_stock):
    produit=produit_combobox.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql1 = "UPDATE product SET stock =%s WHERE Nom_product =%s"
    cursor.execute(sql1, (nouveau_stock,produit,))
    connection.commit()
    
def ajouter_facture():
    total=sum(total_P1)
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql1 = f"INSERT INTO facture (total,id_employer) VALUES ({total},{id})"
    cursor.execute(sql1)
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

image_a=Image.open("images\Facture4.jpg")
resised=image_a.resize((680,420))
new = ImageTk.PhotoImage(resised)

label_facture=Label(facture,image=new,font=('yu gothic ui', 15, "bold") ,bg='white')
label_facture.place(x=0,y=0,width=690,height=410)

date=Label(facture,font=(8),bg='white')
date.place(x=60,y=-2)

client=Label(facture,font=(8) ,bg='white')
client.place(x=80,y=25)

numero_facture=Label(facture,text='0' ,font=(8),bg='white')
numero_facture.place(x=160,y=55)

total=Label(facture,text=f"" ,bg='#a4a4a4',fg='white',font=('yu gothic ui', 15, "bold"))
total.place(x=545,y=360)

facture_frame = ttk.Frame(facture, style='Facture.TFrame')
facture_frame.place(x=20, y=143, width=630, height=200)

textarea = Text(facture_frame,stat=DISABLED)
textarea.pack()

    # Define the style for the frame
facture_style = ttk.Style()
facture_style.configure('Facture.TFrame', background='white')


#------------------------------gestion des button---------------------------------
button=LabelFrame(Frame,text=' Gestion de facture',font=('yu gothic ui', 15, "bold") ,bg='white')
button.place(x=980,y=80,width=254,height=450)


add = Button(button, text="GENERER FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=generer_facture)
add.place(x=30, y=120, width=200, height=45)


update = Button(button, text="VIDER FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=vider_facture)
update.place(x=30, y=210, width=200, height=45)


delete = Button(button, text="LOGOUT  ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f')
delete.place(x=30, y=300, width=200, height=45)


















values_stock()
fileRE.combobox(category_combobox)
root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
fileRE.clock(lbheure)
root.mainloop()






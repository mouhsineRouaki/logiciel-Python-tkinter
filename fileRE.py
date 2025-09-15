from tkinter import messagebox
from tkinter import *
from PIL import ImageTk,Image
import mysql.connector
from tkinter import ttk
import time
import os

#---------------------------------gestion des button de login et retour------------------------------------------------------------
    
def pageLogin(root):
    root.destroy()
    import page_login

def inscription_page(root):
    root.destroy()
    import page_inscription

def pageAdmin(root):
    root.destroy()
    import gestion_admin

def pageCategory(root):
    root.destroy()
    import gestion_category

def pageProduit(root):
    root.destroy()
    import gestion_produit

def pageEmployer(root):
    root.destroy()
    import gestion_employer

def pageFacture(root):
    root.destroy()
    import gestion_facture

def logout(root):
    reponse = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if reponse == True:
        root.destroy()

#-------------------------------------fonction de time------------------------------------------------------------------------------
def clock(label):
    current_time = time.strftime("%H:%M:%S")
    label.config(text=current_time,fg='black', font=('yu gothic ui', 15, "bold"))
    label.after(1000, clock, label)
#-------------------------------connection a la base de donner:tkinter-------------------------------------------------
def connectiondb():
    try:
        connection = mysql.connector.connect(database="tkinter",user="root",password="",host="localhost")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None
    
# pour aficher les category dans combobox dans les pages(produit ,category)
def values_category(category_combobox): # pour reuperer les  category et aficher dans base de donner
    options=[]
    connection = connectiondb()
    cursor = connection.cursor()
    sql2="SELECT Nom_category FROM category "
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
        options.append(row[0])
        category_combobox["values"]=options

def afficher_product(treeview):
    connection = connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM product "
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
def AFFICHER_PRODUCT(combobox, treeview):
    val = combobox.get()
    connection = connectiondb()
    cursor = connection.cursor()
    sql = """SELECT p.Id_product, p.Nom_product, c.Nom_category, p.stock, p.prix,p.date
            FROM product p
            INNER JOIN category c ON p.Nom_category = c.Nom_category
            WHERE c.Nom_category = %s"""
    cursor.execute(sql, (val,))
    products = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for product in products:
        id = product[0]
        nom = product[1]
        category = product[2]
        stock = product[3]
        prix = product[4]
        date =product[5]
        treeview.insert("", END, values=(id, nom, category, stock, prix,date))
def iconbitmap(root):
    icon_img = Image.open("images/logo.png")
    resized_img = icon_img.resize((40, 40))
    tk_icon = ImageTk.PhotoImage(resized_img) 
    root.iconphoto(True, tk_icon)



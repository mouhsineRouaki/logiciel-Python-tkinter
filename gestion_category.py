from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import fileRE


def afficher_cat(treeview):# pour afficher le donner de table category dans un treeview
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM category ORDER BY Id_category"
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
            id = row[0]
            nom = row[1]
            desc = row[2]
            treeview.insert("", END, values=(id,nom,desc))

def ajouterCategory(entry1,entry2,treeview): #pour ajouter des donner dans treeview
    val1=entry1.get()
    val2=entry2.get()
    if val1==''and val2=='':
        messagebox.showerror('ERORR !!','please entre le nom de category et le description')
    elif val1=='':
        messagebox.showerror('ERORR !!','please entre le nom de category que tu dois Inserer')
    elif val2=='':
        messagebox.showerror('ERORR !!','please entre le description de category que tu dois inserer ')
    else:
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        sql1 = "INSERT INTO category (Id_category,Nom_category,description_cat) VALUES (NULL, %s, %s)"
        values1 = ( val1,val2 )
        cursor.execute(sql1, values1)
        connection.commit()
        treeview.delete(*treeview.get_children())
        afficher_cat(treeview)
        messagebox.showerror('GESTION DES ADMIN','INSERTION DES DONNES REUISSIR')


            
 
def modifierCategory(entry1,entry2,entry3,treeview): #pour modifier des donner dans treeview
    nom=entry1.get()
    description=entry2.get()
    id=entry3.get()
    if nom=='':
        messagebox.showerror('ERORR !!','please entre le nom de category que tu dois modifier ')
    elif description=='':
        messagebox.showerror('ERORR !!','please entre la modification que tu propose ')
    elif id=='':
        messagebox.showerror('ERORR !!','please entre la id ou nom de category que tu propose ')
    else:
        connection = fileRE.connectiondb()
        cursor = connection.cursor()
        sql1 = "UPDATE category SET description_cat = %s,Nom_category = %s WHERE Nom_category = %s or id_category=%s"
        values = ( description,nom,id,id )
        cursor.execute(sql1, values)
        connection.commit()
        treeview.delete(*treeview.get_children())
        afficher_cat(treeview)
        messagebox.showerror('GESTION DES ADMIN',' CATEGORY UPDATE AVEC SECCUFEL')
    
def supprimerCategory(entry1,treeview): # pour supprimer les donner dans un treeview
    val1=entry1.get()
    line = treeview.selection()
    values = treeview.item(line, 'values')  
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    if line:
        reponse = messagebox.askokcancel("Question", "Voulez-vous supprimer  cette command ?")
        if (reponse==True):
            id_category = values[0] 
            sql1 = "DELETE FROM category  WHERE  Id_category=%s"
            cursor.execute(sql1, (id_category,))
            for row in line:
                treeview.delete(row)
                messagebox.showerror('GESTION DES ADMIN',' CATEGORY ETAIT SUPPRIMER')
    elif val1=='' or line=='':
        messagebox.showerror('ERORR !!','please entre le nom de category ou selectioner line que tu dois suprimer ')
    else:
        reponse = messagebox.askokcancel("Question", "Voulez-vous supprimer  cette command ?")
        if (reponse==True):
            sql2 = "DELETE FROM category  WHERE Nom_category = %s or Id_category=%s"
            values = (val1,val1)
            cursor.execute(sql2, values)
            connection.commit()
            treeview.delete(*treeview.get_children())
            afficher_cat(treeview)
            messagebox.showerror('GESTION DES ADMIN',' CATEGORY ETAIT SUPPRIMER')

def chercherCategory(username,treeview): #pour chercher un category dans base de donnees et afficher dans un treeview
    val1=username.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM category WHERE Nom_category=%s or id_category=%s "
    cursor.execute(sql2,(val1,val1,))
    category=cursor.fetchall()
    if category :
        treeview.delete(*treeview.get_children())
        for row in category:
                id = row[0]
                nom = row[1]
                category = row[2]
                treeview.insert("", END, values=(id,nom,category))
                messagebox.showerror('GESTION DES CATEGORY','CATEGORY EXIST')
    else :
        messagebox.showerror('GESTION DES CATEGORY','NO FOUND CATEGORY ')
        treeview.delete(*treeview.get_children())
        afficher_cat(treeview)

root = Tk()
style = ttk.Style()
root.title("gestion des category")
root.geometry("920x620+200+30")
root.resizable(False, False)
x_offset = (1920 - root.winfo_width()) // 7
y_offset = (1000 - root.winfo_height()) // 12
chemin="images\\acceui1.jpg"
image_a=Image.open(chemin)
resised=image_a.resize((1900,800))
new = ImageTk.PhotoImage(resised)
label=Label(root,image=new,bg='red')
label.image = new 
label.pack()

heading = Label(root, text="GESTION DES CATEGORY", font=('yu gothic ui', 15, "bold"), fg='white',bg='#9a258f',bd=5,relief=FLAT)
heading.place(x=260, y=2, width=490, height=30)

date = Label(root, text="GESTION DES CATEGORY", font=( 15), fg='black',bd=5,relief=FLAT)
date.place(x=450, y=33)
fileRE.clock(date)

AJOUTER = Button(root, text="AJOUTER CAT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command= lambda :ajouterCategory(nom_category,description_category,tv))
AJOUTER.place(x=37, y=120, width=140, height=45)


MODIFIER = Button(root, text="MODIFIER CAT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command= lambda :modifierCategory(nom_category,description_category,comboboxSearch,tv))
MODIFIER.place(x=37, y=190, width=140, height=45)


SUPPRIMER = Button(root, text="DELETE CAT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command= lambda :supprimerCategory(comboboxSearch,tv))
SUPPRIMER.place(x=37, y=260, width=140, height=45)

comboboxSearch = ttk.Combobox(root, font=(6),width=19)
comboboxSearch.place(x=36, y=330, width=140, height=45)

search = Button(root, text="SEARCH ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:chercherCategory(comboboxSearch,tv))
search.place(x=36, y=400, width=140, height=45)

EXIT = Button(root, text=" EXIT ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command= lambda :fileRE.pageAdmin(root))
EXIT.place(x=37, y=470, width=140, height=45)

LOGOUT = Button(root, text="LOG OUT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command= lambda :fileRE.pageLogin(root))
LOGOUT.place(x=38, y=540, width=140, height=45)

contenu=Frame(root,bg='white')
contenu.place(x=200,y=120,width=717,height=466)

label=Label(contenu,image=new,bg='red')
label.pack()

NomC = Label(root, text='Nom de Category :', fg='black')
NomC.place(x=250, y=150)

nom_category=Entry()
nom_category.place(x=359,y=150)

desC = Label(root, text='Description de  Category :', fg='black')
desC.place(x=550, y=150)

description_category=Entry()
description_category.place(x=690,y=150)

Label(contenu,text='INFORMATIONS CATEGORY', font=('yu gothic ui', 15, "bold")).place(x=250,y=70)
area=('CategoryCode','CategoryNom','descriptionCat')
ac=('all','n','e')
tv=ttk.Treeview(contenu,columns=ac,show='headings',height=100)
style.theme_use('clam')
for i in range(3):
    tv.column(ac[i],width=240,anchor='center')
    tv.heading(ac[i],text=area[i])
    tv.place(x=0,y=120)
afficher_cat(tv)

scrollbar_verticale = ttk.Scrollbar(contenu, orient="vertical", command=tv.yview)
tv.configure(yscroll=scrollbar_verticale.set)
    
scrollbar_verticale.place(relx=0, rely=0, relheight=0.95)
tv.place(relx=0.03, rely=0.02, relwidth=0.97, relheight=0.70)

root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()

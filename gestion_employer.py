from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import fileRE


def afficher_employer( ):
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM inscription ORDER BY id_employer"
    cursor.execute(sql2)
    employers=cursor.fetchall()
    for employer in employers:
            EmployerID = employer[0]
            EmployerEmail = employer[1]
            EmployerNom = employer[2]
            EmployerPassword = employer[3]
            EmployerDestination = employer[4]
            date = employer[5]
            treeview.insert("", END, values=(EmployerID,EmployerEmail,EmployerNom,EmployerPassword,EmployerDestination,date))
    return EmployerEmail,EmployerNom

def ajouter_employer():
    val1=comboboxEmail.get()
    val2=comboboxEmployer.get()
    val3=comboboxPassword.get()
    val4=comboboxDestination.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    EmployerEmail,EmployerNom=afficher_employer()
    if val1=='' and val2=='' and val3==''and val4=='':
       messagebox.showerror('inscription','please!  : Remplir les champ est obligatoire')
    elif val1 == '':
        messagebox.showerror('inscription','please!  : remplir le email employer')
    elif val2 == '':
        messagebox.showerror('inscription','please!  : Remplir le username employer')
    elif val3 == '':
        messagebox.showerror('inscription','please!  : Remplir le password employer')
    elif val4 ==0:
        messagebox.showerror('inscription','please!  : Selectionner  le type employer')
    elif connection:
        query = "SELECT 1 FROM inscription WHERE Email = %s or username=%s"
        cursor.execute(query, (val1,val2,))
        exists = cursor.fetchone()
        if exists:
            messagebox.showerror('GESTION DES EMPLOYER','email ou username deja existe \n changer le nom ou email et ajouter')
        else:
            sql = "INSERT INTO inscription ( Email, username, password, genre) VALUES (%s, %s, %s, %s)"
            values = ( val1, val2,val3,val4 )
            cursor.execute(sql, values)
            connection.commit()
            connection.close()
            treeview.delete(*treeview.get_children())
            afficher_employer()
            messagebox.showerror('GESTION DES EMPLOYER','EMPLOYER AJOUTER AVEC SUCCESS')
            treeview.delete(*treeview.get_children())
            afficher_employer() 

def remplirCombobox(event):
    line = treeview.focus()
    values = treeview.item(line, 'values')
    if line:
        comboboxChercher.set(values[0])
        comboboxEmail.set(values[1])
        comboboxEmployer.set(values[2])
        comboboxPassword.set(values[3])
        comboboxDestination.set(values[4])

def viderCombobox():
    comboboxChercher.set("")
    comboboxEmail.set("")
    comboboxEmployer.set("")
    comboboxPassword.set("")
    comboboxDestination.set("")

def combobox_employer():
    options=[]
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT username FROM inscription"
    cursor.execute(sql2)
    category=cursor.fetchall()
    for row in category:
        options.append(row[0])
        comboboxChercher["values"]=options


def modifier_employer():
    val1=comboboxEmail.get()
    val2=comboboxEmployer.get()
    val3=comboboxPassword.get()
    val4=comboboxDestination.get()
    val5=comboboxChercher.get()
    if val1=='' or val2=='' or val3=='' or val4=='' or val5=='' :
        messagebox.showerror('ERORR !!','please remplir tout les champs pour  modifier ')
    else:
            connection = fileRE.connectiondb()
            cursor = connection.cursor()
            sql1 = "UPDATE inscription SET username = %s,email=%s,password = %s,genre=%s WHERE username = %s or id_employer=%s"
            values = (val2,val1,val3,val4,val5 ,val5)
            cursor.execute(sql1, values)
            connection.commit()
            if cursor.rowcount>0:
                treeview.delete(*treeview.get_children())
                afficher_employer()
                messagebox.showerror('GESTION DES ADMIN',' EMPLOYER UPDATE AVEC SECCUFEL')
            else:
                messagebox.showerror('GESTION DES ADMIN',' EMPLOYER NOT FOUND')


def delete_employer():
    valeur=comboboxChercher.get()
    line = treeview.selection()
    values = treeview.item(line, 'values')  
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    if line:
        reponse = messagebox.askokcancel("Question", "Voulez-vous supprimer  cette command ?")
        if (reponse==True):
            id_produit = values[0] 
            sql1 = "DELETE FROM inscription  WHERE  id_employer=%s"
            cursor.execute(sql1, (id_produit,))
            connection.commit()
            messagebox.showerror('GESTION DES EMPLOYER',' EMPLOYER DELETE AVEC SECCUFEL')
            treeview.delete(*treeview.get_children())
            afficher_employer()
    elif valeur:
        sql1 = "DELETE FROM inscription  WHERE  username=%s or id_employer=%s"
        values = (valeur,valeur)
        cursor.execute(sql1, values)
        if cursor.execute(sql1, values)==True:
            treeview.delete(*treeview.get_children())
            afficher_employer()
            messagebox.showerror('GESTION DES EMPLOYER','EMPLOYER DELETE AVEC SECCUFEL')
        else:
            messagebox.showerror('GESTION DES EMPLOYER','NO FOUND EMPLOYER ')

def chercherEmployer():
    val1=comboboxChercher.get()
    connection = fileRE.connectiondb()
    cursor = connection.cursor()
    sql2="SELECT * FROM inscription WHERE username=%s or id_employer=%s "
    cursor.execute(sql2,(val1,val1,))
    employers=cursor.fetchall()
    if employers :
        treeview.delete(*treeview.get_children())
        for employer in employers:
                id = employer[0]
                nom = employer[1]
                category = employer[2]
                stock = employer[3]
                prix = employer[4]
                date = employer[5]
                treeview.insert("", END, values=(id,nom,category,stock,prix,date))
    else :
        messagebox.showerror('GESTION DES EMPLOYER','NO FOUND EMPLOYER ')
        treeview.delete(*treeview.get_children())
        afficher_employer(treeview)


root = Tk()
root.title("GESTION DES EMPLOYER")
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
txt = "GESTION EMPLOYER"
titre = Label(root, text=txt, font=('yu gothic ui', 15, "bold"),bg='#9a258f', fg='white',bd=5,relief=FLAT)
titre.place(x=250, y=2, width=470, height=30)


ajouterButton = Button(root, text="ADD EMPLOYER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=ajouter_employer)
ajouterButton.place(x=37, y=120, width=140, height=45)


modifierButton = Button(root, text="UPDATE EMPLOYER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda :modifier_employer())
modifierButton.place(x=37, y=190, width=140, height=45)


supprimerButton = Button(root, text="DELETE EMPLOYER  ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:delete_employer())
supprimerButton.place(x=36, y=260, width=140, height=45)

comboboxChercher = ttk.Combobox(root, font=(6),width=19)
comboboxChercher.place(x=36, y=330, width=140, height=45)

chercherButton = Button(root, text="SEARCH ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda:chercherEmployer())
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

afficherButton = Button(contenu, text="AFFICHER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :afficher_employer())
afficherButton.place(x=500, y=50, width=140, height=45)

viderButton = Button(contenu, text="VIDER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :viderCombobox())
viderButton.place(x=500, y=100, width=140, height=45)

headingLabel=Label(contenu,text='GESTION EMPLOYER',font=('Areal',19),bg='white',relief=FLAT)
headingLabel.grid(row=0,column=1,padx=10,pady=10)

categoryLabel=Label(contenu,text=' nom employer :',font=('Areal',10),bg='white')
categoryLabel.grid(row=1,column=0,sticky='w',padx=20)

comboboxEmployer = ttk.Combobox(contenu, font=(6),width=19)
comboboxEmployer.grid(row=2,column=0,sticky='w',padx=30)


EmailLabel=Label(contenu,text='Email :',font=('Areal',10),bg='white')
EmailLabel.grid(row=1,column=1,sticky='w',padx=5)

comboboxEmail = ttk.Combobox(contenu, font=(6),width=19)
comboboxEmail.grid(row=2,column=1,sticky='w',padx=5)

options =['Admin','User']
destinationLabel=Label(contenu,text='  destination :',font=('Areal',10),bg='white')
destinationLabel.grid(row=3,column=0,sticky='w',padx=20)

comboboxDestination = ttk.Combobox(contenu,values=options, font=(6),width=19,state='readonly')
comboboxDestination.grid(row=4,column=0,sticky='w',padx=30)

passwordLabel=Label(contenu,text='password :',font=('Areal',10),bg='white')
passwordLabel.grid(row=3,column=1,sticky='w',padx=5)

comboboxPassword = ttk.Combobox(contenu, font=(6),width=19)
comboboxPassword.grid(row=4,column=1,sticky='w',padx=5)


area=('EmployerID','EmployerEmail','EmployerNom','password','destination','date')
treeview=ttk.Treeview(contenu,columns=area,show='headings',height=100)
for i in range(6):
    treeview.column(area[i],width=119,anchor='center')
    treeview.heading(area[i],text=area[i])
    treeview.place(x=0,y=150)
    treeview.bind('<<TreeviewSelect>>', remplirCombobox)

scrollbar_verticale = ttk.Scrollbar(contenu, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar_verticale.set)
    
scrollbar_verticale.place(relx=0, rely=0, relheight=0.95)
treeview.place(relx=0.02, rely=0.02, relwidth=0.97, relheight=0.70)

afficher_employer()
combobox_employer()
root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))


fileRE.iconbitmap(root)
root.mainloop()
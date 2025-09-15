from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector
import fileRE
import json
root=Tk()

RB=IntVar()

root.geometry("789x516")

x = (1920 - root.winfo_width()) // 7
y = (1080 - root.winfo_height()) // 12
root.geometry(f"+{x}+{y}") 

root.title('page de inscription')

background=ImageTk.PhotoImage(file='images/background.jpg')

root.resizable(False,False)

label=Label(root,image=background,bg='pink')
label.grid()

#-------------------------------------gestion de login-----------------------------------------------------------------
def verifier(email, password):
  global utilisateur
  try:
    connection =fileRE.connectiondb()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inscription WHERE Email = %s AND password = %s", (email, password))
    utilisateur = cursor.fetchone()
    cursor.close()
    connection.close()
    return utilisateur is not None
  except mysql.connector.Error as error:
    print("Erreur de connexion:", error)
    return False


def valider(emailEntry,passwordEtry,check,fenetre):
    global line 
    line=[]
    email = emailEntry.get()
    password = passwordEtry.get()
    checkB=check.get()
    connection = fileRE.connectiondb()
    if email=='' and password=='' and checkB==0:
        messagebox.showerror('login','please!  : entrer le nom et le mot de pass')
    elif  email=='':
         messagebox.showerror('login','please!  : Remplir votre Email')
    elif password=='' :
        messagebox.showerror("login","please! :Remplir votre password")
    elif checkB==0:
        messagebox.showerror('login','please!  : READ THE CONDITIIONS AND CONFIRMER')
    elif connection:
        if verifier(email, password):
            save(utilisateur[0],utilisateur[1],utilisateur[2])
            if utilisateur[4] == "Admin":
                fenetre.destroy()
                import gestion_admin
            else :
                fenetre.destroy()
                import gestion_client
        else:
            messagebox.showerror("verification","VOTRE PASSWORD AND EMAIL INCORRECT !")


def login_page(root):
    root.destroy()
    import page_inscription

def save(id,email,username):
    login_data = {"id": id, "email": email, "username": username}
    json_data = json.dumps(login_data)
    with open("donnes.json", "w") as f:
        f.write(json_data)

frame=Frame(root,bg='white')
frame.place(x=454,y=40)

heading=Label(frame,text='LOG IN ACCOUNT',font=('Areal',19),bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)

email=Label(frame,text='Email :',font=('Areal',10),bg='white',fg='firebrick1')
email.grid(row=1,column=0,padx=40,sticky='w')

emailEntry=Entry(frame,width=35,bg='pink',fg='black')
emailEntry.grid(row=2,column=0,sticky='w',padx=40,pady=10)

password=Label(frame,text='Password :',font=('Areal',10),bg='white',fg='firebrick1')
password.grid(row=5,column=0,padx=40,sticky='w')

passwordEntry=Entry(frame,width=35,bg='pink',fg='black',show='*')
passwordEntry.grid(row=6,column=0,sticky='w',padx=40,pady=10)


case2 = Checkbutton (frame,variable=RB,text='I agree to the terms & conditions',fg='red',bg='white',activebackground='pink',activeforeground='blue')
case2.grid(column =0 , row =11 ,pady=10)

btn=Button(frame,text='LOGIN',font=(16),bg='pink',fg='black',activebackground='pink',activeforeground='red',width=20,command =lambda: valider(emailEntry,passwordEntry,RB,root))
btn.grid(column =0 , row =12,sticky='w',padx=50,pady=10)

labelLogin=Label(frame,text='I dont have an account :',font=('Areal',10),bg='white',fg='firebrick1')
labelLogin.grid(row=15,column=0,padx=40,sticky='w')

btn2=Button(frame,text='Inscription',font=(16),bg='pink',fg='black',activebackground='pink',activeforeground='red',width=20,command=lambda: fileRE.inscription_page(root))
btn2.grid(column =0 , row =17,sticky='w',padx=50)

root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()

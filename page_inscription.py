from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import fileRE
import re

def insertion(email, username, password,confirm,genre,condition,root):
    value_email=email.get()
    value_username=username.get()
    value_password=password.get()
    value_confirm_password=confirm.get()
    value_genre=genre.get()
    value_condition=condition.get()
    connection = fileRE.connectiondb()
    if value_email=='' and value_username=='' and value_password==''and value_confirm_password==''and value_genre=='':
       messagebox.showerror('inscription','please!  : Remplir les champ est obligatoire')
    elif value_email == '':
        messagebox.showerror('inscription','please!  : remplir votre email')
    elif value_username == '':
        messagebox.showerror('inscription','please!  : Remplir votre username')
    elif value_password == '':
        messagebox.showerror('inscription','please!  : Remplir votre password')
    elif value_confirm_password == '':
        messagebox.showerror('inscription','please!  : Remplir votre Confirm Password')
    elif value_confirm_password!=value_password:
        messagebox.showerror('inscription','please!  : your confirm password is incorrect')
    elif value_genre ==0:
        messagebox.showerror('inscription','please!  : Selectionner  votre type')
    elif value_condition ==0:
            messagebox.showerror('inscription','please!  :  you have agree to the terms and condition?')
    elif connection:
        if (value_genre==2):
            value_genre='User' 
        try :
            cursor = connection.cursor()
            sql = "INSERT INTO inscription ( Email, username, password, genre) VALUES (%s, %s, %s, %s)"
            values = ( email.get(), username.get(), password.get(),value_genre )
            cursor.execute(sql, values)
            connection.commit()
            connection.close()
            messagebox.showerror('connection reussie','insertion reussie')
            fileRE.pageLogin(root)
        except Exception:
            messagebox.showerror('connection echec','cette email deja exist')
def validate_email(e):
    regex = '^[a-z0-9]+?[a-z0-9]+[@]+[.]{2,3}$'
    return re.search(regex, e)

def show_error(event):
    if not validate_email(emailEntry.get()):
        messagebox.showerror('email','remplir email avec correct format')


root=Tk()

RB=IntVar()

CB=IntVar()

root.geometry("789x516")

x_offset = (1920 - root.winfo_width()) // 7
y_offset = (1080 - root.winfo_height()) // 12

root.title('page de inscription')

root.geometry(f"+{x_offset}+{y_offset}")

background=ImageTk.PhotoImage(file='images/background.jpg')

root.resizable(False,False)

label=Label(root,image=background,bg='pink')
label.grid()

frame=Frame(root,bg='white')
frame.place(x=454,y=40)

heading=Label(frame,text='CREATE AN ACCOUNT',font=('yu gothic ui', 15, "bold"),bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)

email=Label(frame,text='Email :',font=('yu gothic ui', 15, "bold"),bg='white',fg='firebrick1')
email.grid(row=1,column=0,padx=40,sticky='w')

emailEntry=Entry(frame,width=35,bg='pink',fg='black',)
emailEntry.grid(row=2,column=0,sticky='w',padx=40)

username=Label(frame,text='Username :',font=('yu gothic ui', 15, "bold"),bg='white',fg='firebrick1')
username.grid(row=3,column=0,padx=40,sticky='w')

usernameEntry=Entry(frame,width=35,bg='pink',fg='black')
usernameEntry.grid(row=4,column=0,sticky='w',padx=40)

password=Label(frame,text='Password :',font=('yu gothic ui', 15, "bold"),bg='white',fg='firebrick1')
password.grid(row=5,column=0,padx=40,sticky='w')

passwordEntry=Entry(frame,width=35,bg='pink',fg='black',show='*')
passwordEntry.grid(row=6,column=0,sticky='w',padx=40)

confirm=Label(frame,text='Confirm Password  :',font=('yu gothic ui', 15, "bold"),bg='white',fg='firebrick1',)
confirm.grid(row=7,column=0,padx=40,sticky='w')

confirmEntry=Entry(frame,width=35,bg='pink',fg='black',show='*')
confirmEntry.grid(row=8,column=0,sticky='w',padx=40)


case2 = Radiobutton (frame,text = "User",variable = RB, value =2,fg='red',bg='white')
case2.grid(column =0 , row =10 )

case2 = Checkbutton (frame,text='I agree to the termss',variable=CB,fg='red',bg='white',activebackground='pink',activeforeground='blue')
case2.grid(column =0 , row =11 )

btn=Button(frame,text='inscription',font=(16),bg='pink',fg='black',activebackground='pink',activeforeground='red',width=20,command =lambda: insertion(emailEntry,usernameEntry,passwordEntry,confirmEntry,RB,CB,root))

btn.grid(column =0 , row =12,sticky='w',padx=50)

labelLogin=Label(frame,text='I have an account :',font=('Areal',10),bg='white',fg='firebrick1')
labelLogin.grid(row=15,column=0,padx=40,sticky='w')

btn2=Button(frame,text='Log In',font=(16),bg='pink',fg='black',activebackground='pink',activeforeground='red',width=20,command =lambda: fileRE.pageLogin(root))

btn2.grid(column =0 , row =17,sticky='w',padx=50)


root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()

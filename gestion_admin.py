from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import fileRE
root = Tk()
root.title("gestion des admin")
root.geometry("920x620+200+30")
root.resizable(False, False)
x_offset = (1920 - root.winfo_width()) // 7
y_offset = (1000 - root.winfo_height()) // 12
image_a=Image.open("images\\acceui.jpg")
resised=image_a.resize((1900,800))
new = ImageTk.PhotoImage(resised)
label=Label(root,image=new,bg='red')
label.image = new 
label.pack()

style = ttk.Style()
style.theme_use('alt')
txt = "SYSTEME DE GESTION DU SEPERMARCHE"
heading = Label(root, text=txt, font=('yu gothic ui', 15, "bold"), fg='black',bd=5,relief=FLAT)
heading.place(x=260, y=2, width=490, height=30)

category_btn = Button(root, text="GESTION CATEGORY", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :fileRE.pageCategory(root))
category_btn.place(x=37, y=120, width=150, height=45)

produit_btn = Button(root, text="GESTION PRODUCT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :fileRE.pageProduit(root))
produit_btn.place(x=37, y=190, width=150, height=45)

employer_btn = Button(root, text="GESTION USER  ", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda :fileRE.pageEmployer(root))
employer_btn.place(x=36, y=260, width=150, height=45)

facture_btn = Button(root, text="GESTION FACTURE", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f',bd=0,border=5 , activebackground='#9a258f',command=lambda :fileRE.pageFacture(root))
facture_btn.place(x=36, y=330, width=150, height=45)                


exit_btn = Button(root, text="LOG OUT", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 , activebackground='#9a258f',command=lambda:fileRE.pageAdmin(root))
exit_btn.place(x=38, y=540, width=140, height=45)

contenu=Frame(root,bg='white')
contenu.place(x=200,y=120,width=717,height=466)

label=Label(contenu,image=new,bg='red')
label.pack()

heading_frame = Label(root, text='CATEGORY PRODUCT :', font=('yu gothic ui', 15, "bold"), fg='black')
heading_frame.place(x=250, y=150)

options = []

combobox = ttk.Combobox(root, values=options, font=('yu gothic ui', 15, "bold"))
combobox.current()  
combobox.place(x=470,y=150)

add_btn = Button(root, text="AFFICHER", cursor='hand2', font=('yu gothic ui', 11, "bold"),fg="white", bg='#9a258f', bd=0,border=5 ,activebackground='#9a258f',command=lambda :fileRE.AFFICHER_PRODUCT(combobox, treeview))
add_btn.place(x=740, y=144, width=140, height=45)

Label(contenu,text='TOUS LES CATEGORY', font=('yu gothic ui', 15, "bold")).place(x=250,y=70)
area=('ProductID','ProductNom','Category','Stock ','Price','date')
treeview=ttk.Treeview(contenu,columns=area,show='headings',height=100)
for i in range(6):
    treeview.column(area[i],width=117,anchor='center')
    treeview.heading(area[i],text=area[i])
    treeview.place(x=0,y=120)

scrollbar_verticale = ttk.Scrollbar(contenu, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar_verticale.set)
    
scrollbar_verticale.place(relx=0, rely=0, relheight=0.95)
treeview.place(relx=0.02, rely=0.02, relwidth=0.97, relheight=0.70)


date = Label(root, text=txt, font=( 15), fg='black',bd=5,relief=FLAT)
date.place(x=450, y=33)


#fileRE.clock(date)
fileRE.values_category(combobox)
fileRE.afficher_product(treeview)
root.protocol("WM_DELETE_WINDOW",lambda :fileRE.logout(root))
fileRE.iconbitmap(root)
root.mainloop()

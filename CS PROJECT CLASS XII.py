#class XII  cs project
from customtkinter import * #install it using pip install customtkinter
import tkinter.messagebox as tmsg
import mysql.connector #you need to install it using py -m pip install sql-connector
import random
import string
import smtplib
from email.message import EmailMessage
from PIL import Image
import os
from dotenv import load_dotenv


set_appearance_mode("dark")
set_default_color_theme("blue")
APP_BG = "#151824"
CARD_BG = "#24354f"
BUTTON_BG = "#2e7bb3"
BUTTON_HOVER = "#1f6aa5"
LABEL_TEXT = "#f0f5ff"

# Load variables from the secret .env file
load_dotenv()

# Secure connection using environment variables
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "passdb")
)
my = mydb.cursor()

r=True
password=''
def widgetdestroy(a):
    a.destroy()

#to open the login screen
def login():
    root=CTk() 
    root.configure(fg_color=APP_BG)
    global password
    password=''
        
    #to close login screen and open the account of the person and show all the stored passwords
    def passscreen(uid):
        # to close the password screen and open the login screen for switching accounts 
        def switch():
            widgetdestroy(root2)
            global r
            r=True
            login()

        # to close the password screen and open a screen for generating a random password and 
        # store the random password along with username and website name given by user
        def ranpass():  
            widgetdestroy(root2)
            root3=CTk()
            root3.configure(fg_color=APP_BG)

            # to generate a random password and enter the data into database and 
            # close current screen and reopen the screen with all the stored password
            def generate(): 
                all = string.ascii_letters + string.digits + string.punctuation
                password = "".join(random.sample(all,10))
                my.execute('''INSERT INTO passwords (uid,website,username,password) VALUES(%s,'%s','%s','%s')'''%(uid,gwebentry.get(),guserentry.get(),password))
                mydb.commit()
                gwebvar.set('')
                guservar.set('')
                tmsg.showinfo('',f'your random generated \npassword is {password}')

            root3.maxsize(500,260)
            root3.minsize(500,260)
            root3.title('PASSWORD MANAGER')
            l1=CTkLabel(root3,text='WELCOME TO PASSWORD MANAGER\n',font=('comicsans',20,'bold','underline'),padx=60,pady=20)
            l1.grid(row=0,column=0,columnspan=2)

            gweblabel=CTkLabel(root3,text='NAME OF WEBSITE :',padx=40,pady=20,font=('comicsans',20,'bold'))
            guserlabel=CTkLabel(root3,text='USERNAME :',padx=40,pady=20,font=('comicsans',20,'bold'))

            gweblabel.grid(row=1,column=0)
            guserlabel.grid(row=2,column=0)

            gwebvar=StringVar()
            guservar=StringVar()

            gwebentry=CTkEntry(root3,textvariable=gwebvar)
            guserentry=CTkEntry(root3,textvariable=guservar)

            gwebentry.grid(row=1,column=1)
            guserentry.grid(row=2,column=1)

            #button to call generate functions to create random password and store it
            gsubmit=CTkButton(root3,text='GENERATE',command=generate)

            gsubmit.grid(row=3,column=1)
            #button to go back to password screen
            gbackbutton=CTkButton(root3,text='   BACK   ',command=lambda:[widgetdestroy(root3),passscreen(uid)])

            gbackbutton.grid(row=4,column=1)

            root3.mainloop()

        #to close the password screen and open the screen for storing a password,username and website name given by user
        def passinput():  

            widgetdestroy(root2)
            global password
            password=''
            root4=CTk()
            root4.configure(fg_color=APP_BG)

            # to enter the details given by user into database,close the current screen and reopen the password screen
            def store(): 
                global password
                my.execute("INSERT INTO passwords (uid,website,username,password) VALUES(%s,'%s','%s','%s')"%(uid,swebentry.get(),suserentry.get(),password))
                mydb.commit()
                swebvar.set('')
                suservar.set('')
                spassvar.set('')
                tmsg.showinfo('','your entry has been stored')

            root4.maxsize(550,270)
            root4.minsize(550,270)
            root4.title('PASSWORD MANAGER')

            l1=CTkLabel(root4,text='WELCOME TO PASSWORD MANAGER',font=('comicsans',20,'bold','underline'))

            l1.grid(row=0,column=0,columnspan=3)
            sweblabel=CTkLabel(root4,text='NAME OF WEBSITE :',padx=40,pady=20,font=('comicsans',15,'bold'))
            suserlabel=CTkLabel(root4,text='USERNAME :',padx=40,pady=20,font=('comicsans',15,'bold'))
            spasslabel=CTkLabel(root4,text='PASSWORD :',padx=40,pady=20,font=('comicsans',15,'bold'))

            sweblabel.grid(row=3,column=0)
            suserlabel.grid(row=1,column=0)
            spasslabel.grid(row=2,column=0)

            swebvar=StringVar()
            suservar=StringVar()
            spassvar=StringVar()

            swebentry=CTkEntry(root4,textvariable=swebvar)
            suserentry=CTkEntry(root4,textvariable=suservar)
            spassentry=CTkEntry(root4,textvariable=spassvar)

            swebentry.grid(row=3,column=1)
            suserentry.grid(row=1,column=1)
            spassentry.grid(row=2,column=1)

            #button to call store function to store the details given by user
            ssubmit=CTkButton(root4,text='SUBMIT',command=store)
            ssubmit.grid(row=4,column=1)

            #button to go back to password screen
            sbackbutton=CTkButton(root4,text='BACK',command=lambda:[widgetdestroy(root4),passscreen(uid)])
            sbackbutton.grid(row=5,column=1)

            #button to call the show function for showing password entered by user
            sshowbutton=CTkButton(root4,text='SHOW',command=lambda:show(spassentry,root4,sshowbutton,spassvar))
            sshowbutton.grid(row=2,column=2)

            #binding event to spassentry to call hide function to hide password as the user enters it
            spassentry.bind('<KeyRelease>',lambda event1:hide(event1,spassentry,spassvar))

            # binding event to spassentry to call backspace function when backspace key is pressed
            spassentry.bind('<BackSpace>',lambda event:backspace(event,spassentry))

            root4.mainloop()
        global r
        if r==True: #to make sure below code only executes when user logs into his/her 
                    #account and  not everytime when passcreen is called 
            widgetdestroy(root)
            r=False

        root2=CTk()
        root2.configure(fg_color=APP_BG)
        root2.maxsize(700,500)
        root2.minsize(700,500)
        root2.title('PASSWORD MANAGER')

        container2=CTkFrame(root2, fg_color=CARD_BG, corner_radius=25, border_width=2, border_color='#1f3761')
        container2.pack(padx=20,pady=20,fill='both',expand=True)

        frame=CTkScrollableFrame(container2,fg_color=CARD_BG,corner_radius=18)
        frame.pack(fill='both',expand=True,padx=10,pady=10)

        l2=CTkLabel(frame,text='WELCOME TO PASSWORD MANAGER\n',font=('comicsans',20,'bold','underline'),fg_color=CARD_BG,corner_radius=15,text_color=LABEL_TEXT,padx=200,pady=20)
        l2.grid(row=0,column=0,columnspan=3)

        weblabel=CTkLabel(frame,text='WEBSITE NAME ',font=('comicsans',20,'bold','underline'),text_color=LABEL_TEXT)
        userlabel=CTkLabel(frame,text='USERNAME',font=('comicsans',20,'bold','underline'))
        passlabel=CTkLabel(frame,text='PASSWORD',font=('comicsans',20,'bold','underline'))

        weblabel.grid(row=1,column=0,)
        userlabel.grid(row=1,column=1)
        passlabel.grid(row=1,column=2)

        my.execute("SELECT * FROM passwords where uid=%s"%(uid,))

        #to retrive all the stored passwords and show on screen
        length=0
        i=2
        for x in my: #to find total no of entries
            length+=1

        if length==0: #if there are no entries execute below code
            tmsg.showinfo('PASSWORD MANAGER',"NO PASSWORD STORED\nPRESS OK TO CONTINUE")

        else: #if there are some entries execute below code
            my.execute("SELECT * FROM passwords where uid=%s"%(uid,))
            for x in my: #to print all the stored passwords on password screen
                website=CTkLabel(frame,text=f'{x[1]}',font=('comicsans', 20 ),)
                username=CTkLabel(frame,text=f'{x[2]}',font=('comicsans', 20 ),)
                password=CTkLabel(frame,text=f'{x[3]}',font=('comicsans', 20 ),)

                website.grid(row=i,column=0)
                username.grid(row=i,column=1)
                password.grid(row=i,column=2)

                i+=1

        #button to call passinput function for opening the screen for storing passwords
        storepass=CTkButton(frame,text='STORE A PASSWORD',command=passinput)
        storepass.grid(row=i,column=0,columnspan=3)

        #button to call ranpass function to open screen for creating random passwords
        randpass=CTkButton(frame,text='GENERATE RANDOM PASSWORD',command=ranpass)
        randpass.grid(row=i+1,column=0,columnspan=3)

        #button to call switch account function for switching accounts
        switchacc=CTkButton(frame,text='SWITCH ACCOUNT',command=switch)
        switchacc.grid(row=i+2,column=0,columnspan=3)

        root2.mainloop()

    #to verify otp
    def otp_verification(originalotp,givenotp,uid,root_name):

        if ( originalotp == givenotp ) :
            widgetdestroy(root_name)
            passscreen(uid)
        else :
            tmsg.showinfo('error',"input otp is wrong !!!!")

    # to send otp 
    def send_otp(uid,receiver_email):

        # Generate a secure 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Set up the email message structure
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {otp}")
        msg['Subject'] = 'Your Login OTP'
        
        # Safely fetch your email from environment variables
        sender_email = os.getenv("EMAIL_USER")
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Connect to Gmail's secure SMTP server and send the mail
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # Safely login using the App Password from your .env file
            server.login(sender_email, os.getenv("EMAIL_PASS"))
            server.send_message(msg)
            server.quit()
        except Exception as e:
            tmsg.showerror('Email Error', f"Failed to send OTP. Please check your network connection.\nError: {e}")
            return

        root5=CTk()
        root5.configure(fg_color=APP_BG)

        root5.maxsize(270,150)
        root5.minsize(270,150)
        root5.title("OTP VERIFICATION")
        root5.grid_rowconfigure(0, weight=1)
        root5.grid_columnconfigure(0, weight=1)

        main_frame5 = CTkFrame(root5, fg_color=CARD_BG, corner_radius=20, border_width=2, border_color='#1f3761')
        main_frame5.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        main_frame5.grid_columnconfigure(1, weight=1)

        title=CTkLabel(main_frame5,text='OTP VERIFICATION',font=('comicsans' ,16, 'bold'),text_color=LABEL_TEXT)
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,5))
        otplabel=CTkLabel(main_frame5,text='Enter OTP :',font=('comcisans',15,'bold'),padx=10,pady=5,fg_color='transparent',text_color=LABEL_TEXT)
        otplabel.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        otpvar=StringVar()
        otpentry=CTkEntry(main_frame5,textvariable=otpvar,width=140)
        otpentry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        otpsub_button=CTkButton(main_frame5,text='SUBMIT',command=lambda:otp_verification(otp,otpentry.get(),uid,root5),fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=220)
        otpsub_button.grid(row=2, column=0, columnspan=2, padx=15, pady=(5,10), sticky='ew')
        
        root5.mainloop()

    #to verify the data given by the user on login screen and proceed accordingly
    def dataverification():

        my.execute("SELECT count(*) FROM users WHERE username='%s'"%(userentry.get(),))
        n=my.fetchone()

        if n[0]==0: #to check if username exists in database or not if not execute below code
            uservar.set('')
            passvar.set('')
            global password
            password=''
            tmsg.showinfo('error','please create an account first')

        else: # if the username entered does exist in databse execute below code 
            my.execute("SELECT * FROM users WHERE username='%s'"%(userentry.get(),))
            data=my.fetchone()

            if data[2]==password: #to check if entered password is correct,if  correct execute below codde
                uid=data[0]
                email=data[3]

                send_otp(uid,email)

                # passscreen(uid)

            else:  #if the entered password is wrong execute below code
                passvar.set('')
                password=''
                tmsg.showinfo('error','the entered password is wrong try again')

    #to close the login screen and open the create account screen
    def cacc():

        widgetdestroy(root)
        global password
        password=''
        root1=CTk()
        root1.configure(fg_color=APP_BG)
        root1.maxsize(510,260)
        root1.minsize(510,260)
        root1.geometry('510x260')
        root1.title('PASSWORD MANAGER')

        main_frame1 = CTkFrame(root1, fg_color=CARD_BG, corner_radius=25, border_width=2, border_color='#1f3761')
        main_frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        root1.grid_rowconfigure(0, weight=1)
        root1.grid_columnconfigure(0, weight=1)

        l2=CTkLabel(main_frame1,text='WELCOME TO PASSWORD MANAGER',font=('comicsans',20,'bold','underline'),fg_color='#19203a',corner_radius=15,text_color=LABEL_TEXT)
        l2.grid(row=0, column=0, columnspan=3, padx=20, pady=(10,10), sticky='ew')

        #to create the account of person in database if details given are not present already
        def dataentry():

            my.execute("SELECT count(*) FROM users WHERE username='%s'"%(cuservar.get(),))
            n=my.fetchone()

            if n[0]>0:      #to check if username entered by user is already present execute below code if present 
                tmsg.showinfo('error',"USERNAME ALREADY PRESENT TRY TO USE ANOTHER ONE")
                cuservar.set('')
                cpassvar.set('')
                global password
                password=''

            else:         #to execute the below code if username not present and create account of person in database 
                my.execute("INSERT INTO users (username,password,email) VALUES(%s,%s,%s)",(cuservar.get(),password,cemailvar.get()))
                mydb.commit()
                tmsg.showinfo('','ACCOUNT CREATED \n TRY TO LOGIN NOW')
                cuservar.set('')
                cpassvar.set('')
                cemailvar.set('')

        cuserlabel=CTkLabel(main_frame1,text='CREATE USERNAME :',padx=20,pady=10,font=('comicsans',15,'bold'),fg_color='transparent',text_color=LABEL_TEXT)
        cpasslabel=CTkLabel(main_frame1,text='CREATE PASSWORD :',padx=20,pady=10,font=('comicsans',15,'bold'),fg_color='transparent',text_color=LABEL_TEXT)
        cemaillabel=CTkLabel(main_frame1,text='ENTER EMAIL ID : ',padx=20,pady=10,font=('comicsans',15,'bold'),fg_color='transparent',text_color=LABEL_TEXT)

        cuserlabel.grid(row=1, column=0, padx=20, pady=5, sticky='w')
        cpasslabel.grid(row=2, column=0, padx=20, pady=5, sticky='w')
        cemaillabel.grid(row=3, column=0, padx=20, pady=5, sticky='w')

        cuservar=StringVar()
        cpassvar=StringVar()
        cemailvar=StringVar()

        cuserentry=CTkEntry(main_frame1,textvariable=cuservar,width=260)
        cpassentry=CTkEntry(main_frame1,textvariable=cpassvar,width=260)
        cemailentry=CTkEntry(main_frame1,textvariable=cemailvar,width=260)

        cuserentry.grid(row=1, column=1, padx=20, pady=5, sticky='ew')
        cpassentry.grid(row=2, column=1, padx=20, pady=5, sticky='ew')
        cemailentry.grid(row=3, column=1, padx=20, pady=5, sticky='ew')

        #button to call dataentry function for creating account in database
        csubmitbutton=CTkButton(main_frame1,text='SUBMIT',command=dataentry,fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=120)
        csubmitbutton.grid(row=4, column=1, padx=20, pady=(10,5), sticky='e')

        #button to close create account screen and go back to login screen
        loginbutton=CTkButton(main_frame1,text='GO TO SIGN IN PAGE',command=lambda:[widgetdestroy(root1),login()],fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=200)
        loginbutton.grid(row=5, column=0, columnspan=3, padx=20, pady=(5,10), sticky='ew')

        #button to call the show function for showing password entered by user
        cshowbutton=CTkButton(main_frame1,text='SHOW',command=lambda:show(cpassentry,root1,cshowbutton,cpassvar),fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=80)
        cshowbutton.grid(row=2, column=2, padx=10, pady=5)

        main_frame1.grid_columnconfigure(1, weight=1)

        #binding event to cpassentry to call hide function to hide password as the user enters it
        cpassentry.bind('<KeyRelease>',lambda event:hide(event,cpassentry,cpassvar))

        # binding event to cpassentry to call backspace function when backspace key is pressed
        cpassentry.bind('<BackSpace>',lambda event:backspace(event,cpassentry))

        root1.mainloop()

    # to make changes to variable password while password is in show mode
    def updatepassword(event):

        global password
        password+=event.char

    # to make changes to the variable password as the user presses delete
    def delete(event,e_name):

        global password
        cur_position=e_name.index(INSERT)
        password=password[0:cur_position]+password[cur_position+1:]

    # to make changes to the variable password as the user presses backspace
    def backspace(event,e_name):

        global password
        cur_position=e_name.index(INSERT)
        password=password[0:cur_position-1]+password[cur_position:]

    #to hide the password while user is entering and storing the entered password in a variable password while it is in hide mode
    def hide(event,pe_name,v_name):

        lst=['exclam','quotedbl','numbersign','dollar','ampersand','apostrophe','parenleft','parenright',
             'asterisk','plus','comma','underscore','minus','period','slash','colon','semicolon','less',
             'equal','greater','question','at','bracketleft','backslash','bracketright','asciicircum',
             'grave','braceleft','braceright','bar','asciitilde']
        
        if event.keysym in string.ascii_letters or  event.keysym in string.digits or  event.keysym in lst:
            global password
            passvalue=pe_name.get()
            password+=event.char
            length=len(passvalue)
            l='*'*length
            v_name.set(l)

    #to show the password entered by user when showbutton is pressed
    def show(pe_name,r_name,b_name,v_name):

        v_name.set(password)

        # to unbind the keyrelease event
        pe_name.unbind('<KeyRelease>')
        pe_name.bind('<KeyPress>',updatepassword)
        b_name.destroy()

        #button to call the hidepass function for hiding password entered by user
        hidebutton=CTkButton(r_name,text='HIDE',command=lambda:[hidepass(hidebutton,pe_name,r_name,b_name,v_name)])
        hidebutton.grid(row=2,column=2)

    #to hide the password entered by user when the hidebutton is pressed
    def hidepass(hidebutton,pe_name,r_name,b_name,v_name):

        passvalue=pe_name.get()
        length=len(passvalue)
        l='*'*length
        v_name.set(l)
        hidebutton.destroy()

        #button to call the show function for showing password entered by user
        b_name=CTkButton(r_name,text='SHOW',command=lambda:show(pe_name,r_name,b_name,v_name))
        b_name.grid(row=2,column=2)
        pe_name.unbind('<KeyPress>')

        #binding event to passentry to call hide function to hide password as the user enters it
        pe_name.bind('<KeyRelease>',lambda event: hide(event,pe_name,v_name))
        
    root.maxsize(600,300)
    root.minsize(600,300)
    root.geometry('600x300')
    root.title('PASSWORD MANAGER')
    # bimage=CTkImage(Image.open("D:\study\programming\Python\pass_image.png"),size=(600,300))

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # mainlabel=CTkLabel(root,image=bimage,text="")
    main_frame = CTkFrame(root, fg_color=CARD_BG, corner_radius=25, border_width=2, border_color='#1f3761')
    main_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
    main_frame.grid_columnconfigure(1, weight=1)

    header = CTkFrame(main_frame, fg_color='#19203a', corner_radius=20)
    header.grid(row=0, column=0, columnspan=3, padx=20, pady=(20,10), sticky='ew')
    header.grid_columnconfigure(0, weight=1)

    l1=CTkLabel(header,text='WELCOME TO PASSWORD MANAGER',font=('comicsans' ,18, 'bold' ,'underline'),text_color=LABEL_TEXT)
    l1.grid(row=0, column=0, padx=20, pady=10)

    userlabel=CTkLabel(main_frame,text='USERNAME :',padx=20,pady=10,font=('comcisans',15,'bold'),fg_color='transparent',text_color=LABEL_TEXT)
    passlabel=CTkLabel(main_frame,text='PASSWORD :',padx=20,pady=10,font=('comcisans',15,'bold'),fg_color='transparent',text_color=LABEL_TEXT)

    userlabel.grid(row=1, column=0, padx=20, pady=5, sticky='w')
    passlabel.grid(row=2, column=0, padx=20, pady=5, sticky='w')

    uservar=StringVar()
    passvar=StringVar()

    userentry=CTkEntry(main_frame,textvariable=uservar,width=260)
    passentry=CTkEntry(main_frame,textvariable=passvar,width=260)

    userentry.grid(row=1, column=1, padx=20, pady=5, sticky='ew')
    passentry.grid(row=2, column=1, padx=20, pady=5, sticky='ew')

    #button to call dataverification function for checking details of user and proceed accordingly
    submitbutton=CTkButton(main_frame,text='SIGN IN',command=dataverification,fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=120)
    submitbutton.grid(row=3, column=0, padx=20, pady=(10,20), sticky='e')

    #button to call cacc function for closing login screen and open the create account screen
    caccbutton=CTkButton(main_frame,text='CREATE ACCOUNT',command=cacc,fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=170)
    caccbutton.grid(row=3, column=1, padx=20, pady=(10,20), sticky='w')

    #button to call the show function for showing password entered by user
    showbutton=CTkButton(main_frame,text='SHOW',command=lambda:[show(passentry,root,showbutton,passvar)],fg_color=BUTTON_BG,hover_color=BUTTON_HOVER,text_color=LABEL_TEXT,width=80)
    showbutton.grid(row=2, column=2, padx=10, pady=5)

    #binding event to passentry to call hide function to hide password as the user enters it
    passentry.bind('<KeyRelease>',lambda event:hide(event,passentry,passvar))

    # binding event to passentry to call backspace function when backspace key is pressed
    passentry.bind('<BackSpace>',lambda event:backspace(event,passentry))
    passentry.bind('<Delete>',lambda event:delete(event,passentry))

    root.mainloop()
login()


    

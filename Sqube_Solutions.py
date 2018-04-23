# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	


#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
#https://gist.github.com/SirRobo/c503014bbb03088bec37a61231036461
#https://blog.devcolor.org/heating-up-with-firebase-tutorial-on-how-to-integrate-firebase-into-your-app-6ce97440175d


import Tkinter as tk
import tkMessageBox
import pyrebase
import editedrfid
import time

config = {
    "apiKey": "AIzaSyD3w34u_ldmgK61PaH5TAlQV64jj4ro1l8",
    "authDomain": "superstore-bde7f.firebaseapp.com",
    "databaseURL": "https://superstore-bde7f.firebaseio.com",
    "projectId": "superstore-bde7f",
    "storageBucket": "gs://superstore-bde7f.appspot.com",
    "messageSenderId": "superstore-bde7f.appspot.com",
    "serviceAccount": "/home/pi/Desktop/Sqube_Solutions/SuperStore-5486286531d1.json"
  }

# Initializing firebase for the GUI
firebase = pyrebase.initialize_app(config)

# Standard fonts used in the app
H1_FONT= ("Verdana", 14)
H2_FONT= ("Helvetica", 12)


# Container class that has all the frames of the GUI
class StoreHelpLine(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Search_Page, Call_Help, Product_Details, Wrong_Login):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
# The default start page of the app (Sign in page) 
class StartPage(tk.Frame):
    
    def Sign_In(self):
        
        emailSt = emailEL.get()
        pwordSt = pwordEL.get()
        
        ## Saving the email id of the user for the "Add to cart" Function
        file = open("emailid.txt","w")
        file.write(emailSt)
        file.close() 
        
        ## Initializing the Authentication
        auth = firebase.auth()
        try:
            user = auth.sign_in_with_email_and_password(emailSt, pwordSt)        
            self.controller.show_frame(Search_Page)
        except:
            self.controller.show_frame(Wrong_Login)
            
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        global emailEL
        global pwordEL
        
        self.controller = controller
        
        label = tk.Label(self, text="Store HelpLine", font=H1_FONT)
        label.grid(row=0,column=0,sticky="ew")
        
        lable2 = tk.Label(self, text="Sign-In", font=H2_FONT)
        lable2.grid(sticky="ew")

        emailL = tk.Label(self, text='Email: ')
        pwordL = tk.Label(self, text='Password: ')
        emailL.grid(row=2, sticky="w")
        pwordL.grid(row=3, sticky="w")
        
        emailEL = tk.Entry(self) # The entry input
        pwordEL = tk.Entry(self, show='*')
        emailEL.grid(row=2, column=1)
        pwordEL.grid(row=3, column=1)
        
        button = tk.Button(self, text="Sign-In", command=self.Sign_In)
        button.grid(columnspan=2, sticky="w")
        
        
# The search page to search the items in the database
class Search_Page(tk.Frame):
    
    def search_function(self):
        
        searchSt = searchEL.get()
        
        # Saving the searched item to a file, so that it can be used later
        file = open("temp.txt","w")
        file.write(searchSt)
        file.close()
        
        self.controller.show_frame(Product_Details)

    def call_for_help(self):
        
        result = tkMessageBox.askquestion("Tk", "Are you sure about it?")
        if result == "yes":
            editedrfid.main()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Store HelpLine", font=H1_FONT)
        label.grid(pady=10,padx=10)
        
        global searchEL
        
        self.controller = controller
        
        searchl = tk.Label(self, text="Search", font=H2_FONT)
        searchl.grid(row=2, sticky="w")
        
        searchEL = tk.Entry(self)
        searchEL.grid(row=2, column=1)
        
        button2 = tk.Button(self, text="Search", command=self.search_function)
        button2.grid(columnspan=2, sticky="w")
       
        button1 = tk.Button(self, text="Sign Out",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(columnspan=2, sticky="w")
                
        button3 = tk.Button(self, text="Request Help", command=self.call_for_help)
        button3.grid(columnspan=2, sticky="w")
        
        global waitl
        waitl = tk.Label(self, text=" ")
        waitl.grid(columnspan=2, sticky="w")
        

# Displays the Product details and give the option to "Add to cart"
class Product_Details(tk.Frame):
    
    ## This is a function that creats a dialog box when ever a person calls for help
    def call_for_help(self):
      
        result = tkMessageBox.askquestion("Tk", "Are you sure about it?")
        if result == "yes":
            editedrfid.main()


    def add_to_cart(self):
        
        file = open("emailid.txt","r")
        email = file.readline()
        db = firebase.database()
  
        userdata = db.child("users").get()
        
        user_checker = False
        
        # looking for the user in the database and then adding cart for it
        for user in userdata.each():
            eachuser = db.child("users").child(user.key()).get()
            
            for myuser in eachuser.each():
                
                if myuser.key() == "Name" and myuser.val() == email:
                    user_checker = True
                else:
                    user_checker = False
                    break
        
                if user_checker:
                    db.child("users").child(user.key()).child("cart").child(sku).set(True)
    
    def jugad(self):
        
        global sku
        aisle_num = -1
        brand = None
        desc = None
        name = None
        price = None            

        file = open("temp.txt","r+")
        searchItem = file.readline()
        db = firebase.database()
        searchval = db.child("Items").get()
          
        # Looking for the searched item in the database
        for item in searchval.each():
            about = db.child("Items").child(item.key()).get()
            
            for itemdes in about.each():
                if itemdes.key() == "Name":
                    if itemdes.val() == searchItem:
                        name = itemdes.val()
                        item_checker = True
                    else:
                        item_checker = False
                        break
                elif itemdes.key() == "Aisle Number": aisle_num = itemdes.val()
                elif itemdes.key() == "Brand": brand = itemdes.val() 
                elif itemdes.key() == "Description": desc = itemdes.val()
                elif itemdes.key() == "Price": price = itemdes.val()
                elif itemdes.key() == "SKU": sku = itemdes.val()
      
            if item_checker:
                break
            else:
                aisle_num = -1
                brand = None
                desc = None
                name = None
                price = None

        file.close()   
        
        labelna.config(text = name)
        labelas.config(text = aisle_num)
        labelbr.config(text = brand)
        labelpr.config(text = price)

    ## This is the constructor to build the GUI on the screen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        global labelna
        global labelas
        global labelbr
        global labelpr
        
        label = tk.Label(self, text="Store HelLine", font=H1_FONT)
        label.grid(pady=10,padx=10)
        
        label2 = tk.Label(self, text="PRODUCT SCREEN",font=H2_FONT)
        label2.grid(row=2)
        
        self.controller = controller
        
        labelref = tk.Label(self, text="Click Refresh after every search", font=H2_FONT, fg="Red")
        labelref.grid(row=3)
        
        button4 = tk.Button(self, text="Refresh",command=self.jugad)
        button4.grid(columnspan=1, column=2, sticky="w", row=3)
        
        labelname = tk.Label(self, text="Name")
        labelname.grid(row=4, column=1)                     
        labelna = tk.Label(self, text="Click Refresh")
        labelna.grid(row=4, column=2)
        
        labelaisle = tk.Label(self, text="Aisle Number")
        labelaisle.grid(row=5, column=1)                     
        labelas = tk.Label(self, text="Click Refresh")
        labelas.grid(row=5, column=2)
        
        labelbrand = tk.Label(self, text="Brand")
        labelbrand.grid(column=1, row=6)   
        labelbr = tk.Label(self, text="Click Refresh")
        labelbr.grid(column=2, row=6)
        
        labelprice = tk.Label(self, text="Price")
        labelprice.grid(column=1, row=7)                     
        labelpr = tk.Label(self, text="Click Refresh")
        labelpr.grid(column=2, row=7)

        button1 = tk.Button(self, text="Add to Cart", command=self.add_to_cart)
        button1.grid(columnspan=1, sticky="w", row=8)

        button2 = tk.Button(self, text="Cancel",
                            command=lambda: controller.show_frame(Search_Page))
        button2.grid(columnspan=1, column=2, sticky="e", row=8)
        
        button3 = tk.Button(self, text="Request Help", command=self.call_for_help)
        button3.grid(columnspan=2, sticky="w")
        

class Wrong_Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="StoreHelpLine", font=H1_FONT)
        label.pack(pady=10,padx=10)

        label2 = tk.Label(self, text="Worng Credentials", font=H2_FONT)
        label2.pack(pady=10,padx=10)
    
        button1 = tk.Button(self, text="OK",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)
app = StoreHelpLine()
app.mainloop()

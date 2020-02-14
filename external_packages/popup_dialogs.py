import tkinter
import os
from external_packages.widget_Creater import widget_creater
from external_packages.backend import database_query_constants
import datetime
import sqlite3
import Images
class message_dialog(tkinter.Toplevel):
    def __init__(self,parent,text,title,n,button_text = None,compound_image = None):
        super(message_dialog,self).__init__(parent,bg = "#FCE8E8")
        self.title(title)
        self.titl = title
        self.parent = parent
        self.geometry("%dx%d+%d+%d"%(350,160,self.parent.winfo_rootx()+350,self.winfo_rooty()+250))
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW",self.cancel)
        self.iconbitmap(Images.ICON)
        self.grab_set()
        self.text = text
        self.n = n
        self.button_text = button_text
        self.compound_image = compound_image
        self.event = None
        self.keyboard_key_bindings()
        self.initial_focus = self.widget_Assembler()
        self.initial_focus.focus_set()
        self.wait_window(self)
    
    def widget_Assembler(self):
        wc_obj = widget_creater()
        x = self.n
        #creating message label
        message_label = wc_obj.create_labels(
            master = self,background = ["#FCE8E8"],n = 1,font = [("Segoe UI",13,"bold")],foreground = ["black"],
            text = [self.text]
        )
        if(self.titl=="Save Changes" or self.titl=="Confirmation"):
            message_label[0].place(x = 50,y = 30)
        elif(self.titl=="Save Notification"):
            message_label[0].place(x = 103,y = 30)
        elif(self.titl=="Delete Notification"):
            message_label[0].place(x = 90,y = 30)
        elif(self.titl=="Notification"):
            message_label[0].place(x = 105,y = 30)
        elif(self.titl=="Some Information is incorrect" and self.text=="INVALID AGE"):
            message_label[0].place(x = 120,y = 30)
        elif(self.titl=="Some Information is incorrect"):
            message_label[0].place(x = 108,y = 30)
        elif(self.titl=="Some Information is missing" and (self.text=="Please enter disease information" or self.text=="Please enter symptoms of disease" or self.text=="Please enter medicines prescription")):
            message_label[0].place(x = 50,y = 30)
        elif(self.titl=="Some Information is missing"):
            message_label[0].place(x = 108,y = 30)
        elif(self.titl=="Required"):
            message_label[0].place(x = 30,y = 30)
        #creating buttons
        button_width = []
        button_height = []
        button_background = []
        button_activebackground = []
        button_foreground = []
        button_font = []
        button_compound = []

        while(x>0):
            button_width.append(100)
            button_height.append(27)
            button_background.append("#697DCE")
            button_activebackground.append("#697DCE")
            button_foreground.append("#000000")
            button_font.append(("Segoe UI",14))
            button_compound.append(tkinter.LEFT)
            x-=1
            
        dialog_buttons = wc_obj.create_buttons(
            master = self,width = button_width,height = button_height,background = button_background,
            activebackground = button_activebackground,n = self.n,foreground = button_foreground,
            font = button_font,text = self.button_text,image = self.compound_image,compound = button_compound
        )
        dialog_buttons[0].configure(command = self.ok)
        if(self.n==2):
            dialog_buttons[0].place(x = 40,y = 80)
            dialog_buttons[1].place(x = 200,y = 80)
            dialog_buttons[1].configure(command = self.cancel)
        elif(self.n==1):
            dialog_buttons[0].place(x = 125,y = 80)
        return dialog_buttons[0]
    
    def keyboard_key_bindings(self):
        self.bind("<Return>",self.ok)
        self.bind("<Escape>",self.cancel)
    
    def ok(self,event = None):
        if(self.n==2):
            self.event = "ok button clicked"
        self.withdraw()
        self.update_idletasks()
        self.cancel(event)
    
    def cancel(self,event = None):
        if(self.n==2 and self.event==None):
            self.event = "cancel button clicked"
        self.parent.focus_set()
        self.destroy()

class dialog_box(tkinter.Toplevel):
    def __init__(self,parent,label_text,button_text,compound_image,title,update_case_no = None):
        super(dialog_box,self).__init__(parent,bg = "#EFE4E4")
        self.parent = parent
        self.label_text = label_text
        self.n = len(label_text)
        if(self.n==2):
            self.geometry("%dx%d+%d+%d"%(411,220,self.parent.winfo_rootx()+350,self.parent.winfo_rooty()+150))
        elif(self.n==1):
            if(self.label_text[0]!="Date : " and self.label_text[0]!="Name : " and self.label_text[0]!="Age : " and self.label_text[0]!="Gender : "):
                self.geometry("%dx%d+%d+%d"%(450,220,self.parent.winfo_rootx()+350,self.parent.winfo_rooty()+150))
            else:
                self.geometry("%dx%d+%d+%d"%(320,120,self.parent.winfo_rootx()+350,self.parent.winfo_rooty()+150))
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW",self.cancel)
        self.iconbitmap(Images.ICON)
        self.grab_set()
        self.titl = title
        self.title(self.titl)
        self.compound_image = compound_image
        self.button_text = button_text
        self.dialog_entry_box = None
        self.dialog_text_box = None
        self.Update = None
        self.query_Result = None
        self.event = None
        self.update_case_no = update_case_no
        self.dialog_bindings()
        self.initial_focus = self.widget_Assembler()
        self.initial_focus.focus_set()
        self.wait_window(self)
    
    def widget_Assembler(self):
        x = self.n
        wc_obj = widget_creater()
        #creating labels
        label_background = []
        label_font = []
        label_foreground = []
        while(x>0):
            label_background.append("#EFE4E4")
            label_font.append(("Segoe UI",14))
            label_foreground.append("#000000")
            x-=1
        dialog_labels = wc_obj.create_labels(
            master = self,background = label_background,n = self.n,font = label_font,foreground = label_foreground,
            text = self.label_text
        )
        if(self.n==1):
            if(self.titl!="Update Date" and self.titl!="Update Name" and self.titl!="Update Age" and self.titl!="Update Gender"):
                dialog_labels[0].place(x = 5,y = 10)
            else:
                if(self.titl=="Update Date" or self.titl=="Update Name" or self.titl=="Update Age"):
                    dialog_labels[0].place(x = 20,y = 20)
                elif(self.titl=="Update Gender"):
                    dialog_labels[0].place(x = 8,y = 20)
        elif(self.n==2):
            dialog_labels[0].place(x = 46,y = 50)
            dialog_labels[1].place(x = 70,y = 105)
        
        #creating entry box and text box
        if(self.n==2):
            self.dialog_entry_box = wc_obj.create_entry_box(
                master = self,width = 20,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",15),n = self.n
            )
            self.dialog_entry_box[0].place(x = 142,y = 50)
            self.dialog_entry_box[1].place(x = 142,y = 110)
        else:
            if(self.titl!="Update Date" and self.titl!="Update Name" and self.titl!="Update Age" and self.titl!="Update Gender"):
                self.dialog_text_box = wc_obj.create_text_box(
                    master = self,width = 37,height = 7,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",13),
                    n = self.n
                )
                if(self.titl=="Update Disease"):
                    self.dialog_text_box[0].place(x = 96,y = 15)
                elif(self.titl=="Update Symptoms" or self.titl=="Update Medicines"):
                    self.dialog_text_box[0].place(x = 110,y = 15)
                elif(self.titl=="Update Pathological Information"):
                    self.dialog_text_box[0].configure(width = 30)
                    self.dialog_text_box[0].place(x = 170,y = 15)
            else:
                self.dialog_entry_box = wc_obj.create_entry_box(
                    master = self,width = 20,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",15),n = self.n
                )
                if(self.titl=="Update Date"):
                    self.dialog_entry_box[0].place(x = 80,y = 23)
                elif(self.titl=="Update Name" or self.titl=="Update Gender"):
                    self.dialog_entry_box[0].place(x = 90,y = 23)
                elif(self.titl=="Update Age"):
                    self.dialog_entry_box[0].place(x = 76,y = 23)

        #creating button
        dialog_buttons = wc_obj.create_buttons(
            master = self,width = [100],height = [27],background = ["#697DCE"],activebackground = ["#697DCE"],
            n = 1,foreground = ["#000000"],font = [("Segoe UI",14)],text = self.button_text,image = self.compound_image,
            compound = [tkinter.LEFT]
        )
        dialog_buttons[0].configure(command = self.ok)
        if(dialog_buttons[0].cget("text")=="Search"):
            dialog_buttons[0].place(x = 164,y = 160)
        elif(dialog_buttons[0].cget("text")=="Update"):
            if(self.titl!="Update Date" and self.titl!="Update Name" and self.titl!="Update Age" and self.titl!="Update Gender"):
                dialog_buttons[0].place(x = 180,y = 183)
            else:
                dialog_buttons[0].place(x = 110,y = 80)
        return dialog_buttons[0]
    
    def dialog_bindings(self):
        if(self.titl=="Update Name" or self.titl=="Update Date" or self.titl=="Search Patient" or self.titl=="Update Age" or self.titl=="Update Gender"):
            self.bind("<Return>",self.ok)
            self.bind("<Escape>",self.cancel)
        else:
            self.bind("<Escape>",self.cancel)

    def ok(self,event = None):
        if(not self.validate()):
            self.initial_focus.focus_set()
        else:
            if(event==None):
                self.event = "ok button clicked"
            self.withdraw()
            self.update_idletasks()
            self.apply()
            self.cancel(event)
    
    def cancel(self,event = None):
        if(event!=None):
            self.event = event.keycode
        elif(self.event==None):
            self.event = "cancel button clicked"
        self.parent.focus_set()
        self.destroy()
    
    def validate(self):
        if(self.titl == "Search Patient"):
            temp = None
            for i in range(2):
                if(self.dialog_entry_box[i].get()!=""):
                    try:
                        temp = self.dialog_entry_box[i].get()
                        temp = int(temp)
                        raise ValueError
                    except ValueError:
                        if(i==0):
                            if(type(temp)==str):
                                message_dialog(
                                    parent = self,text = "INVALID CASE NO.",title = "Some Information is incorrect",n = 1,
                                    button_text = ["OK"],compound_image = [Images.OK]
                                )
                                return 0
                            elif(type(temp)==int):
                                return 1
                        elif(i==1):
                            if(type(temp)==str):
                                return 1
                            elif(type(temp)==int):
                                message_dialog(
                                    parent = self,text = "INVALID NAME",title = "Some Information is incorrect",n = 1,
                                    button_text = ["OK"],compound_image = [Images.OK]
                                )
                                return 0
        else:
            try:
                if(self.titl=="Update Date"):
                    self.Update = self.dialog_entry_box[0].get()
                    if(self.Update.count("/")==2 or self.Update.count("-")==2 or self.Update.count(".")==2):
                        return 1
                    else:
                        message_dialog(
                        parent = self,text = "INVALID DATE",title = "Some Information is incorrect",n = 1,
                        button_text = ["OK"],compound_image = ["Images/ok.png"]
                        )
                        return 0
                elif(self.titl=="Update Name"):
                    self.Update = self.dialog_entry_box[0].get()
                    self.Update = int(self.Update)
                    raise ValueError
                elif(self.titl=="Update Gender"):
                    self.Update = self.dialog_entry_box[0].get().lower()
                    if(self.Update!="male" and self.Update!="female" and self.Update!="m" and self.Update!="f"):
                        message_dialog(
                            parent = self,text = "INVALID GENDER",title = "Some Information is incorrect",n = 1,
                            button_text = ["OK"],compound_image = ["Images/ok.png"]
                        )
                        self.Update = None
                        return 0
                    return 1
                elif(self.titl=="Update Age"):
                    self.Update = self.dialog_entry_box[0].get()
                elif(self.titl=="Update Disease" or self.titl=="Update Symptoms" or self.titl=="Update Medicines" or self.titl=="Update Pathological Information"):
                    self.Update = self.dialog_text_box[0].get("1.0","end-1c")
                    return 1
            except ValueError:
                if(self.titl=="Update Name"):
                    if(type(self.Update)==str):
                        return 1
                    elif(type(self.Update)==int):
                        message_dialog(
                            parent = self,text = "INVALID NAME",title = "Some Information is incorrect",n = 1,
                            button_text = ["OK"],compound_image = ["Images/ok.png"]
                        )
                        self.Update = None
                        return 0
                elif(self.titl=="Update Age"):
                    if(type(self.Update)==int):
                        return 1
                    elif(type(self.Update)==str):
                        message_dialog(
                            parent = self,text = "INVALID AGE",title = "Some Information is incorrect",n = 1,
                            button_text = ["OK"],compound_image = ["Images/ok.png"]
                        )
                        self.Update = None
                        return 0
    
    def apply(self):
        documents_folder_path = os.path.expanduser("~/Documents")
        documents_folder_path = documents_folder_path.replace("\\","/",documents_folder_path.count("\\"))
        db_connection = sqlite3.connect(documents_folder_path+"/Doc Manager/patient.db")
        query_constants_object = database_query_constants()
        current_date = datetime.datetime.now().strftime("%d/%m/%y")
        if(self.titl=="Search Patient" and self.dialog_entry_box[0].get()!=""):
            self.query_Result = db_connection.execute(query_constants_object.get_data_by_case_no % int(self.dialog_entry_box[0].get())).fetchall()
        elif(self.titl=="Search Patient" and self.dialog_entry_box[1].get()!=""):
            self.query_Result = db_connection.execute(query_constants_object.get_data_by_name % self.dialog_entry_box[1].get()).fetchall()
        elif(self.titl=="Update Name"):
            db_connection.execute(query_constants_object.update_name % (self.Update,self.update_case_no))
        elif(self.titl=="Update Date"):
            db_connection.execute(query_constants_object.update_date % (self.Update,self.update_case_no))
        elif(self.titl=="Update Age"):
            db_connection.execute(query_constants_object.update_age % (self.Update,self.update_case_no))
        elif(self.titl=="Update Gender"):
            db_connection.execute(query_constants_object.update_gender % (self.Update,self.update_case_no))
        elif(self.titl=="Update Disease"):
            db_connection.execute(query_constants_object.update_disease % (self.Update,self.update_case_no))
            f = open(documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.update_case_no)+"/Disease.txt","a")
            f.write("\n\n"+current_date+" : "+self.Update)
            f.close()
        elif(self.titl=="Update Symptoms"):
            db_connection.execute(query_constants_object.update_symptoms % (self.Update,self.update_case_no))
            f = open(documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.update_case_no)+"/Symptoms.txt","a")
            f.write("\n\n"+current_date+" : "+self.Update)
            f.close()
        elif(self.titl=="Update Medicines"):
            db_connection.execute(query_constants_object.update_medicines % (self.Update,self.update_case_no))
            f = open(documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.update_case_no)+"/Medicines.txt","a")
            f.write("\n\n"+current_date+" : "+self.Update)
            f.close()
        elif(self.titl=="Update Pathological Information"):
            db_connection.execute(query_constants_object.update_pathological_info % (self.Update,self.update_case_no))
            f = open(documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.update_case_no)+"/Pathological Information.txt","a")
            f.write("\n\n"+current_date+" : "+self.Update)
            f.close()
        db_connection.commit()
        db_connection.close()
        if(self.query_Result==[]):
            self.query_Result = None
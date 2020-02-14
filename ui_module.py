import tkinter
from tkinter import ttk
from external_packages import backend
from external_packages.widget_Creater import widget_creater
from external_packages.popup_dialogs import dialog_box,message_dialog
from threading import Thread
import time
import shutil
import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import webbrowser
import Images
#this is loading window class
class app_window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("624x302+370+200")
        self.configure(bg = "#1B5384")
        self.overrideredirect(True)
        self.after(5000,self.navigate)
        self.widget_initializer()

    def widget_initializer(self):
        wc_obj = widget_creater()
        bg_label = wc_obj.create_labels(self,["#1B5384"],1,image = [Images.FLASH])
        bg_label[0].pack()
        st = ttk.Style()
        st.theme_use("winnative")
        st.configure("#6ECCC7.Horizontal.TProgressbar",background = "#6ECCC7")
        self.pg_bar = ttk.Progressbar(
            master = self,style = "#6ECCC7.Horizontal.TProgressbar",mode = "determinate",
            length = 624,maximum = 100,orient = tkinter.HORIZONTAL,value = 20
        )
        self.pg_bar.pack()
        t1 = Thread(target = self.progress)
        t1.start()
        self.mainloop()
    
    def progress(self):
        while(self.pg_bar["value"]!=self.pg_bar["maximum"]):
            time.sleep(1)
            self.pg_bar["value"]+=20
    
    def navigate(self):
        self.destroy()
        documents_folder_path = os.path.expanduser("~/Documents").replace("\\","/",os.path.expanduser("~/Documents").count("\\"))
        if(not os.path.isfile(documents_folder_path+"/Doc Manager/information.dat")):
            doctorInformationWindow()
        else:
            startingWindow()

#this is doctor's information collector class
class doctorInformationWindow(tkinter.Tk):
    def __init__(self):
        super(doctorInformationWindow,self).__init__()
        self.geometry("1100x600+200+60")
        self.configure(bg = "#EFE4E4")
        self.title("Please Enter Mandatory Information")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.text_box_list = None
        self.backend_obj = backend.doctors_Information_Window_Backend()
        self.widget_assembler()

    def widget_assembler(self):
        upper_frame = tkinter.Frame(
            master = self,width = 1100,height = 89,bg = "#697DCE",bd = 0
        )
        upper_frame.pack(side = tkinter.TOP)
        wc_obj = widget_creater()
        header_label = wc_obj.create_labels(
            master = upper_frame,background = ["#697DCE"],n = 1,font = [("Segoe UI",20,"bold")],
            foreground = ["#000000"],text = ["DOCTORS INFORMATION"]
        )
        header_label[0].place(x = 380,y = 20)

        #information indicator label
        info_label_list = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4"],
            n = 10,font = [("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),
            ("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold")],
            foreground = ["#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000"],
            text = ["Hospital/Clinic Name","Doctor's Name","Qualification","Specialization","Registration No.","Address(street/area)",
            "City/District/Town","State","Pincode","Clinic/Hospital Timing"]
        )
        #y coordinate for labels
        y = 100
        for i in range(10):
            if(i<5):
                info_label_list[i].place(x = 82,y = y)
                y += 90
                if(i+1==5):
                    y = 100
            else:
                info_label_list[i].place(x = 662,y = y)
                y+=90
        y = 130
        
        #text list box
        self.text_box_list = wc_obj.create_text_box(
            master = self,width = 30,height = 2,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",15),n = 10
        )
        for i in range(10):
            if(i<5):
                self.text_box_list[i].place(x = 85,y = y)
                y+=90
                if(i+1==5):
                    y = 130
            else:
                self.text_box_list[i].place(x = 665,y = y)
                y+=90
        
        #submit button
        button_list = wc_obj.create_buttons(
            master = self,width = [100],height = [27],background = ["#697DCE"],activebackground = ["#697DCE"],n = 1,
            foreground = ["#000000"],font = [("Segoe UI",14)],text = ["Submit"],image = [Images.SUBMIT],compound = [tkinter.LEFT]
        )
        button_list[0].configure(command = self.submit_information_button)
        button_list[0].place(x = 493,y = 560)
    
    def submit_information_button(self):
        doctor_data = []
        for i in range(10):
            if(self.text_box_list[i].get("1.0","end-1c")!=""):
                doctor_data.append(self.text_box_list[i].get("1.0","end-1c"))
            else:
                message_dialog(
                    parent = self,text = "Please enter the required information",title = "Required",n = 1,button_text = ["OK"],
                    compound_image = [Images.OK]
                )
                break
        if(len(doctor_data)==10):
            self.backend_obj.save_doctors_data(doctor_data)
            message_dialog(
                parent = self,text = "Saved Successfully",title = "Save Notification",n = 1,button_text = ["OK"],
                compound_image = [Images.OK]
            )
            self.navigate()
    
    def navigate(self):
        self.destroy()
        startingWindow()

#this is options window
class startingWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x600+120+60")
        self.configure(bg = "#EFE4E4",bd=0)
        self.title("Doc Manager")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.widget_assembler()

    def widget_assembler(self):
        wc_obj = widget_creater()
        window_labels = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4"],n = 3,font = [("Segoe UI",20,"italic"),("Segoe UI",15,"italic")],
            foreground = ["#7E785F","#653131"],text = ["Doc Manager","'Your limitaion-it's only your imagination'"],image = [Images.UNDERLINE]
        )
        window_labels[0].place(x = 471,y = 5)
        window_labels[1].place(x = 370,y = 521)
        window_labels[2].place(x = 394,y = 55)
        options_button = wc_obj.create_buttons(self,[206,153],[220,170],
                        ["#EFE4E4","#EFE4E4"],["#EFE4E4","#EFE4E4"],2,["#000000","#000000"],
                        [("Segoe UI",10),("Segoe UI",10)],["Add new patient","Search patient"],
                        [Images.ADD_NEW_PATIENT,Images.MEDICAL_REPORT],[tkinter.TOP,tkinter.TOP]
                        )
        #add new patient button
        options_button[0].configure(command = self.navigate_to_prescription_window)
        options_button[0].place(x = 300,y = 120)
        #search patient button
        options_button[1].configure(command = self.search_patient)
        options_button[1].place(x = 600,y = 165)
    
    def navigate_to_prescription_window(self):
        self.destroy()
        prescriptionWindow()
    
    def search_patient(self):
        search_object = dialog_box(
            parent = self,label_text = ["Case No. : ","Name : "],button_text = ["Search"],compound_image = [Images.SEARCH],
            title = "Search Patient"
        )
        if(search_object.query_Result!=None):
            self.destroy()
            if(len(search_object.query_Result)==1):
                patientInformation(search_object.query_Result)
            elif(len(search_object.query_Result)>1):
                deleteAllWindow("Total Cases",search_object.query_Result)
        elif((search_object.event==13 or search_object.event=="ok button clicked") and search_object.query_Result==None):
            message_dialog(
                parent = self,text = "No Record Found",title = "Notification",n = 1,
                button_text = ["OK"],compound_image = [Images.OK]
            )
#this is prescription window class
class prescriptionWindow(tkinter.Tk):
    def __init__(self):
        super(prescriptionWindow,self).__init__()
        self.geometry("1100x600+200+60")
        self.configure(bg = "#EFE4E4")
        self.title("Doc Manager")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.entry_box_list = None
        self.text_box_list = None
        self.backend_obj = backend.prescriptionWindowBackendFunction()
        self.widget_assembler()

    def widget_assembler(self):
        side_frame = tkinter.Frame(master = self,width = 50,height = 600,bg = "#697DCE",bd = 0)
        side_frame.pack(side = tkinter.LEFT)
        wc_obj = widget_creater()
        
        #labels object list in the window
        label_list = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4"],
            n = 11,font = [("Segoe UI",20,"italic"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),
            ("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold"),("Segoe UI",15,"bold")],
            foreground = ["#7E785F","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000"],
            text = ["PRESCRIPTION","Case no : ","Patient Name : ","Date : ","Age : ","Gender : ","Disease : ","Symptoms : ","Medicines : ","Pathological Info : "],
            image = [Images.UNDERLINE]
        )
        #header label
        label_list[0].place(x = 480,y = 13)
        #case no label
        label_list[1].place(x = 141,y = 90)
        #name label
        label_list[2].place(x = 593,y = 90)
        #date label
        label_list[3].place(x = 169,y = 138)
        #age label
        label_list[4].place(x = 687,y = 138)
        #gender label
        label_list[5].place(x = 145,y = 190)
        #disease label
        label_list[6].place(x = 651,y = 190)
        #symptoms label
        label_list[7].place(x = 114,y = 243)
        #medicines label
        label_list[8].place(x = 625,y = 320)
        #pathological info label
        label_list[9].place(x = 50,y = 373)

        #creating entry box
        self.entry_box_list = wc_obj.create_entry_box(
            master = self,width = 30,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",14),n = 5
        )
        #case no entry box
        self.entry_box_list[0].place(x = 234,y = 95)
        #name entry box
        self.entry_box_list[1].place(x = 749,y = 97)
        #date entry box
        self.entry_box_list[2].place(x = 234,y = 145)
        #age entry box
        self.entry_box_list[3].place(x = 749,y = 145)
        #gender entry box
        self.entry_box_list[4].place(x = 234,y = 197)

        #creating text box
        self.text_box_list = wc_obj.create_text_box(
            master = self,width = 30,height = 4,background = "#ffffff",insertbackground = "#000000",font = ("Segoe UI",14),
            n = 4
        )
        #disease text box
        self.text_box_list[0].place(x = 749,y = 197)
        #symptoms text box
        self.text_box_list[1].place(x = 234,y = 250)
        #medicines text box
        self.text_box_list[2].place(x = 749,y = 325)
        #pathological info text box
        self.text_box_list[3].place(x = 234,y = 380)

        #creating buttons
        buttons_list = wc_obj.create_buttons(
            master = self,width = [100,100,30,30],height = [27,27,30,30],background = ["#697DCE","#697DCE","#697DCE","#697DCE"],
            activebackground = ["#697DCE","#697DCE","#697DCE","#697DCE"],n = 4,foreground = ["#000000","#000000"],
            font = [("Segoe UI",14),("Segoe UI",14)],text = ["Save","Reset"],image = [Images.SAVE,Images.RESET,Images.SEARCH,Images.DELETE],
            compound = [tkinter.LEFT,tkinter.LEFT]
        )
        #save button
        buttons_list[0].place(x = 408,y = 523)
        buttons_list[0].configure(command = self.save)
        #reset button
        buttons_list[1].configure(command = self.reset)
        buttons_list[1].place(x = 680,y = 523)
        #search button
        buttons_list[2].place(x = 7,y = 10)
        buttons_list[2].configure(command = self.search)
        #delete all button
        buttons_list[3].configure(command = self.see_all_cases)
        buttons_list[3].place(x = 7,y = 50)
    
    def search(self):
        search_object = dialog_box(
            parent = self,label_text = ["Case No. : ","Name : "],button_text = ["Search"],compound_image = [Images.SEARCH],
            title = "Search Patient"
        )
        if(search_object.query_Result!=None):
            self.destroy()
            if(len(search_object.query_Result)==1):
                patientInformation(search_object.query_Result)
            else:
                deleteAllWindow("Total Cases",search_object.query_Result)
        elif((search_object.event==13 or search_object.event=="ok button clicked") and search_object.query_Result==None):
            message_dialog(
                parent = self,text = "No Record Found",title = "Notification",n = 1,button_text = ["OK"],
                compound_image = [Images.OK]
            )
    
    def save(self):
        patient_data = []
        for i in range(len(self.entry_box_list)):
            if(self.entry_box_list[i].get()!=""):
                if(i==0):
                    temp = None
                    try:
                        temp = self.entry_box_list[i].get()
                        temp = int(temp)
                        raise ValueError
                    except ValueError:
                        if(type(temp)==int):
                            patient_data.append(temp)
                        elif(type(temp)==str):
                            message_dialog(
                                parent = self,text = "INVALID CASE NO.",title = "Some Information is incorrect",n = 1,
                                button_text = ["OK"],compound_image = [Images.OK]
                            )
                else:
                    patient_data.append(self.entry_box_list[i].get())
            elif(i==0):
                message_dialog(
                    parent = self,text = "Please enter case no",title = "Some Information is missing",
                    n = 1,button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==1):
                message_dialog(
                    parent = self,text = "Please patient name",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==2):
                message_dialog(
                    parent = self,text = "Please enter date",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==3):
                message_dialog(
                    parent = self,text = "Please enter age",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==4):
                message_dialog(
                    parent = self,text = "Please enter gender",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
        for i in range(len(self.text_box_list)):
            if(self.text_box_list[i].get("1.0","end-1c")!=""):
                patient_data.append(self.text_box_list[i].get("1.0","end-1c"))
            elif(i==0):
                message_dialog(
                    parent = self,text = "Please enter disease information",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==1):
                message_dialog(
                    parent = self,text = "Please enter symptoms of disease",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==2):
                message_dialog(
                    parent = self,text = "Please enter medicines prescription",title = "Some Information is missing",n = 1,
                    button_text = ["OK"],compound_image = [Images.OK]
                )
            elif(i==3):
                patient_data.append("NA")
        if(len(patient_data)==9):
            if(self.backend_obj.save_Data(patient_data)):
                message_dialog(
                    parent = self,text = "Saved Successfully",title = "Save Notification",n = 1,button_text = ["OK"],compound_image = [Images.OK]
                )
        
    def reset(self):
        for entry in self.entry_box_list:
            entry.delete(0,tkinter.END)
        for text in self.text_box_list:
            text.delete("1.0","end-1c")
        self.entry_box_list[0].focus_set()
    
    def see_all_cases(self):
        db_conn = sqlite3.connect(self.backend_obj.documents_folder_path+"/Doc Manager/patient.db")
        query = db_conn.execute(backend.database_query_constants().get_all_data).fetchall()
        db_conn.close()
        self.destroy()
        deleteAllWindow("All Cases",query)

#this is patient information window class
class patientInformation(tkinter.Tk):
    def __init__(self,query_Result,window_name = None,patient_name = None):
        super(patientInformation,self).__init__()
        self.geometry("1100x600+200+60")
        self.configure(bg = "#EFE4E4")
        self.title("Doc Manager")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.query_result = query_Result
        self.query_result_labels = None
        self.window_name = window_name
        self.patient_name = patient_name
        self.backend_obj = backend.patientWindowBackendFunction()
        self.widget_Assembler()
    
    def widget_Assembler(self):
        #side frame
        side_frame = tkinter.Frame(
            master = self,width = 50,height = 600,bg = "#697DCE",bd = 0
        )
        side_frame.pack(side = tkinter.LEFT)
        #creating labels
        wc_obj = widget_creater()
        labels_list = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4"],
            n = 11,font = [("Segoe UI",20,"italic"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),
            ("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold"),("Segoe UI",14,"bold")],
            foreground = ["#7E785F","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000"],
            text = ["PATIENT INFORMATION","Case No. : ","Name : ","Date : ","Age : ","Gender : ","Disease : ","Symptoms : ","Medicines : ","Pathological Info : "],
            image = [Images.UNDERLINE]
        )
        #creating query result labels
        self.query_result_labels = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4"],
            n = 9,font = [("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14)],
            foreground = ["#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000","#000000"],
            text = [self.query_result[0][0],self.query_result[0][1],self.query_result[0][2],self.query_result[0][3],
            self.query_result[0][4],self.query_result[0][5],self.query_result[0][6],self.query_result[0][7],self.query_result[0][8]]
        )
        for i in range(5,9):
            self.query_result_labels[i].configure(text = self.query_result_labels[i].cget("text").strip())
            if(len(self.query_result_labels[i].cget("text"))>=10):
                self.query_result_labels[i].configure(text = self.query_result_labels[i].cget("text")[:11]+"....")
        #header label
        labels_list[0].place(x = 430,y = 20)
        #case no. label
        labels_list[1].place(x = 171,y = 104)
        self.query_result_labels[0].place(x = 270,y = 105)
        #name label
        labels_list[2].place(x = 197,y = 150)
        self.query_result_labels[1].place(x = 270,y = 151)
        #date label
        labels_list[3].place(x = 208,y = 195)
        self.query_result_labels[2].place(x = 270,y = 196)
        #age label
        labels_list[4].place(x = 213,y = 242)
        self.query_result_labels[3].place(x = 270,y = 243)
        #gender label
        labels_list[5].place(x = 183,y = 290)
        self.query_result_labels[4].place(x = 270,y = 291)
        #disease label
        labels_list[6].place(x = 184,y = 335)
        self.query_result_labels[5].place(x = 270,y = 336)
        #symptoms label
        labels_list[7].place(x = 155,y = 382)
        self.query_result_labels[6].place(x = 270,y = 383)
        #medicines label
        labels_list[8].place(x = 160,y = 428)
        self.query_result_labels[7].place(x = 270,y = 429)
        #pathological info label
        labels_list[9].place(x = 97,y = 476)
        self.query_result_labels[8].place(x = 270,y = 475)
        #underline label
        labels_list[10].place(x = 410,y = 62)

        #creating buttons
        buttons_list = wc_obj.create_buttons(
            master = self,width = [100,100,100,100,100,100,100,100,100,100,100,100,100,30,40],
            height = [27,27,27,27,27,27,27,27,27,27,27,27,27,30,40],background = ["#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE",
            "#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE"],
            activebackground = ["#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE","#697DCE",
            "#697DCE","#697DCE","#697DCE","#697DCE"],n = 15,foreground = ["#000000","#000000","#000000","#000000","#000000","#000000","#000000",
            "#000000","#000000","#000000","#000000","#000000","#000000"],font = [("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),
            ("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),
            ("Segoe UI",14)],text = ["Update","Update","Update","Update","Update","Update","Update","Update","Details","Details","Details",
            "Details","Delete"],image = [Images.UPDATE,Images.UPDATE,Images.UPDATE,Images.UPDATE,Images.UPDATE,
            Images.UPDATE,Images.UPDATE,Images.UPDATE,Images.DETAILS,Images.DETAILS,
            Images.DETAILS,Images.DETAILS,Images.DELETE,Images.BACK,Images.PRINT],compound = [tkinter.LEFT,
            tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,tkinter.LEFT,
            tkinter.LEFT]
        )
        #update name button
        buttons_list[0].configure(command = self.update_Name)
        buttons_list[0].place(x = 938,y = 153)
        #update date button
        buttons_list[1].configure(command = self.update_Date)
        buttons_list[1].place(x = 938,y = 200)
        #update age button
        buttons_list[2].configure(command = self.update_Age)
        buttons_list[2].place(x = 938,y = 247)
        #update gender button
        buttons_list[3].configure(command = self.update_Gender)
        buttons_list[3].place(x = 938,y = 292)
        #update disease button
        buttons_list[4].configure(command = self.update_Disease)
        buttons_list[4].place(x = 938,y = 338)
        #update symptoms button
        buttons_list[5].configure(command = self.update_Symptoms)
        buttons_list[5].place(x = 938,y = 386)
        #update medicines button
        buttons_list[6].configure(command = self.update_Medicines)
        buttons_list[6].place(x = 938,y = 433)
        #update pathological info button
        buttons_list[7].configure(command = self.update_pathological_info)
        buttons_list[7].place(x = 938,y = 480)
        #disease details button
        buttons_list[8].configure(command = self.disease_details)
        buttons_list[8].place(x = 793,y = 339)
        #symptoms details button
        buttons_list[9].configure(command = self.symptoms_details)
        buttons_list[9].place(x = 793,y = 386)
        #medicines detail button
        buttons_list[10].configure(command = self.medicines_details)
        buttons_list[10].place(x = 793,y = 433)
        #pathological info deatils button
        buttons_list[11].configure(command = self.pathological_details)
        buttons_list[11].place(x = 793,y = 480)
        #delete button
        buttons_list[12].configure(command = self.delete_data)
        buttons_list[12].place(x = 525,y = 549)
        #back button
        buttons_list[13].configure(command = self.back)
        buttons_list[13].place(x = 5,y = 12)
        #print button
        buttons_list[14].configure(command = self.print)
        buttons_list[14].place(x = 3,y = 60)
    
    def update_Name(self):
        name_dialog_object = dialog_box(
            parent = self,label_text = ["Name : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Name",update_case_no = self.query_result[0][0]
        )
        if(name_dialog_object.Update!=None):
            self.query_result_labels[1].configure(text = name_dialog_object.Update)
    
    def update_Date(self):
        date_dialog_object = dialog_box(
            parent = self,label_text = ["Date : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Date",update_case_no = self.query_result[0][0]
        )
        if(date_dialog_object.Update!=None):
            self.query_result_labels[2].configure(text = date_dialog_object.Update)
    
    def update_Age(self):
        age_dialog_object = dialog_box(
            parent = self,label_text = ["Age : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Age",update_case_no = self.query_result[0][0]
        )
        if(age_dialog_object.Update!=None):
            self.query_result_labels[3].configure(text = age_dialog_object.Update)
    
    def update_Gender(self):
        gender_dialog_object = dialog_box(
            parent = self,label_text = ["Gender : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Gender",update_case_no = self.query_result[0][0]
        )
        if(gender_dialog_object.Update!=None):
            self.query_result_labels[4].configure(text = gender_dialog_object.Update)
    
    def update_Disease(self):
        disease_dialog_object = dialog_box(
            parent = self,label_text = ["Disease : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Disease",update_case_no = self.query_result[0][0]
        )
        if(disease_dialog_object.Update!=None):
            self.query_result_labels[5].configure(text = disease_dialog_object.Update)
    
    def update_Symptoms(self):
        symptoms_dialog_object = dialog_box(
            parent = self,label_text = ["Symptoms : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Symptoms",update_case_no = self.query_result[0][0]
        )
        if(symptoms_dialog_object.Update!=None):
            self.query_result_labels[6].configure(text = symptoms_dialog_object.Update[:10]+"...")
    
    def update_Medicines(self):
        medicines_dialog_object = dialog_box(
            parent = self,label_text = ["Medicines : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Medicines",update_case_no = self.query_result[0][0]
        )
        if(medicines_dialog_object.Update!=None):
            self.query_result_labels[7].configure(text = medicines_dialog_object.Update[:10]+"...")
    
    def update_pathological_info(self):
        pathological_info_dialog_object = dialog_box(
            parent = self,label_text = ["Pathological Info : "],button_text = ["Update"],compound_image = [Images.UPDATE],
            title = "Update Pathological Information",update_case_no = self.query_result[0][0]
        )
        if(pathological_info_dialog_object.Update!=None):
            self.query_result_labels[8].configure(text = pathological_info_dialog_object.Update[:10]+"...")
    
    def disease_details(self):
        self.destroy()
        detailsWindow("Disease Details",self.query_result[0][0])
    
    def symptoms_details(self):
        self.destroy()
        detailsWindow("Symptoms Details",self.query_result[0][0])
    
    def medicines_details(self):
        self.destroy()
        detailsWindow("Medicines Details",self.query_result[0][0])
    
    def pathological_details(self):
        self.destroy()
        detailsWindow("Pathological Details",self.query_result[0][0])

    def back(self):
        self.destroy()
        if(self.window_name!=None):
            db_conn = sqlite3.connect(self.backend_obj.documents_folder_path+"/Doc Manager/patient.db")
            if(self.window_name=="All Cases"):
                deleteAllWindow("All Cases",db_conn.execute(self.backend_obj.db_constants.get_all_data).fetchall())
            elif(self.window_name=="Total Cases"):
                deleteAllWindow("Total Cases",db_conn.execute(self.backend_obj.db_constants.get_data_by_name % self.patient_name).fetchall())
            db_conn.close()
        else:
            prescriptionWindow()
    
    def print(self):
        cn = canvas.Canvas(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.query_result[0][0])+"/prescription.pdf",pagesize=A4)
        cn.setFont("Helvetica",40)
        cn.drawCentredString(x = 300,y = 795,text = "Bhati Hospital")
        cn.drawImage(Images.LINE,x = 25,y = 770)
        cn.setFontSize(size = 14)
        cn.drawString(x = 40,y = 750,text = "Dr.Chandresh Arora(PT)")
        cn.drawString(x = 40,y = 730,text = "H.O.D Physiotherapy Department,Bhatia Hospital")
        cn.drawString(x = 40,y = 710,text = "BPT,MPT(Neuro)Ph.D(Sports)MD(am),")
        cn.drawString(x = 40,y = 690,text = "CPTDM(Neuro & Sports),CHW,CPHY,MIAP,MIAFT,Aerobics,")
        cn.drawString(x = 40,y = 670,text = "Pilates & Plyometric Power Yoga,Swiss Ball,Thera Band Exr.Instructor")
        cn.drawString(x = 40,y = 650,text = "Physical Therapist & Fitness Expert")
        cn.setFontSize(size = 18)
        cn.drawString(x = 40,y = 630,text = "Call : 0141-4922569, 99299 92997")
        cn.drawString(x = 40,y = 610,text = "Email : arora.physio@yahoo.com")
        cn.drawString(x = 40,y = 590,text = "whatsapp : 98291 88899")
        cn.drawImage(Images.LINE,x = 25,y = 570)
        cn.setFontSize(size = 12)
        cn.drawString(x = 10,y = 550,text = "Facilities : ")
        cn.drawString(x = 10,y = 530,text = "1-SWD,IFT,TENS")
        cn.drawString(x = 10,y = 510,text = "2-Ultrasound,IRR,Traction")
        cn.drawString(x = 10,y = 490,text = "3-WAX/HYDRO Collatral")
        cn.drawString(x = 10,y = 470,text = "4-Body Massager")
        cn.drawString(x = 10,y = 450,text = "5-Cranial Nerve Stimulator")
        cn.drawString(x = 10,y = 430,text = "6-Muscle Stimulator")
        cn.drawString(x = 10,y = 410,text = "7-Vaccum")
        cn.drawString(x = 10,y = 390,text = "8-Deep Heat")
        cn.drawString(x = 10,y = 370,text = "9-Body Shaper")
        cn.drawString(x = 10,y = 350,text = "10-Cavitation")
        cn.drawString(x = 10,y = 330,text = "11-Laser/Long wave")
        cn.drawString(x = 10,y = 310,text = "12-BRT/MRT")
        cn.drawImage(Images.LINE_VERTICAL,x =  160,y = 310)
        cn.drawImage(Images.LINE_HORIZONTAL,x = 10,y = 300)
        cn.drawString(x = 170,y = 553,text = "Case No : "+str(self.query_result[0][0]))
        cn.drawString(x = 270,y = 553,text = "Name : "+self.query_result[0][1])
        cn.drawString(x = 460,y = 553,text = "Date : "+str(self.query_result[0][2]))
        cn.drawString(x = 170,y = 535,text = "Age : "+self.query_result[0][3])
        cn.drawString(x = 270,y = 535,text = "Sex : "+self.query_result[0][4])
        cn.drawString(x = 170,y = 515,text = "Disease : "+self.query_result[0][5])
        cn.drawImage(Images.LINE,x = 25,y = 60)
        cn.setFontSize(size = 10)
        cn.drawString(x = 40,y = 45,text = "Bhati Hospital")
        cn.drawString(x = 40,y = 30,text = "Near Panchwati Circle,")
        cn.drawString(x = 40,y = 15,text = "Raja Park,jaipur")
        cn.drawString(x = 190,y = 45,text = "Arora's Physiotherapy & Wellness Clinic")
        cn.drawString(x = 190,y = 30,text = "2/20,Infront of jawahar Enclave,")
        cn.drawString(x = 190,y = 15,text = "Near Bank of India,Jawahar Nagar,Jaipur")
        cn.drawString(x = 410,y = 45,text = "Janupyogi Kendra")
        cn.drawString(x = 410,y = 30,text = "Sector-4,Behind Seedling School")
        cn.drawString(x = 410,y = 15,text = "Jawahar Nagar,Jaipur")
        cn.save()
        webbrowser.open_new(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.query_result[0][0])+"/prescription.pdf")
    # def print(self):
    #     f_open = open(self.backend_obj.documents_folder_path+"/Doc Manager/information.dat",'r')
    #     information_list = f_open.readlines()
    #     if(information_list.count(information_list[8])>1):
    #         for i in range(information_list.count(information_list[8])-1):
    #             del(information_list[8])
    #     cn = canvas.Canvas(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.query_result[0][0])+"/prescription.pdf",pagesize = A4)
    #     cn.setFont("Helvetica",40)
    #     cn.drawCentredString(x = 300,y = 795,text = information_list[0][:information_list[0].index("\n")])
    #     cn.drawImage(Images.LINE,x = 25,y = 770,mask = "auto")
    #     cn.setFontSize(size = 14)
    #     y = 750
    #     for i in range(1,5):
    #         cn.drawString(x = 40,y = y,text = information_list[i][:information_list[i].index("\n")])
    #         if(i+4==8):
    #             cn.drawString(x = 420,y = y,text = information_list[8][:information_list[8].index("\n")]+"-"+information_list[10][:information_list[10].index("\n")])
    #         else:
    #             cn.drawString(x = 420,y = y,text = information_list[i+4][:information_list[i+4].index("\n")])
    #         y-=20
    #     cn.drawImage(Images.LINE,x = 25,y = 670)
    #     cn.drawString(x = 40,y = 650,text = "Case No : "+str(self.query_result[0][0]))
    #     cn.drawString(x = 160,y = 650,text = "Name : "+self.query_result[0][1])
    #     cn.drawString(x = 390,y = 650,text = "Date : "+self.query_result[0][2])
    #     cn.drawString(x = 500,y = 650,text = "Age : "+str(self.query_result[0][3]))
    #     cn.drawString(x = 40,y = 630,text = "Gender : "+self.query_result[0][4])
    #     cn.drawString(x = 40,y = 600,text = "Disease : "+self.query_result[0][5])
    #     cn.drawString(x = 40,y = 480,text = "Symptoms : "+self.query_result[0][6])
    #     cn.drawString(x = 40,y = 360,text= "Medicines : "+self.query_result[0][7])
    #     cn.drawString(x = 40,y = 240,text = "Pathological Info : "+self.query_result[0][8])
    #     cn.drawImage(Images.LINE,x = 25,y = 60,mask = "auto")
    #     cn.drawString(x = 40,y = 30,text = "Timing : Morning - "+information_list[11][:information_list[11].index(",")])
    #     cn.drawString(x = 94,y = 10,text = "Evening - "+information_list[12][:information_list[12].index("\n")])
    #     cn.save()
    #     webbrowser.open_new(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.query_result[0][0])+"/prescription.pdf")
    
    def delete_data(self):
        delete_message_object = message_dialog(
            parent = self,text = "Are you sure you want to delete",title = "Confirmation",n = 2,button_text = ["OK","Cancel"],
            compound_image = [Images.OK,Images.CANCEL]
        )
        if(delete_message_object.event=="ok button clicked"):
            obj = backend.patientWindowBackendFunction()
            query_object = backend.database_query_constants()
            db_connection = sqlite3.connect(obj.documents_folder_path+"/Doc Manager/patient.db")
            db_connection.execute(query_object.delete_data % self.query_result[0][0])
            db_connection.commit()
            db_connection.close()
            shutil.rmtree(obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.query_result[0][0]))
            message_dialog(
                parent = self,text = "Deleted Successfully",title = "Delete Notification",n = 1,button_text = ["OK"],
                compound_image = [Images.OK]
            )
            self.destroy()
            prescriptionWindow()

#this is details window class
class detailsWindow(tkinter.Tk):
    def __init__(self,header_label_text,case_no):
        super().__init__()
        self.geometry("1100x600+200+60")
        self.configure(bg = "#EFE4E4")
        self.title("Doc Manager")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.header_label_text = header_label_text
        self.text_box = None
        self.state = None
        self.case_no = case_no
        self.backend_obj = backend.detailsWindowBackendFunction()
        self.is_saved_button_pressed = 0
        self.widget_Assembler()
    
    def widget_Assembler(self):
        side_frame = tkinter.Frame(
            master = self,width = 50,height = 600,bg = "#697DCE",bd = 0
        )
        side_frame.pack(side = tkinter.LEFT)
        wc_obj = widget_creater()
        #creating labels
        labels_list = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4"],n = 2,font = [("Segoe UI",20,"italic")],
            foreground = ["#7E785F"],text = [self.header_label_text],image = [Images.UNDERLINE]
        )
        #header label
        labels_list[0].place(x = 460,y = 20)
        #underline label
        labels_list[1].place(x = 405,y = 70)

        #creating text box
        self.text_box = wc_obj.create_text_box(
            master = self,width = 100,height = 19,background = "#ffffff",insertbackground = "#000000",
            font = ("Segoe UI",14),n = 1
        )
        self.text_box[0].place(x = 75,y = 100)
        self.text_box[0].focus_set()
        self.display_patient_data()
        self.text_box[0].configure(state = tkinter.DISABLED)
        #creating frame buttons
        buttons_list = wc_obj.create_buttons(
            master = side_frame,width = [30,30,30],height = [30,30,30],background = ["#697DCE","#697DCE","#697DCE"],
            activebackground = ["#697DCE","#697DCE","#697DCE"],n = 3,image = [Images.BACK,Images.EDIT,Images.SAVE]
        )
        #back button
        buttons_list[0].configure(command = self.back)
        buttons_list[0].place(x = 10,y = 10)
        #edit button
        buttons_list[1].configure(command = self.edit_data)
        buttons_list[1].place(x = 10,y = 49)
        #save button
        buttons_list[2].configure(command = self.save)
        buttons_list[2].place(x = 10,y = 90)
    
    def display_patient_data(self):
        patient_file = None
        if(self.header_label_text=="Medicines Details"):
            patient_file = open(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.case_no)+"/Medicines.txt","r")
        elif(self.header_label_text=="Symptoms Details"):
            patient_file = open(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.case_no)+"/Symptoms.txt","r")
        elif(self.header_label_text=="Disease Details"):
            patient_file = open(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.case_no)+"/Disease.txt","r")
        elif(self.header_label_text=="Pathological Details"):
            patient_file = open(self.backend_obj.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.case_no)+"/Pathological Information.txt","r")
        self.text_box[0].insert(tkinter.END,patient_file.read())
        patient_file.close()
    
    def back(self):
        if(self.is_saved_button_pressed==0):
            if(self.state == tkinter.NORMAL):
                message_dialog_obj = message_dialog(
                    parent = self,text = "Do you want to save changes?",title = "Save Changes",n = 2,button_text = ["OK","cancel"],
                    compound_image = [Images.OK,Images.CANCEL]
                )
                if(message_dialog_obj.event=="ok button clicked"):
                    self.backend_obj.save_data(self.text_box[0],self.header_label_text[:self.header_label_text.index(" ")],self.case_no)
        self.destroy()
        db_connection = sqlite3.connect(self.backend_obj.documents_folder_path+"/Doc Manager/patient.db")
        query_constants = backend.database_query_constants()
        patient_data = db_connection.execute(query_constants.get_data_by_case_no % self.case_no).fetchall()
        db_connection.close()
        patientInformation(patient_data)
    
    def save(self):
        self.backend_obj.save_data(self.text_box[0],self.header_label_text[:self.header_label_text.index(" ")],self.case_no)
        message_dialog(
            parent = self,text = "Saved Successfully",title = "Save Notification",n = 1,button_text = ["OK"],
            compound_image = [Images.OK]
        )
        self.is_saved_button_pressed = 1

    def edit_data(self):
        self.text_box[0].configure(state = tkinter.NORMAL)
        self.state = tkinter.NORMAL

class deleteAllWindow(tkinter.Tk):
    def __init__(self,header_label_text,query_result):
        super().__init__()
        self.geometry("1100x600+200+60")
        self.configure(bg = "#EFE4E4")
        self.title("Doc Manager")
        self.resizable(width = False,height = False)
        self.iconbitmap(Images.ICON)
        self.header_label_text = header_label_text
        self.canvas = None
        self.query_result = query_result
        self.widget_Assembler()
    
    def widget_Assembler(self):
        side_frame = tkinter.Frame(
            master = self,width = 50,height = 600,bg = "#697DCE",bd = 0
        )
        side_frame.pack(side = tkinter.LEFT)
        wc_obj = widget_creater()
        #creating buttons
        button_list = wc_obj.create_buttons(
            master = self,width = [30],height = [30],background = ["#697DCE"],
            activebackground = ["#697DCE"],n = 1,foreground = ["#000000"],
            image = [Images.BACK]
        )
        #back button
        button_list[0].configure(command = self.back_function)
        button_list[0].place(x = 8,y = 10)

        #creating labels
        labels_list = wc_obj.create_labels(
            master = self,background = ["#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4","#EFE4E4"],n = 6,
            font = [("Segoe UI",25,"italic"),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14),("Segoe UI",14)],
            foreground = ["#7E785F","#000000","#000000","#000000","#000000"],text = [self.header_label_text,"Case No.","Name","Date","Disease"],
            image = [Images.UNDERLINE]
        )
        #header label
        if(self.header_label_text=="All Cases"):
            labels_list[0].place(x = 500,y = 15)
        elif(self.header_label_text=="Total Cases"):
            labels_list[0].place(x = 492,y = 15)
        #case no. label
        labels_list[1].place(x = 100,y = 110)
        #name label
        labels_list[2].place(x = 300,y = 110)
        #Date label
        labels_list[3].place(x = 500,y = 111)
        #Disease label
        labels_list[4].place(x = 670,y = 111)
        #underline label
        labels_list[5].place(x = 420,y =65)
        container_frame = tkinter.Frame(
            master = self,bg = "#FFFFFF",highlightthickness = 2
        )
        container_frame.place(x = 60,y = 140)
        self.canvas = tkinter.Canvas(
            master = container_frame,width = 1000,height = 450,bg = "#FFFFFF"
        )
        self.canvas.pack(side = tkinter.LEFT,expand = True,fill = tkinter.BOTH)
        scroll = tkinter.Scrollbar(
            master = container_frame,orient = tkinter.VERTICAL,command = self.canvas.yview
        )
        scroll.pack(side = tkinter.RIGHT,expand = False,fill = tkinter.Y)
        self.canvas.bind_all("<MouseWheel>",self.onMouseWheel)
        frame_y_coordinate = 28
        if(self.header_label_text=="All Cases"):
            delete_all_button = MyButton(
                root = self,parent = self,text = "Delete All",image = Images.DELETE
            )
            delete_all_button.place(x = 910,y = 70)
            for i in self.query_result:
                frame = tkinter.Frame(
                    master = self.canvas,bg = "#FFFFFF",highlightthickness = 2,highlightbackground = "#40414B"
                )
                var = tkinter.IntVar()
                checkButton = myCheckButton(
                    parent = frame,case_no = i[0],delete_all_button_ref = delete_all_button,var = var
                )
                checkButton.place(x = 10,y = 7)
                label_info_list = wc_obj.create_labels(
                    master = frame,background = ["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF"],n = 4,font = [("Segoe UI",12),("Segoe UI",12),("Segoe UI",12),("Segoe UI",12)],
                    foreground = ["#000000","#000000","#000000","#000000"],text = [str(i[0]),i[1],i[2],i[5]]
                )
                label_info_list[0].place(x = 55,y = 5)
                label_info_list[1].place(x = 180,y = 5)
                label_info_list[2].place(x = 410,y = 5)
                if(len(label_info_list[3].cget("text"))>15):
                    label_info_list[3].configure(text = label_info_list[3].cget("text")[:10])
                label_info_list[3].place(x = 585,y = 5)
                view_button = MyButton(
                    root = self,parent = frame,case_no = i[0],text = "View",image = Images.VIEW,
                    window_name = "All Cases"
                )
                view_button.pack(side = tkinter.RIGHT,padx = 10,pady = 5)
                self.canvas.create_window(500,frame_y_coordinate,window = frame,width = 960,height = 45)
                frame_y_coordinate += 50
        elif(self.header_label_text=="Total Cases"):
            for i in self.query_result:
                frame = tkinter.Frame(
                    master = self.canvas,bg = "#ffffff",highlightthickness = 2,highlightbackground = "#40414B"
                )
                label_info_list = wc_obj.create_labels(
                    master = frame,background = ["#ffffff","#ffffff","#ffffff","#ffffff"],n = 4,
                    font = [("Segoe UI",12),("Segoe UI",12),("Segoe UI",12),("Segoe UI",12)],
                    foreground = ["#000000","#000000","#000000","#000000"],text = [str(i[0]),i[1],i[2],i[5]]
                )
                label_info_list[0].place(x = 55,y = 5)
                label_info_list[1].place(x = 180,y = 5)
                label_info_list[2].place(x = 410,y = 5)
                if(len(label_info_list[3].cget("text"))>15):
                    label_info_list[3].configure(text = label_info_list[3].cget("text")[:10])
                label_info_list[3].place(x = 585,y = 5)
                view_button = MyButton(
                    root = self,parent = frame,case_no = i[0],text = "View",image = Images.VIEW,
                    window_name = "Total Cases",patient_name = i[1]
                )
                view_button.pack(side = tkinter.RIGHT,padx = 10,pady = 5)
                self.canvas.create_window(500,frame_y_coordinate,window = frame,width = 960,height = 45)
                frame_y_coordinate += 50
        self.canvas.configure(yscrollcommand = scroll.set,scrollregion = (0,0,0,frame_y_coordinate-20,))
        frame_y_coordinate = 0
    
    def back_function(self):
        self.destroy()
        prescriptionWindow()
    
    def onMouseWheel(self,event):
        self.canvas.yview_scroll(-1*(event.delta//120),"units")

class MyButton(tkinter.Button):
    def __init__(self,root,parent,case_no = None,text = None,image = None,window_name = None,patient_name = None):
        tkinter.Button.__init__(self,master = parent,width = 120,height = 27,bg = "#5559D8",bd = 0,font = ("Segoe UI",14))
        self.root = root
        self.parent = parent
        self.window_name = window_name
        self.patient_name = patient_name
        self.case_no = case_no
        self.delete_all_list = []
        self.delete_all_frames = []
        self.query_constants = backend.database_query_constants()
        self.documents_folder_path = os.path.expanduser("~/Documents").replace("\\","/",os.path.expanduser("~/Documents").count("\\"))
        photo = tkinter.PhotoImage(file = image)
        self.configure(image = photo,text = text,compound = tkinter.LEFT)
        self.image = photo
        if(text=="Delete All"):
            self.configure(command = self.delete_All)
        elif(text=="View"):
            self.configure(command = self.view_function)
        
    def view_function(self):
        self.root.destroy()
        db_conn = sqlite3.connect(self.documents_folder_path+"/Doc Manager/patient.db")
        query = db_conn.execute(self.query_constants.get_data_by_case_no % self.case_no).fetchall()
        db_conn.close()
        if(self.window_name=="All Cases"):
            patientInformation(query,self.window_name)
        elif(self.window_name=="Total Cases"):
            patientInformation(query,self.window_name,self.patient_name)
    
    def delete_All(self):
        db_conn = sqlite3.connect(self.documents_folder_path+"/Doc Manager/patient.db")
        for i in self.delete_all_list:
            db_conn.execute(self.query_constants.delete_data % i)
            shutil.rmtree(self.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(i))
        db_conn.commit()
        db_conn.close()
        for i in self.delete_all_frames:
            i.destroy()
    
class myCheckButton(tkinter.Checkbutton):
    def __init__(self,parent,case_no,delete_all_button_ref,var):
        tkinter.Checkbutton.__init__(self,master = parent,bg = "#FFFFFF",activebackground = "#FFFFFF",command = self.create_delete_all_list,variable = var)
        self.parent = parent
        self.case_no = case_no
        self.delete_all_button_reference = delete_all_button_ref
        self.state_variable = var
    
    def create_delete_all_list(self):
        if(self.state_variable.get()):
            self.delete_all_button_reference.delete_all_list.append(self.case_no)
            self.delete_all_button_reference.delete_all_frames.append(self.parent)
        else:
            del(self.delete_all_button_reference.delete_all_list[self.delete_all_button_reference.delete_all_list.index(self.case_no)])
            del(self.delete_all_button_reference.delete_all_frames[self.delete_all_button_reference.delete_all_frames.index(self.parent)])
if __name__=="__main__":
    app_window()
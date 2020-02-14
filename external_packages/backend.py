import os
import sqlite3
import shutil
import datetime
import time

#creating class for prescription window backend function
class prescriptionWindowBackendFunction:
    def __init__(self):
        self.documents_folder_path = os.path.expanduser("~/Documents")
        self.n = self.documents_folder_path.count("\\")
        self.documents_folder_path = self.documents_folder_path.replace("\\","/",self.n)
        self.path_list = [
            "/Disease.txt","/Symptoms.txt","/Medicines.txt","/Pathological Information.txt"
        ]
        self.current_Date = datetime.datetime.now().strftime("%d/%m/%y")

    def save_Data(self,patient_data_list):
        database_query_object = database_query_constants()
        db_connection = sqlite3.connect(self.documents_folder_path+"/Doc Manager/patient.db")
        db_connection.execute(database_query_object.insert_data,patient_data_list)
        os.mkdir(self.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(patient_data_list[0]))
        for i in range(5,len(patient_data_list)):
            f = open(self.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(patient_data_list[0])+self.path_list[i-5],"w")
            f.write(self.current_Date+" : "+patient_data_list[i])
            f.close()
        db_connection.commit()
        db_connection.close()
        return patient_data_list[0]

#creating class for patient information window backend
class patientWindowBackendFunction:
    def __init__(self):
        self.documents_folder_path = os.path.expanduser("~/Documents")
        self.n = self.documents_folder_path.count("\\")
        self.documents_folder_path = self.documents_folder_path.replace("\\","/",self.n)
        self.path_list = [
            "/Disease.txt","/Medicines.txt","/Symptoms.txt","/Pathological Information.txt","/Age.txt","/Gender.txt"
        ]
        self.current_Date = datetime.datetime.now().strftime("%d/%m/%y")
        self.db_constants = database_query_constants()

class detailsWindowBackendFunction:
    def __init__(self):
        self.documents_folder_path = os.path.expanduser("~/Documents")
        self.n = self.documents_folder_path.count("\\")
        self.documents_folder_path = self.documents_folder_path.replace("\\","/",self.n)
        self.case_no = None
    
    def save_data(self,txt_box_ref,file_name,case_no):
        self.case_no = case_no
        if(file_name=="Pathological"):
            file_name = "Pathological Information"
        f_open  = open(self.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(case_no)+"/"+file_name+".txt","w")
        f_open.write(txt_box_ref.get("1.0","end-1c"))
        f_open.close()
        self.pre_process_file(file_name)
    
    def pre_process_file(self,f_name):
        f_open = open(self.documents_folder_path+"/Doc Manager/Patient Data/Case No."+str(self.case_no)+"/"+f_name+".txt","r")
        data = f_open.readlines()
        f_open.close()
        latest_info = data[len(data)-1]
        if(f_name=="Disease"):
            self.update_database("disease",latest_info[latest_info.index(":")+2:])
        elif(f_name=="Medicines"):
            self.update_database("medicines",latest_info[latest_info.index(":")+2:])
        elif(f_name=="Symptoms"):
            self.update_database("symptoms",latest_info[latest_info.index(":")+2:])
        elif(f_name=="Pathological Information"):
            self.update_database("pathological_info",latest_info[latest_info.index(":")+2:])
        elif(f_name=="Age"):
            self.update_database("age",latest_info[latest_info.index(":")+2:])
        elif(f_name=="Gender"):
            self.update_database("gender",latest_info[latest_info.index(":")+2:])
    
    def update_database(self,column_name,column_value):
        db_connect = sqlite3.connect(self.documents_folder_path+"/Doc Manager/patient.db")
        db_connect.execute("UPDATE patient_info SET "+column_name+" = '%s' WHERE case_no = '%d';" % (column_value,self.case_no))
        db_connect.commit()
        db_connect.close()

#doctor's information window backend function class
class doctors_Information_Window_Backend:
    def __init__(self):
        self.documents_folder_path = os.path.expanduser("~/Documents")
        self.documents_folder_path = self.documents_folder_path.replace("\\","/",self.documents_folder_path.count("\\"))
    
    def save_doctors_data(self,information_list):
        print(information_list)
        db_connection = None
        database_query_object = database_query_constants()
        if(not os.path.isdir(self.documents_folder_path+"/Doc Manager")):
            os.mkdir(self.documents_folder_path+"/Doc Manager")
            os.mkdir(self.documents_folder_path+"/Doc Manager/Patient Data")
            db_connection = sqlite3.connect(self.documents_folder_path+"/Doc Manager/patient.db")
            db_connection.execute(database_query_object.create_table)
        f_open = open(self.documents_folder_path+"/Doc Manager/information.dat",'w')
        for i in information_list:
            f_open.write(i+"\n")
        f_open.close()

#creating class for accessing database and performing query
class database_query_constants:
    def __init__(self):
        self.create_table = "CREATE TABLE patient_info(case_no INTEGER PRIMARY KEY,name TEXT NOT NULL,date TEXT NOT NULL,age TEXT NOT NULL,gender TEXT NOT NULL,disease TEXT NOT NULL,symptoms TEXT NOT NULL,medicines TEXT NOT NULL,pathological_info TEXT NOT NULL);"
        self.insert_data = "INSERT INTO patient_info(case_no,name,date,age,gender,disease,symptoms,medicines,pathological_info)VALUES(?,?,?,?,?,?,?,?,?);"
        self.update_name = "UPDATE patient_info SET name = '%s' WHERE case_no = '%d';"
        self.update_date = "UPDATE patient_info SET date = '%s' WHERE case_no = '%d';"
        self.update_age = "UPDATE patient_info SET age = '%d' WHERE case_no = '%d';"
        self.update_gender = "UPDATE patient_info SET gender = '%s' WHERE case_no = '%d';"
        self.update_disease = "UPDATE patient_info SET disease = '%s' WHERE case_no = '%d';"
        self.update_symptoms = "UPDATE patient_info SET symptoms = '%s' WHERE case_no = '%d';"
        self.update_medicines = "UPDATE patient_info SET medicines = '%s' WHERE case_no = '%d';"
        self.update_pathological_info = "UPDATE patient_info SET pathological_info = '%s' WHERE case_no = '%d';"
        self.get_data_by_case_no = "SELECT case_no,name,date,age,gender,disease,symptoms,medicines,pathological_info FROM patient_info WHERE case_no = '%d';"
        self.get_data_by_name = "SELECT case_no,name,date,age,gender,disease,symptoms,medicines,pathological_info FROM patient_info WHERE name = '%s' COLLATE NOCASE;"
        self.delete_data = "DELETE FROM patient_info WHERE case_no = '%d';"
        self.get_case_no = "SELECT max(case_no) FROM patient_info;"
        self.get_all_data = "SELECT * FROM patient_info;"
import pymongo
import re
import pandas as pd
from datetime import datetime

#Establishing Connections
client = pymongo.MongoClient("mongodb+srv://ajay96:1234@cluster0.7phm1vl.mongodb.net/?retryWrites=true&w=majority")
db = client.LibraryManagementSystem
stud_details = db.studentDetails
bookrec = db.bookRecords
studissued = db.issuedRenewedDetails

#Student Login & Functionalities
def studlogin():
  print("Student Login")
  phone = input("Enter your Phone No : ")
  password = input("Enter your password : ")
  lst = []
  if stud_details.find_one({"PhoneNumber" : phone, "Password":password}):
    print("Login Successfull !")
    print("Perform the following Functionalities :")
    studopt = input("1. Search for Books\n2. Your Library History\n")
    if studopt == "1":
      bookname = input("Name of the book : ")
      find = list(bookrec.find({"Title":bookname, "status":"Stock"}))
      if len(find) != 0:
        for x in bookrec.find({"Title":bookname, "status":"Stock"}):
          print(x)
      else:
        print("The book you are searching is currently unavailable")
    elif studopt == "2":
      for x in studissued.find({"PhoneNo":phone}, {"_id":0, "Title":1, "DateOfIssue":1, "RenewalDate":1, "Penalty":1}):
        lst.append(x)
      lst = pd.DataFrame(lst)
      print(lst)
  else:
      print("Invalid Login")

#Penalty calculating function
def penaltycalculate(startdate1, enddate1):
  print(startdate1)
  daydiff = (enddate1 - startdate1).days
  print(daydiff)
  if daydiff > 15:
      penaltyDiff = daydiff - 15
      penalty = penaltyDiff * 5
      return penalty
  return 0  

#Functionalities of Admin
def admin_func():
  adminoption = input("What action do you want to perform?\n1. Add Book\n2. Delete existing books\n3. Issue Book\n4. Receive or Renew Book\n5. Display list of Issued Books\n6. Display list of Books\n")
  #Adding a new book
  if adminoption == "1":
    print("Enter Book Details: ")
    book_title = input("Enter the title of the Book: ")
    author_name = input("Enter the Author Name: ")
    pattern = "^[0-9]{5}$"
    isbn_no = input("Enter ISBN no: ")
    bookrec.insert_one({"_id":isbn_no, "Title" : book_title, "AuthorName" : author_name, "status":"Stock"})
    for x in bookrec.find():
      print(x)
    if re.match(pattern, isbn_no):
      print("Book added successfully!")
    else:
      print("ISBN number length should be 5")
      bookrec.delete_one({"_id":isbn_no})
  #Deleting a book
  elif adminoption == "2":
    print("Delete a book")
    isbn1 = input("Enter the ISBN no of the book to delete : ")
    if bookrec.find({"_id" : isbn1}):
      bookrec.delete_one({"_id":isbn1})
      print("Book has been deleted successfully")
    else:
      print("Enter a valid ISBN number")
  #Issueing a book
  elif adminoption == "3":
    print("Issue Book")
    date1 = datetime.now()
    isbn2 = input("ISBN No : ")
    phone_no = input("Phone No. of Student : ")
    bookrecord = bookrec.find_one_and_update({"_id" : isbn2}, {"$set": {"status" : "Issued"}})
    studissued.insert_one({"_id":isbn2, "DateOfIssue":date1, "Penalty" : 0, "PhoneNo":phone_no, "Title":bookrecord["Title"]})
    print("Book Issued!")
  #Receive or Renew a Book
  elif adminoption == "4":
    print("Receive or Renew Book")
    option1 = input("Enter the following options to proceed : \n1.Receive\n2.Renew\n")
    isbn2 = input("ISBN No : ")
    phone_no = input("Phone No. of Student : ")
    date1 = studissued.find_one({"_id":isbn2})
    print(date1)
    if option1 =="1":
      print("Receive")
      bookrec.find_one_and_update({"_id" : isbn2}, {"$set": {"status" : "Stock"}})
      if "RenewalDate" in date1:
        if (date1["RenewalDate"] - datetime.now()).days > 15:
          total_penalty = penaltycalculate(date1["RenewalDate"], datetime.now()) + date1["Penalty"]
          studissued.find_one_and_update({"_id":isbn2}, {"$set": {"Penalty" : total_penalty}})
          bookrec.find_one_and_update({"_id" : isbn2}, {"$set": {"status" : "Stock"}})
        else:
          bookrec.find_one_and_update({"_id" : isbn2}, {"$set": {"status" : "Stock"}})
      else:
        total_penalty = penaltycalculate(date1["DateOfIssue"], datetime.now()) + date1["Penalty"]
        studissued.find_one_and_update({"_id":isbn2}, {"$set": {"Penalty" : total_penalty}})
        bookrec.find_one_and_update({"_id" : isbn2}, {"$set": {"status" : "Stock"}})
      print("Book has been received!")

    elif option1 == "2":
      print("Renew")
      if "RenewalDate" in date1:
        if (date1["RenewalDate"] - datetime.now()).days > 15:
          total_penalty = penaltycalculate(date1["RenewalDate"], datetime.now()) + date1["Penalty"]
          studissued.find_one_and_update({"_id":isbn2}, {"$set": {"Penalty" : total_penalty, "RenewalDate":datetime.now()}})
        else:
          total_penalty = penaltycalculate(date1["DateOfIssue"], datetime.now()) + date1["Penalty"]
          studissued.find_one_and_update({"_id":isbn2}, {"$set": {"Penalty" : total_penalty, "RenewalDate":datetime.now()}})
      else:
        total_penalty = penaltycalculate(date1["DateOfIssue"], datetime.now()) + date1["Penalty"]
        studissued.find_one_and_update({"_id":isbn2}, {"$set": {"Penalty" : total_penalty, "RenewalDate" : datetime.now()}})
      print("Book Renewed!")
  #Display Issued Books
  elif adminoption == "5":
    print("Display Books Issued")
    for x in bookrec.find({"status":"Issued"}):
      print(x)
  #Display Available Books
  elif adminoption == "6":
    print("Display Books")
    for x in bookrec.find({"status":"Stock"}):
      print(x)
  else:
    print("Invalid Option")

#Admin Login Function
def adminlogin():
  user1 = input("Enter login name : ")
  password1 = input("Enter password : ")
  if user1 == "admin":
    if password1 == "admin":
      print("Admin Login Successful")
      admin_func()
    else:
      print("Password invalid!")
  else:
    print("Invalid username!")

#General Login Function
def login():
  log = input("1. Student Login\n2. Admin Login\n")
  if log == "1":
    studlogin()
  else:
    adminlogin()

#Student Register Function
def register():
  print("Student Registeration")
  name = input("Enter Name : ")
  rollno = input("Enter RollNo : ")
  department = input("Enter Department Name : ")
  phonenum = input("Enter Phone Num : ")
  mail = input("Enter your mail id : ")
  password = input("Enter Password : ")
  stud_details.insert_one({"Name" : name, "rollno" : rollno, "Department" : department, "PhoneNumber" : phonenum, "Email" :mail, "Password" : password})
  print("User registered successfully!")

print("-------Library Management System-------")
n = int(input("1. Login\n2. Register\n"))
if n == 1:
  login()
elif n == 2:
  register()
else:
  print("Invalid Option")
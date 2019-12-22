from mongoengine import *
import re

connect('test4')

#MongoDB document mapper

#Defining regex that will be used for verification during saving these objects
valid_name = re.compile('[^\s^\d]+(\d+)?')
valid_class = re.compile('^[A-Z]{3}[1-4][A-Z]R?-\d{2}')
valid_date = re.compile('^\d{8}')

#Defining validation methods
def check_unique_date(val):
   unique_days = []
   for day in val:
       for unique_day in unique_days:
           if day.date == unique_day:
               raise NotUniqueError("Date is not unique")
       unique_days.append(day.date)

def check_unique_class(val):
    unique_classes = []
    for classroom in val:
        for unique_class in unique_classes:
            if classroom.class_code == unique_class:
                raise NotUniqueError("Class is not unique")
        unique_classes.append(classroom.class_code)


#Models
class Student(EmbeddedDocument):
   id = StringField(required=True, regex=valid_name)
   first_name = StringField(required=True)
   last_name = StringField(required=True)
   attendance = BooleanField()

class Day(EmbeddedDocument):
   date = StringField(required=True, regex=valid_date)
   day_attendance = EmbeddedDocumentListField(Student, required=True)

class Group(EmbeddedDocument):
   groupName = StringField(required=True, regex=valid_class)
   allMembers = EmbeddedDocumentListField(Student)
   calendar = EmbeddedDocumentListField(Day, validation=check_unique_date)

class User(Document):
   username = StringField(required=True, unique=True)
   password = StringField(required=True)
   authenticated = BooleanField(default=False)
   groups = EmbeddedDocumentListField(Group, validation=check_unique_class)

   def is_active(self):
       return True

   def get_id(self):
        return self.username

   def is_authenticated(self):
        return self.authenticated

   def is_anonymous(self):
       return False

   def get_classes(self):
       return self.groups

   def logout(self):
       self.authenticated = False

#helper functions
def class_search(class_code, user):
   search_class = None
   for classroom in user.classes:
           if classroom.class_code == class_code:
               search_class = classroom
               return search_class
   return None

def user_search(username):
    for user in User.objects:
        if user.username == username:
            return user
    return None

#case insensitive user search
def user_search_i(username):
    for user in User.objects:
        if user.username.lower() == username.lower():
            return user
    return None

###Manipulate db with functions below###

def printDb():
   for user in User.objects:
       print(user.username, user.password, user.is_authenticated())
       for classroom in user.classes:
           print(classroom.class_code)
           for student in classroom.class_list:
               print(student.id)
           for day in classroom.calendar:
               print(day.date)
               for attending_student in day.day_attendance:
                   print(attending_student.id, attending_student.attendance)

def registerUser(username, password):

   new_user = User(username=username, password=password)
   try:
        new_user.save()
   except NotUniqueError

def authenticate(username, password):
   user = user_search_i(username)
   if not user:
       return None
   if password == user.password:
       user.authenticated = True
       user.save()
       return user
   else:
       return None

def addStudent(first, last, class_code, user):
   def addStudentToClass():
       enrolled_class = class_search(class_code, user)
       if not enrolled_class:
           return "Fail"

       #Find number of students with same first last names and set student unique number if duplicates are found
       firstlast = (first + last).lower()
       num_student_duplicates = 0
       for student in enrolled_class.class_list:
           print(student)
           is_student_duplicate = re.search(firstlast+'(\d+)?', student.id)
           if is_student_duplicate:
               if is_student_duplicate.group(1):
                   if int(is_student_duplicate.group(1)) >= num_student_duplicates:
                       num_student_duplicates = int(is_student_duplicate.group(1))+1
               else:
                   if num_student_duplicates == 0:
                       num_student_duplicates = 1

       if num_student_duplicates != 0:
           new_student = Student(id=firstlast+str(num_student_duplicates), first_name = first, last_name = last)
       else:
           new_student = Student(id=firstlast, first_name = first, last_name = last)

       enrolled_class.class_list.append(new_student)
       print(enrolled_class.class_list)
       user.save()

   try:
       addStudentToClass()
   except DoesNotExist:
       print('No matching class code')
   except NotUniqueError as nue:
       print(nue)
   except ValidationError:
       print("Incorrect data types entered, expecting string inputs")

def removeStudent(firstlast, class_code, username):
   user = User.objects.get(username=username)
   dropped_class = class_search(class_code, user).class_list
   if not dropped_class:
       return "Fail"

   for i in range(len(dropped_class)):
       if dropped_class[i].id == firstlast:
           dropped_class.pop(i)
           user.save()
           break
       elif i == len(dropped_class)-1:
           print(firstlast + " not in class list")

def addClass(class_code, username):
   try:
       new_class = Class(class_code=class_code)
       user = User.objects.get(username=username)
       user.classes.append(new_class)
       user.save()
       return None
   except ValidationError:
       return 'Improper class code, must follow regex pattern [A-Z]{3}[0-9]{1}[A-Z]{1}-[0-9]{2}, example: ICS4U-01'
   except NotUniqueError:
       return 'You already have this class!'

def addDay(date, class_code, username):
   def copyClassList(selected_class):
       student_attendance = []
       for student in selected_class.class_list:
           copy_of_student = Student(id=student.id, first_name=student.first_name, last_name = student.last_name)
           copy_of_student.attendance = False
           student_attendance.append(copy_of_student)
       return student_attendance

   user = User.objects.get(username=username)
   selected_class = class_search(class_code, user)
   if not selected_class:
       return "Fail"

   student_attendance = copyClassList(selected_class)

   #Create new day and add to calendar
   new_day = Day(date=date, day_attendance=student_attendance)
   selected_class.calendar.append(new_day)

   user.save()

def markStudentPresent(date, class_code, id, username):
   user = User.objects.get(username=username)
   selected_class = class_search(class_code, user)
   if not selected_class:
       return "Fail"

   for day in selected_class.calendar:
       if day.date == date:
           for student in day.day_attendance:
               if student.id == id:
                   student.attendance = True
                   break
           break
   user.save()

def getAttendance(date, class_code, username):
   user = User.objects.get(username=username)
   selected_class = class_search(class_code, user)
   if not selected_class:
       return "Fail"

   for day in selected_class.calendar:
       if day.date == date:
           day_attendance = {}
           for student in day.day_attendance:
               day_attendance[student.id] = student.attendance
           return day_attendance
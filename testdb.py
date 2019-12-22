import userdb as db

'''
db.registerUser('fred', 'bruh')
db.addClass('ICS4U-01', db.User.objects.get(username='fred').id)
db.addClass('ICS4U-02', db.User.objects.get(username='fred').id)
'''
'''
db.addStudent('FredLiu', 'ICS4U-01', db.User.objects.get(username='fred').id)
db.addStudent('FredLiu', 'ICS4U-01', db.User.objects.get(username='fred').id)
db.addStudent('FredLiu', 'ICS4U-01', db.User.objects.get(username='fred').id)
db.addStudent('FredLiu', 'ICS4U-02', db.User.objects.get(username='fred').id)
db.addStudent('FredLiu', 'ICS4U-02', db.User.objects.get(username='fred').id)
db.addStudent('FredLiu', 'ICS4U-02', db.User.objects.get(username='fred').id)
'''

#db.markStudentPresent('20190922', 'ICS4U-01', 'FredLiu1', db.User.objects.get(username='fred').id)
#print(db.getAttendance('20190922', 'ICS4U-01', db.User.objects.get(username='fred').id))
#db.addClass('ICS4U-01', 'a')
#db.addStudent('fredliu', 'fred', 'liu', 'ICS4U-01', 'fred')
db.printDb()
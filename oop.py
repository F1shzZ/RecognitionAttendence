import math as m


class schoolMember():

    count = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        schoolMember.count += 1

    def tell(self):
        print("name:", self.name, "age", self.age)

    def delete(self):
        schoolMember.count -= 1

    @classmethod
    # cls
    def memberCount(cls):
        return(cls.count)

    @staticmethod
    # no cls or self needed
    def welcome():
        print("welcome to school")


class student(schoolMember):
    def __init__(self, name, age, studentNumber):
        schoolMember.__init__(self, name, age)
        self.studentNumber = studentNumber
        schoolMember.welcome()

    def tell(self):
        schoolMember.tell(self)
        print(self.studentNumber)

    def welcome(self, a):
        print("hello", self.name, a)

    # same name override
    # doesnt matter method levle (instance method, class method, static method)
    @staticmethod
    def delete():
        print("scholl is not over yet")


class teacher(schoolMember):
    def __init__(self, name, age):
        print("int")
        schoolMember.__init__(self, name, age)
    # def __init__(self):
    #     print('hi')


if __name__ == "__main__":

    t = teacher("teacher", 30)
    # t = teacher()
    t.tell()

    print(int(m.sqrt(3)))

    George = student("george", 16, 26)
    # override
    George.tell()
    # classmethod can interact with class instance
    print(schoolMember.memberCount())
    # same override no matter the levle of functions or the parameters
    George.delete()
    # classmethod
    print(schoolMember.memberCount())
    # staticmethod
    # can't interact with class instance
    # can only perform some individual functions
    schoolMember.welcome()
    # same override no matter the levle of functions or the parameters
    George.welcome('a')

#!/usr/local/bin/python3

import oop

print('done')


class test(oop.schoolMember):
    def __init__(self, name, age):
        super().__init__(name, age)


class test2(oop.teacher, oop.student):
    def __init__(self, name, age, studentNumber):
        oop.teacher.__init__(self, name, age)
        print(oop.schoolMember.memberCount())
        oop.student(name, age, studentNumber)


t = test('try in import', -1)
print(oop.schoolMember.memberCount())

test2('test2', -2, 'num')
print(oop.schoolMember.memberCount())

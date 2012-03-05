class Foo(object):
    def __getattr__(self, name):
        print name

    def __get(self):
        return "asdasd"


class Foo1(Foo):
    def __get(self):
        return "1111"

f = Foo1()
print f._Foo1__get()


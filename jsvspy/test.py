name = "bbbb"

class Test(object):
	name = "aaa"
	def Foo(self):
		def w(*args, **kwargs):
			#global name
			print args, kwargs, self.name, name #  �հ���������
		return w

c = Test().Foo()
Test.name = "ccc"
c(1, 2)
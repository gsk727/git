#-*- coding:utf-8 -*-
import struct
import StringIO
class MsgHeader(object):
    MSG_TYPE_DATA = 1
    MSG_TYPE_METHOD = 2
    MSG_TYPE_CLASS = 3
    MSG_TYPE_ARGS = 4
    type_index = {
        float:1,
        int:2,
        str:3,
        "method":4,
        }

    def __init__(self):
        pass

    def addHeader(self, stream, data_type, data_len):
        data_len += 3
        data_type = self.type_index[data_type]
        stream.write(struct.pack("H", data_len))
        stream.write(struct.pack("B", data_type))

class Message:
    type_map ={
        ("list", "tuple"):"writeList",
        ("dict", ):"writeDict",
        ("int",):"writeInt",
        ("float",):"writeFloat",
        ("str", "unicode"):"writeStr",
        ("bool",):"writeBool",
        }
    type_index = {
        "float":1,
        "int":2,
        "str":3,
        "method":4,
        "list":5,
        "dict":6,
        "bool":7,
        }
    def __init__(self):
        """
        data_len:  当前写操作的数据长度，包括头长度和数据长度
        """
        self.data_len = 0
        self.stream = StringIO.StringIO()

    def getWriter(self, data_type):
        for t, w in self.type_map.iteritems():
            if data_type in t:
                return getattr(self, w)

    def addType(self, data_type):
        data_type = self.type_index[data_type]
        self.stream.write(struct.pack("B", data_type))
        self.data_len += 1

    def addData(self, data_type, data):
        self.write(data)
        self.writeEnd()

    def writeEnd(self):
        print self.data_len
        self.stream.seek(1,0)
        self.stream.write(struct.pack("H", self.data_len))

    def addHeader(self, data_type):
        data_type = self.type_index[data_type]
        print data_type
        self.stream.write(struct.pack("B", data_type))

        self.stream.write(struct.pack("H", 0))
        self.data_len += 3
        self.origin_header = False

    def writeList(self, data):
        origin_len = self.data_len
        origin_pos = self.stream.tell()
        self.data_len = 0
        self.addHeader("list")
        for d in data:
            self.write(d)

        self.endAWrite(origin_len, origin_pos)

    def endAWrite(self,  origin_len, origin_pos):
       self.stream.seek(origin_pos + 1, 0)
       self.stream.write(struct.pack("H", self.data_len))
       self.data_len += origin_len
       self.stream.seek(0, 2)

    def writeDict(self, data):
        origin_len = self.data_len
        self.data_len = 0
        origin_pos = self.stream.tell()
        self.addHeader("dict")
        for k, v in data.items():
            self.write((k,v))
        self.endAWrite(origin_len, origin_pos)

    def writeInt(self, data):
        self.addType("int")
        self.stream.write(struct.pack("i", data))
        self.data_len +=  4

    def writeFloat(self, data):
        d = struct.pack("f", data)
        l = len(d)
        self.addType("float")
        self.stream.write(d)
        self.data_len += l

    def writeStr(self, data):
        self.addType("str")
        self.stream.write(struct.pack("H", len(data) + 3 ))
        self.data_len += 2
        fmt = "%ds"%(len(data))

        self.stream.write(struct.pack(fmt, data))
        self.data_len += len(data)

    def writeBool(self, data):
        self.addType("bool")
        self.stream.write(struct.pack("?", data))
        self.data_len += 1

    def write(self, data):
        t = data.__class__.__name__
        if t == "unicode":
            t = "str"
            data = str(data.decode("utf-8"))

        w = self.getWriter(t)
        w(data)

    def reset(self):
        self.stream.truncate(0)
        self.data_len = 0

if __name__ == "__main__":
    m = Message()
    data = {"2":"2", '1':'1'}

    m.addData("dict", data)
    print len(m.stream.getvalue())
    # m.reset()
    # m.addData("dict", data)
    # print m.stream.getvalue()

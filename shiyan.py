
class A(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super(A,cls).__new__(cls, *args, **kwargs)

        return cls._instance



class B(object):
    pass

a = B()
B.cc = a

if hasattr(B,"cc"):
    print '0.o'
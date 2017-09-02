import sys
import os
def main():
    print("main code")

def meth1():
    print("meth1")

def func2(*args): #unpacking
   print(args)  #args is a tuple
   for arg in args:
       print arg

def get_recorder_nums(*args):
    nums = []
    for arg in args:
        recorder_num = arg.split('_')
        nums.append(recorder_num[-1])
    print 'This sis nums'
    print nums

meth1()

a = 'C:\Users\BIOWAVES\PycharmProjects\audioMerger\D2-170813-153000.wav'
x = 'C:\Users\BIOWAVES\PycharmProjects\audioMerger\D2-170813-153000.txt'
b = os.path.join(a)


def ends_wav(c):
    print 'WTF'
    if not c.endswith('.wav'):
        print 'Does not endwith .wav', c
    else:
        print 'Does endwith .wav', c



print b
if __name__ == "__main__":
    import sys
    print(sys.argv)
    print (len(sys.argv))
    main()
    args = sys.argv[1:]
    func2(*args)
    get_recorder_nums(*args)

    ends_wav(a)
    ends_wav(x)
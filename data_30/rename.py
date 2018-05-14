import sys
import os
from os import walk

def lv2grename():
    print("Renaming files...")
    for (dirpath, dirnames, filenames) in walk('./'):
        print(dirpath)
        for filename in filenames:
            sp=filename.split(".")
            if len(sp)>2 :
                new=sp[0]+sp[1]+'.'+sp[len(sp)-1]
                print("\t" + filename + " -> " + new)
                os.rename(dirpath+'/'+filename, dirpath+'/'+new)

if __name__ == '__main__':
    lv2grename()

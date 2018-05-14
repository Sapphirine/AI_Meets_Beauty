import sys
import os
from os import walk

def rename():
    for (folder, pl, files) in walk('./'):
        print(folder)
        for file in files:
            items=file.split(".")
            if len(items)>2 :
                new=items[0]+items[1]+'.'+items[len(items)-1]
                print("\t" + file + " -> " + new)
                os.rename(folder+'/'+file, folder+'/'+new)

if __name__ == '__main__':
    rename()

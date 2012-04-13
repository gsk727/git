import os
for i in xrange(100):
    with open(str(i), "w+") as f:
        f.write(str(i))
    
    os.system("git add .")
    os.system("git commit -m %d"%(i,))
    os.system("git push")


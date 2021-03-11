import time
#import subprocess
#from sys import argv


for i in range(1,50):
    data=open("worm{}.txt".format(i),"w")
    time.sleep(0.25)
    data.write("Your computer has been infected!")

data.close()
    

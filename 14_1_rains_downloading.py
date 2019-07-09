from ftplib import FTP
import datetime, time,os
ts = time.time()
print "Starting at "+ datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

y = 2019
m = 1
d = 1

if m <10:
    m = "0"+str(m)

if d <10:
    d = "0"+str(d)
b = 1
filepath=r"C:/Ocean-2019/variables/14rainfall"
down_file="3B-HHR-L.MS.MRG.3IMERG."+str(y)+str(m)+str(d)+"-S000000-E002959.0000.V05B.1day.tif"
down_file2="3B-HHR-L.MS.MRG.3IMERG."+str(y)+str(m)+str(d)+"-S000000-E002959.0000.V05B.1day.tif"

ftp=FTP("jsimpson.pps.eosdis.nasa.gov")
ftp.login("ju.iowa@gmail.com","ju.iowa@gmail.com")
ts = time.time()
print "Logged at "+ datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
directory1="/data/imerg/gis/"+str(y)+"/"+str(m)+"/"

def ___download___( directory, downloaded_files, down_path): 
   ftp.cwd(directory1)
   with open(os.path.join(down_path, downloaded_files), 'wb') as local_file:
        ftp.retrbinary('RETR '+ downloaded_files, local_file.write)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print downloaded_files+" downloaded at "+st  
while y < 2020:
    for n in ftp.nlst(directory1):
 
        if n[56:70]=="S233000-E23595" and n[82:86]=="1day":
           
            if n[87:90]=="tif" or n[87:90]=="tfw" :
                

                ___download___(directory1, n[24:], filepath)
                b = b+2
                d = int(d)+1
                    
    m = int(m)+1
    if int(m) <10:
            m = "0"+str(m)    
    if int(m)>12:
                    y = int(y)+1
                    m = 1
                    d = 1
                    if int(d) <10:
                        d = "0"+str(d)
                    if int(m) <10:
                        m = "0"+str(m)


    ftp.close()
    ftp=FTP("jsimpson.pps.eosdis.nasa.gov")
    ftp.login("ju.iowa@gmail.com","ju.iowa@gmail.com")
    directory1="/data/imerg/gis/"+str(y)+"/"+str(m)+"/"
    down_file="3B-HHR-L.MS.MRG.3IMERG."+str(y)+str(m)+str(d)+"-S000000-E002959.0000.V05B.1day.tif"

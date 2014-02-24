
import argparse
import csv
import utils
import os



parser = argparse.ArgumentParser(description='encoded file ')
parser.add_argument("-d",'--dataFilePath' ,type=file,help='csv data file encode files')
args =parser.parse_args()


dataFilePath = args.dataFilePath.name
###################################################################
#main
if dataFilePath == None:
    print "no file input "
    exit 


# open CSV file
ifile  = open(dataFilePath, "rb")
reader = csv.reader(ifile)
print "start parsing file %s" % dataFilePath

encodeFilePath = "%s%s" % ( dataFilePath  ,"encoded.csv")

string_hash ={}

if os.path.exists(encodeFilePath):
    os.remove(encodeFilePath)


wfile = open(encodeFilePath,"wb")
writer_ =  csv.writer(wfile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)



rownum = -1
for row in reader:
    rownum += 1
    rowList=[]
    for col in row:
        if rownum ==0 :
            newcol = col
        else:
            newcol = utils.EncodeString(col)
            if not string_hash.has_key(newcol):
                string_hash[newcol]=str(col)
        rowList.append(newcol)
    writer_.writerow(rowList)

print "finish encoded data set ,encoded data set is save on %s " % encodeFilePath    
utils.DumpObjToFile(string_hash, "sting_hash_generate.pkl")



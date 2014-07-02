import utils
import csv
import argparse
from apt_pkg import HashString

FILE_SUFFIX = "encoded.csv"
FILE_HASH_PICKLE="string_hash_2.pkl"

def CreateNewEncodeData(dataFilePath):
    
    ifile  = open(dataFilePath, "rb")
    wfile   = open(dataFilePath+FILE_SUFFIX,"wb")
    reader = csv.reader(ifile)
    writer = csv.writer(wfile,delimiter=',',quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    rowCont =0
    for row in reader:
        rowArr =[]
        for col in row:
            if (rowCont==0):
                rowArr.append(col)
            else:
                rowArr.append(utils.EncodeString(col))
            #print row
             
        writer.writerow(rowArr)
        rowCont+=1
############################################################

def createHash(dataFilePath):
    print "fuck"
    ifile  = open(dataFilePath, "rb")    
    reader = csv.reader(ifile)
    rowCont =0
    hashString={}
    for row in reader:
        rowArr =[]
        for col in row:
            if (rowCont==0):
                rowCont+=1
                continue
            else:
                codedCol= utils.EncodeString(col)
                hashString[codedCol] =col
    
    utils.DumpObjToFile(hashString,FILE_HASH_PICKLE)   
###################### main ######################




parser = argparse.ArgumentParser(description='parse to graph ')
parser.add_argument("-d",'--dataFilePath' ,type=file,help='csv data file for create new encode data')
parser.add_argument("-s",'--hash_file',action="store_true",help='create hash_item')
args =parser.parse_args()

dataFilePath=args.dataFilePath.name if args.dataFilePath.name!=None else 'data.csv'
print "encoding data...."
CreateNewEncodeData(dataFilePath)

print "done!!!"
if args.hash_file:
    print "create new hash pickle"
    createHash(dataFilePath)
    if not utils.PathExist(FILE_HASH_PICKLE) :
        print "Error file not created!!!"
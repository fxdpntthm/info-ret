import os
import glob
import threading
import multiprocessing
from nltk.util import ngrams
from nltk.stem.porter import PorterStemmer

#Stemmer to stem the words
ps = PorterStemmer()

def digestData(rawData):
    """generates the ngrams of the given text
        | input : raw data read from the file stream
        | output: ngrams of the given input
    """
    #print "in digestData"
    #strip the punctuations
    finerText = str(rawData).lower().translate(None, "\/!?*+@#$%^&*()<>\"\':;.,-|_\n\r")
    #stem the data
    stemmedText = ps.stem(finerText)
    #generate character 5-grams of the stemmed text 
    return ngrams(list(stemmedText),5)

def digestFile(inFilePath, outFilePath):
    """reads file from inFilePath digests data and outputs
       the data in the outFilePath folder
       | input : path to the input file to read data inFilePath, 
                 path to the output file to write data outFilePath
       | output: None
    """
    try:
        #open input stream
        #print inFilePath
        inFile = open(inFilePath)

        #open output stream
        outFile = open(outFilePath, "w")
        
        #read inputstream
        #rawData = inFile.read()
        #print rawData
        #digestedData = str(digestData(rawData))
        #print digestedData
        outFile.write(str(digestData(inFile.read())))
    except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def digestMultipleFiles(inFileList, outFilePath):
    """digests multiple files given in the inFileList
       and generates corresponding data in the outFilePath
       | input : digest the files given in the inFileList
       | output: None
    """
    print "digesting partition " + inFileList[0]
    for fileName in inFileList:
        digestFile(fileName, outFilePath+fileName)

def digestAllFiles(inDirectory, outDirectory):
    """uses 10 parallel process to read 
       all the files in the inDirectory
       digests data and writes in the outDirectory
       each file in the outDirectory contains the respective
       ngrams of each file
       | input : directory name in which the corpus is situated
       | output: None
    """
    
    process_list=[]

    for i in range(0,10):
        print "partition: " + inDirectory+"/1"+str(i)+"*"
        listOfFiles = glob.glob(inDirectory+"/1"+str(i)+"*")
        #print "list:" + str(listOfFiles)
        p = multiprocessing.Process(target=digestMultipleFiles, args=(listOfFiles, outDirectory))
        process_list.append(p)

    for i in range(2,10):
        print "partition: " + inDirectory+"/"+str(i)+"*"
        listOfFiles = glob.glob(inDirectory+"/"+str(i)+"*")
        #print "list:" + str(listOfFiles)
        p = multiprocessing.Process(target=digestMultipleFiles, args=(listOfFiles, outDirectory))
        process_list.append(p)

    print "Status: starting process execution"
    #start the thread execution
    for p in process_list:
        p.start()

    #wait for the threads to stop
    for p in process_list:
        p.join()
    
    print "Status: all files data digested" 
    print "input directory:" + inDirectory + " output Directory: " +outDirectory + "corpus"

digestAllFiles("corpus", "ngramsData")

#testing functions
#f = open(r'corpus/1.txt')
#out = open("ngramsData/1.txt", "w")
#out.write(str(digestData(f.read())))

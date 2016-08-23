import cv2
import numpy as np
import os.path
import pathOperator
import shutil

def testcode():
    img = cv2.imread("/home/zoul15/img/sourceimg.jpg",0)
    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("/home/zoul15/img/matchimg.jpg",0)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    print type(res)
    threshold = 0.8
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        print pt[0],pt[1]

def Match(sourceFName, matchFName,partFName):
    img = cv2.imread(sourceFName,0)
    template = cv2.imread(matchFName,0)

    partTemplate = cv2.imread(partFName,0)

    # get part deviation
    deRes = cv2.matchTemplate(partTemplate,template,cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    loc = np.where( deRes >= threshold)
    dePoint = []
    for pt in zip(*loc[::-1]):
        dePoint.append(pt[0])
        dePoint.append(pt[1])
        break

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)

    # change point list
    changePointList = []
    for pt in zip(*loc[::-1]):
        changePoint = []
        changePoint.append(pt[0]-dePoint[0])
        changePoint.append(pt[1]-dePoint[1])
        changePointList.append(changePoint)

    # print debug info
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(changePointList)

    # get part area
    w,h = partTemplate.shape[::-1]

    # change picture
    for loc in changePointList:
        x,y = loc
        cv2.rectangle(img,(x,y),(w,h),(255,255,255),-1)
#        img[x:x+w,y:y+h] = [255,255,255]

    dirName = os.path.dirname(sourceFName)
    fname = "_"+os.path.basename(sourceFName)
    wfile = os.path.join(dirName,fname)

    cv2.imwrite(wfile,img)

def PaintExceptTitle(sourceFName,titleFName):
    if os.path.isdir(sourceFName):
        fnameList = os.listdir(sourceFName)
        for fname in fnameList:
            fullName = os.path.join(sourceFName,fname)
            PaintExceptTitle(fullName,titleFName)
        return

    img = cv2.imread(sourceFName,0)
    title = cv2.imread(titleFName,0)

    w,h = title.shape[::-1]
    sw,sh = img.shape[::-1]

    img = cv2.imread(sourceFName,-1)
    cv2.rectangle(img,(0,h),(sw,sh),(255,0,0),-1)

    dirName = os.path.dirname(sourceFName)
    fname = "_"+os.path.basename(sourceFName)
    wfile = os.path.join(dirName,fname)

    cv2.imwrite(wfile,img)
    os.remove(sourceFName)

def FetchTitle(sourceFName):
    img = cv2.imread(sourceFName,0)
    sw,sh = img.shape[::-1]

    dirName = os.path.dirname(sourceFName)
    fname = "_"+os.path.basename(sourceFName)
    wfile = os.path.join(dirName,fname)

    cv2.imwrite(wfile,img[0:500,0:827])

    print sw,"\t",sh

def checkSize():
    pass

# delete the picture in which I joined
def filterPic(sourceFname, myyFname,mynFname):
    if os.path.isdir(sourceFname):
        fileList = pathOperator.listfile(sourceFname)
        for filename in fileList:
            filterPic(filename,myyFname,mynFname)
        return

    # myyFname match and mynFname not match, then delete sourceFname
    print "process:   ", sourceFname
    img = cv2.imread(sourceFname, -1)
    myy = cv2.imread(myyFname, -1)
    myn = cv2.imread(mynFname, -1)

    # match myy
    deRes = cv2.matchTemplate(img, myy, cv2.TM_CCOEFF_NORMED)
    # print type(deRes)
    # print deRes
    # for v in deRes:
    #     for r in v:
    #         if r > 0.8:
    #             print r
    threshold = 0.99
    loc = np.where(deRes >= threshold)
    # print "loc"
    # print loc
    myyPoint = []
    for pt in zip(*loc[::-1]):
        myyPoint.append(pt[0])
        myyPoint.append(pt[1])
        break

    # match myn
    deRes = cv2.matchTemplate(img, myn, cv2.TM_CCOEFF_NORMED)
    # print type(deRes)
    # print deRes
    # for v in deRes:
    #     for r in v:
    #         if r > 0.8:
    #             print r
    threshold = 0.99
    loc = np.where(deRes >= threshold)
    mynPoint = []
    for pt in zip(*loc[::-1]):
        mynPoint.append(pt[0])
        mynPoint.append(pt[1])
        break

    print len(myyPoint),len(mynPoint)
    if len(myyPoint) > 0 and len(mynPoint) == 0:
        os.remove(sourceFname)
        print "remove:  ",sourceFname
        return

def paintViewer(sourceFname, viewerFname):
    if os.path.isdir(sourceFname):
        fileList = pathOperator.listfile(sourceFname)
        for filename in fileList:
            paintViewer(filename,viewerFname)
        return

    img = cv2.imread(sourceFname, -1)
    viewer = cv2.imread(viewerFname, -1)

    w, h = img.shape[:-1]
    vw,vh = viewer.shape[:-1]

    deRes = cv2.matchTemplate(img, viewer, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(deRes >= threshold)
    myyPoint = [] # array of point
    for pt in zip(*loc[::-1]):
        myyPoint.append([pt[0],pt[1]])

        cv2.rectangle(img, (0, pt[1]), (w, pt[1] + vh), (255, 0, 0), -1)

    print "paint  :",sourceFname
    cv2.imwrite(sourceFname,img)

def sortPic(tempDir, sourceDir):
    dirList = pathOperator.listdir(tempDir)

    # construct template dict
    tempimgDict = {}
    for dirname in dirList:
        tempimgDict[dirname] = []

        tempfileList = pathOperator.listfile(dirname)
        for filename in tempfileList:
            tempimg = cv2.imread(filename, -1)
            tempimgDict[dirname].append(tempimg)

    # match img

    imgfileList = pathOperator.listfile(sourceDir)
    for imgfile in imgfileList:
        print "process   :",imgfile
        targetimg = cv2.imread(imgfile,-1)
        matchsuccess = 0
        for tempdirname in dirList:
            tempimgList = tempimgDict[tempdirname]
            if matchsuccess:
                break

            for tempimg in tempimgList:
                deRes = cv2.matchTemplate(targetimg, tempimg, cv2.TM_CCOEFF_NORMED)
                threshold = 0.99
                loc = np.where(deRes >= threshold)
                myyPoint = []  # array of point
                for pt in zip(*loc[::-1]):
                    myyPoint.append([pt[0], pt[1]])
                    break

                # match success, move the pic to target dir
                if len(myyPoint) > 0:
                    shutil.copy(imgfile, os.path.join(tempdirname,os.path.basename(imgfile)))
                    matchsuccess = 1
                    break

if __name__ == "__main__":
    #FetchTitle("/home/zoul15/img/htkpk.jpg")
    #PaintExceptTitle("/home/zoul15/img/pk","/home/zoul15/img/title.jpg")
    #Match("/home/zoul15/img/sourceimg.jpg","/home/zoul15/img/sourceimg.jpg","/home/zoul15/img/sourceimg.jpg")


    #filterPic("/media/zoul15/Elements/test","/home/zoul15/img/mey.jpg","/home/zoul15/img/men.jpg")
    #paintViewer("/media/zoul15/Elements/test","/media/zoul15/Elements/test/me/viewer.jpg")
    sortPic("/media/zoul15/Elements/test/me/pk","/media/zoul15/Elements/test")
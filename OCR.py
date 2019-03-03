def fun(list1):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import tensorflow as tf
    import cv2
    import random
    # Import costume functions, corresponding to notebooks
    from ocr.normalization import imageNorm, letterNorm
    from ocr import page, words
    #from ocr import charSeg
    from ocr.helpers import implt, resize
    from ocr.tfhelpers import Graph
    from ocr.datahelpers import idx2char
    from src import gsmain
    import glob
    import os
    # ### Global Variables
    for x_file in list1:
        tf.reset_default_graph()
        str1 = ''.join(x_file)
        # Settings
        IMG = str1    # 1, 2, 3
        # ## Load image
        
        image = cv2.cvtColor(cv2.imread(IMG), cv2.COLOR_BGR2RGB)
        implt(image)
        
        # Crop image and get bounding boxes
        crop = page.detection(image)
        implt(crop)
        bBoxes = words.detection(crop)
        lines = words.sort_words(bBoxes)
        filelist=glob.glob("./new3/*.png")
        for file in filelist:
            os.remove(file)
        indeximg = 0
        nl=0
        for line in lines: 
            for (x1, y1, x2, y2) in line:
                cv2.imwrite("new3/" + str(indeximg)+".png",crop[y1:y2, x1:x2])
                #implt(cv2.imread("outcheck.png"))
                indeximg = indeximg + 1
                #gsmain.FilePaths.fnInfer = ["outcheck.png"]
                #wordreco = gsmain.main()
                #file.write(wordreco + ' ')
            cv2.imwrite("new3/"+str(nl)+"space.png",crop[y1:y2,x1:x2])
            nl=nl+1
        
        
        #Get all segmented words
        list2 = glob.glob("./new3/*.png")
        list2.sort(key=os.path.getmtime)
        '''list2=list()
        for ii in range(0,indeximg):
            list2.append("")'''
        #all files which have to be infer are loaded
        rand_num= random.randint(100,1000)
        cv2.imwrite('final_output/'+str(rand_num)+'.jpg',image)
        for i in range(0,len(list2)):
            gsmain.FilePaths.fnInfer = gsmain.FilePaths.fnInfer + [list2[i]]
        gsmain.main('final_output/'+str(rand_num))

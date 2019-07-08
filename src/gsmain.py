from __future__ import division
from __future__ import print_function

import sys
import numpy as np
import argparse
import cv2
import editdistance
from src import DataLoader
from src import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2
import glob
import os
import re
import math

# Import costume functions, corresponding to notebooks
#from ocr.normalization import imageNorm, letterNorm
#from ocr import page, words
#from ocr import charSeg
from ocr.helpers import implt, resize
from ocr.tfhelpers import Graph
from ocr.datahelpers import idx2char


#from src import Model.DecoderType, Model.Model
#from src import DataLoader.DataLoader, Dataloader.Batch
#sfrom src import SamplePreprocessor
from src import SamplePreprocessor
img=[]
def preprocessimg(addr):
	img = cv2.imread(addr)
	#cv2.imwrite("outpre.png",img)
	#theta = compute_skew("outpre.png")
	#img = deskew("outpre.png", theta)
#	img = contrast(img)# increase contrast
	pxmin = np.min(img)
	pxmax = np.max(img)
	imgContrast = (img - pxmin) / (pxmax - pxmin) * 255# increase line width
	kernel = np.ones((2,2), np.uint8)
	imgMorph = cv2.erode(imgContrast, kernel, iterations = 1)
	blur = cv2.bilateralFilter(img,9,75,75)
	return blur

def contrast(img):

   # img = cv2.imread('sunset.jpg', 1)

   # cv2.imshow("Original image",img)

   # CLAHE (Contrast Limited Adaptive Histogram Equalization)

   clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

   
   lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space

   l, a, b = cv2.split(lab)  # split on 3 different channels

   l2 = clahe.apply(l)  # apply CLAHE to the L-channel

   lab = cv2.merge((l2,a,b))  # merge channels

   img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR

   img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

   cv2.adaptiveThreshold(img3,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY ,41,3)

   ret,thresh1 = cv2.threshold(img3,127,255,cv2.THRESH_BINARY)


   return thresh1

    
class FilePaths:
	"filenames and paths to data"
	fnCharList = 'model/charList.txt'
	fnAccuracy = 'model/accuracy.txt'
	fnOut = 'data/out'
	fnTrain = 'data/'
	fnInfer = []
	fnCorpus = 'data/corpus.txt'
	index = 0
	#fnOut = '../data/out.png'
    #f
    
    
def train(model, loader):
	"train NN"
	epoch = 0 # number of training epochs since start
	bestCharErrorRate = float('inf') # best valdiation character error rate
	noImprovementSince = 0 # number of epochs no improvement of character error rate occured
	earlyStopping = 5 # stop training after this number of epochs without improvement
	while True:
		epoch += 1
		print('Epoch:', epoch)

		# train
		print('Train NN')
		loader.trainSet()
		while loader.hasNext():
			iterInfo = loader.getIteratorInfo()
			batch = loader.getNext()
			loss = model.trainBatch(batch)
			print('Batch:', iterInfo[0],'/', iterInfo[1], 'Loss:', loss)

		# validate
		charErrorRate = validate(model, loader)
		
		# if best validation accuracy so far, save model parameters
		if charErrorRate < bestCharErrorRate:
			print('Character error rate improved, save model')
			bestCharErrorRate = charErrorRate
			noImprovementSince = 0
			model.save()
			open(FilePaths.fnAccuracy, 'w').write('Validation character error rate of saved model: %f%%' % (charErrorRate*100.0))
		else:
			print('Character error rate not improved')
			noImprovementSince += 1

		# stop training if no more improvement in the last x epochs
		if noImprovementSince >= earlyStopping:
			print('No more improvement since %d epochs. Training stopped.' % earlyStopping)
			break


def validate(model, loader):
	"validate NN"
	print('Validate NN')
	loader.validationSet()
	numCharErr = 0
	numCharTotal = 0
	numWordOK = 0
	numWordTotal = 0
	while loader.hasNext():
		iterInfo = loader.getIteratorInfo()
		print('Batch:', iterInfo[0],'/', iterInfo[1])
		batch = loader.getNext()
		(recognized, _) = model.inferBatch(batch)
		
		print('Ground truth -> Recognized')	
		for i in range(len(recognized)):
			numWordOK += 1 if batch.gtTexts[i] == recognized[i] else 0
			numWordTotal += 1
			dist = editdistance.eval(recognized[i], batch.gtTexts[i])
			numCharErr += dist
			numCharTotal += len(batch.gtTexts[i])
			print('[OK]' if dist==0 else '[ERR:%d]' % dist,'"' + batch.gtTexts[i] + '"', '->', '"' + recognized[i] + '"')
	
	# print validation result
	charErrorRate = numCharErr / numCharTotal
	wordAccuracy = numWordOK / numWordTotal
	#print('Character error rate: %f%%. Word accuracy: %f%%.' % (charErrorRate*100.0, wordAccuracy*100.0))
	return charErrorRate


def infer(model, fnImg, f):
	"recognize text in image provided by file path"
	img = SamplePreprocessor.preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.Model.imgSize)
	import numpy as np
	np.shape(img)
	batch = DataLoader.Batch(None, [img])
	print(np.shape(img))
	(recognized, probability) = model.inferBatch(batch, True)
	out_name='new1/check%s'%FilePaths.index + '+%s.png'%recognized[0]
	img1=cv2.imread(fnImg)
	cv2.imwrite(out_name,img1)
	print('Recognized:', '"' + recognized[0] + '"')
	f.write(recognized[0] + " ")
	#print('Probability:', probability[0])


def main(file_name):
#	print(open(FilePaths.fnAccuracy).read())
	decoderType = Model.DecoderType.BestPath
	model = Model.Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True)
	filelist=glob.glob("new1/*.png")
	filename = file_name+'.txt'
	f=open(filename,'w')
	for file in filelist:
		os.remove(file)
	for i in FilePaths.fnInfer:
		if i[-5]=='e':
			f.write('\n')
		else:  
			print("processing ",i)
			img=preprocessimg(i)
			implt(img)
		    #img=cv2.imread(i)
		    #img=contrast(img)
		    #implt(img)
			cv2.imwrite("out123.png",img)
			FilePaths.index = FilePaths.index + 1
			infer(model,"out123.png", f)
	f.close()
'''if __name__ == '__main__':
	main()
'''

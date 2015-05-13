#!/usr/local/bin/python3

from FPGrowth.FPGrowth import database

db=database()
db.loadTrans('data/dataset1.data.tra')
db.identifyFreqItems(10)
db.reorderFreqItems()

from FPGrowth.FPGrowth import FPTree

alpha=FPTree()
alpha.growth(db.trans,db.occurence)
traverseOrder=alpha.getTraverseOrder()
traverseOrder[0]

fpPattern=alpha.getConditionalTrans(54)

beta=FPTree()
beta.growth([db.trans[0]],db.occurence)
sinNodeList=beta.getSinglePathTreeNodes()


#####
from FPGrowth.FPGrowth import FPGrowth
dataset1=FPGrowth('data/dataset1.data.tra',10)
dataset1.process()

dataset2=FPGrowth('data/dataset2.data.tra',10)
dataset2.process()

dataset3=FPGrowth('data/dataset3.data.tra',200)
dataset3.process()

dataset4=FPGrowth('data/dataset4.data.tra',1000)
dataset4.process()

dataset5=FPGrowth('data/Dataset-D(n_1M).TXT',1000)
dataset5.process()

dataset6=FPGrowth('data/ASSO_DS_2.txt',1000,splitter=' ')
dataset6.process()


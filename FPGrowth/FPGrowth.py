#!/usr/local/bin/python3

class database():
  def __init__(self):
    pass
  def loadTrans(self,infileName,splitter=','):
    with open(infileName,'r') as infile:
      strlines=list(map(lambda x:x.strip('\n'),infile.readlines()))
    self.trans=list(map(lambda x:list(map(lambda y:int(y),x.split(splitter))),
                        strlines))
  def loadTransFromFP(self,patternList):
    self.trans=[]
    for pattern in patternList:
      for index in range(pattern[1]):
        self.trans.append(pattern[0])
  def identifyFreqItems(self,mini_support,fraction=0.01):
    self.occurence={}
    if mini_support==0:
      mini_support=len(self.trans)*fraction
    def mapping(x):
      if x in self.occurence:
        self.occurence[x]=self.occurence[x]+1
      else:
        self.occurence[x]=1
    for tran in self.trans:
      for x in tran:
        mapping(x)
    self.freqItems=list(filter(lambda x: self.occurence[x]>=mini_support,
                               self.occurence))
  def reorderFreqItems(self):
    def sortOrder(elements):
      return sorted(elements,key=lambda x:self.occurence[x],reverse=True)
    self.trans=list(map(lambda x: sortOrder(list(filter(lambda y:y in self.freqItems,x))),self.trans))

class FPNode():
  def __init__(self,itemName,index,parent):
    self.itemName=itemName
    self.index=index
    self.parent=parent
    #self.children=[]
    self.children={}
    self.previous=None
    self.nextNode=None
  def appendChild(self,child):
    #self.children.append(child)
    self.children[child.itemName]=child
  def getChildren(self):
    #return self.children
    return list(self.children.values())
  def getChild(self,itemName):
    #return list(filter(lambda x: x.itemName==itemName,self.children))
    if itemName in self.children:
      return [self.children[itemName]]
    else:
      return []
  def getParent(self):
    return self.parent
  def incIndex(self):
    self.index+=1

class FPTree():
  def __init__(self):
    self.root=FPNode('root',0,None)
    self.header={}
  def growth(self,trans,occurence):
    self.occurence=occurence
    for tran in trans:
      self.growthOne(tran)
  def isNull(self):
    if len(self.root.children)==0:
      return True
    return False
  def growthOne(self,tran):
    current=self.root
    for x in tran:
      current.incIndex()
      if not current.getChild(x):
        child=FPNode(x,0,current)
        current.appendChild(child)
        self.buildHeader(child)
      current=current.getChild(x)[0]
    current.incIndex()
  def buildHeader(self,node):
    if node.itemName in self.header:
      node.nextNode=self.header[node.itemName]
      self.header[node.itemName].previous=node
    self.header[node.itemName]=node
  def getNodePath(self,current):
    pathList=[]
    while current!=self.root:
      pathList.append(current)
      current=current.getParent()
    return pathList
  def isSinglePathTree(self):
    current=self.root
    while True:
      if len(current.getChildren())>1:
        return False
      elif len(current.getChildren())==0:
        return True
      current=current.getChildren()[0]
  def getSinglePathTreeNodes(self):
    if self.isNull():
      return None
    elif self.isSinglePathTree():
      nodeList=[]
      current=self.root.getChildren()[0]
      while True:
        nodeList.append(current)
        if len(current.children)>0:
          current=list(current.children.values())[0]
        else:
          return nodeList
  def getTraverseOrder(self):
    return sorted(self.header.keys(),key=lambda x:self.occurence[x])
  def getConditionalTrans(self,itemName):
    currentNode=self.header[itemName]
    patternList=[]
    while currentNode:
      path=self.getNodePath(currentNode)
      pattern=list(map(lambda x:x.itemName,path[1:]))
      patternList.append((pattern,path[0].index))
      currentNode=currentNode.nextNode
    return patternList
  ## debug func below
  def traverseTree(self):
    self.recursiveAccessChild(self.root)
  def recursiveAccessChild(self,node):
    self.printStructure(node)
    for child in node.getChildren():
      self.recursiveAccessChild(child)
  def printStructure(self,node):
    print(node.itemName,'\t#:',node.index,end='\t')
    if node.parent:
      print('parent:',node.parent.itemName,end='\t')
    print('')
  def traverseNode(self,itemName):
    #return self.recursiveAccessNode(self.header[itemName],[])
    nodeList=[]
    current=self.header[itemName]
    while True:
      nodeList.append(current)
      if current.nextNode:
        current=current.nextNode
      else:
        return nodeList
  def recursiveAccessNode(self,node,nodeList):
    if node:
      #self.printStructure(node)
      nodeList.append(node)
      nodeList=self.recursiveAccessNode(node.nextNode,nodeList)
    return nodeList

class FPGrowth():
  def __init__(self,infileName,min_support,confidence=0.9,max_run=10000,splitter=',',fraction=0.01):
    self.db=database()
    self.db.loadTrans(infileName,splitter)
    self.db.identifyFreqItems(min_support)
    self.db.reorderFreqItems()
    self.min_support=min_support
    self.confidence=confidence
    self.max_run=max_run
    self.fraction=min_support/len(self.db.trans)
    print('fraction:',self.fraction)
  def process(self):
    tree=FPTree()
    tree.growth(self.db.trans,self.db.occurence)
    self.growth(tree,None)
  def genCombination(self,alpha,nodeList,numTrans):
    def selectSubCombination(index,nodeList):
      returnList=[]
      for loop in range(len(nodeList)):
        if index%2==1:
          returnList.append(nodeList[loop])
        index=int(index/2)
      return returnList
    for index in range(1,2**len(nodeList)):
      subNodeList=selectSubCombination(index,nodeList)
      support=min(list(map(lambda x:x.index,subNodeList)))
      confidence=support/numTrans
      if confidence>=self.confidence:
        confidence="%.2f" %confidence
        print(alpha,' -> ',list(map(lambda x:x.itemName,subNodeList)),'\t with confidence:',confidence,'(',support,'/',numTrans,')')
        self.max_run-=1
  def growth(self,tree,alpha):
    if self.max_run<=0:
      return
    if tree.isSinglePathTree():
      nodeList=tree.getSinglePathTreeNodes()
      self.genCombination(alpha,nodeList,tree.root.index)
    else:
      traverseOrder=tree.getTraverseOrder()
      for item in traverseOrder:
        support=sum(list(map(lambda x: x.index,tree.traverseNode(item))))
        numTrans=tree.root.index
        confidence=support/numTrans
        if confidence>=self.confidence:
          confidence="%.2f" %confidence
          print(alpha,' -> ',item,'\t with Confidence:',confidence,'(',support,'/',numTrans,')')
          self.max_run-=1
        subdb=database()
        subdb.loadTransFromFP(tree.getConditionalTrans(item))
        subdb.identifyFreqItems(self.min_support,fraction=self.fraction)
        subdb.reorderFreqItems()
        subtree=FPTree()
        subtree.growth(subdb.trans,subdb.occurence)
        if not subtree.isNull():
          if alpha:
            condition=alpha+','+str(item)
          else:
            condition=str(item)
          self.growth(subtree,condition)

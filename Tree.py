from data import dataSet
import math


#Basic Entropy of list of numbers calculation
def entropy(A):
    sum,total = 0,0
    for a in A:
        total = total+a
    if total==0:
        return 999999999999888
    for a in A:
        if(a>0):
            sum = sum - a/total*math.log(a/total)
    return sum

def ordered_insert(A,s):
    for i in range(len(A)):
        if s < A[i]:
            A.insert(i,s)
            return
    A.append(s)


class Tree:
    Nodes = []
    value = 0
    data = []
    ans = ''

    # initialize Tree objefct.
    # Root node only.
    # Contains all data records
    def __init__(self,ds):
        self.Nodes = []
        self.value = 0
        self.data = ds.clone()
        self.ans = ''


    ###  Display  ###

    #primitive display
    def dis(self):
        print("Val = {}".format(self.value))
        print("ans = {}".format(self.ans))
        for d in self.data.Data:
            print(d)
        for n in self.Nodes:
            n.dis()
    #display with indentation of size 'lvl
    def Display(self,lvl):
        s = '  '*lvl
        if self.value!=0:
            print((s+"{} val = {}").format(lvl,self.value))

        else:
            print(s+"{} ans = {}".format(lvl,self.ans))
        for d in self.data.Data:
            print((s+'|{}').format(d))
        for n in self.Nodes:
            n.Display(lvl+1)


    ###   Utility  ###

    # returns an array with mean of each field
    def means(self):
        x = [0]*(len(self.data.Data[0])-1)
        for d in self.data.Data:
            for i in range(len(d) - 1):
                x[i] = x[i] + d[i]
        for i in range(len(d) - 1):
            x[i] = x[i] / len(self.data.Data)
        return x
    # returns an array with min and max of each field
    def minmax(self):
        if len(self.data.Data) == 0:
            return []
        x = [0]*(len(self.data.Data[0])-1)
        for i in range(len(x)):
            x[i] = [self.data.Data[0][i],self.data.Data[0][i]]
        for d in self.data.Data:
            for i in range(len(d) - 1):
                if d[i] > x[i][1]:
                    x[i][1]=d[i]
                if d[i] < x[i][0]:
                    x[i][0]=d[i]
        return x


    ###  Training functions  ###

    # Returns node with highest entropy in Answer field
    # 'minNodes' is minimum records per leaf parameter
    # Ex is an exclusion list.  Nodes contained in it are skipped
    def biggestE(self, minNodes,ex):
        if self in ex:
            return [-1,-1]
        if len(self.Nodes)==0:
            g=self.nodeEntropy(minNodes) * len(self.data.Data)
            return [self, g]
        max,maxi=-1,-1
        for n in self.Nodes:
            b = n.biggestE(minNodes,ex)
            if b[1] > max:
                max=b[1]
                maxi=b[0]
        return [maxi, max]

    # Returns the entropy of a node's answer field.  Used by biggestE()
    def nodeEntropy(self, minNodes):
        if len(self.data.Data) < 2*minNodes:
            return 0
        Arrl = [0]*(len(self.data.classes))
        for d in self.data.Data:
            for k in range(len(self.data.classes)):
                if d[len(d)-1] == self.data.classes[k]:
                    Arrl[k] = Arrl[k] +1
        return entropy(Arrl)

    # Finds 'the best' split on a leaf node.
    # Returns [] if no split can be made
    # minNodes is the minimum records per leaf node parameter
    def findsplit(self,minNodes):
        # an array of the smallest and largest field values in the set
        m=self.minmax()

        # This loop ranges over the number of fields in our data
        # to find the best split in each and then choses the lowest
        # combined entropy of the two nodes obtained by each split
        for i in range(len(m)):

            # Variables for finding the smallest resultinng entropy
            minEntropy = 9999999 # tracks smallest combined entropy entropy seen so far
            ming=0

            # Breaks the interval into sections.
            # This idea is useful for problem 3
            # the 100 here could be made a parameter passed into the function
            # as a way to toggle precision but increase runtime.
            # my method is primitive and needs to be optimized
            # steps = 1000 takes significantly longer
            num_steps=100
            step = (m[i][1] - m[i][0])/num_steps

            for g in range(num_steps):
                s=m[i][0] + step*g
                Arrl = [0]*(len(self.data.classes))
                Arrg = [0]*(len(self.data.classes))
                totL,totG = 0,0
                for d in self.data.Data:
                    if s < d[i]:
                        for k in range(len(self.data.classes)):
                            if d[len(d)-1] == self.data.classes[k]:
                                Arrl[k] = Arrl[k] +1
                                totL = totL+1
                    else:
                        for k in range(len(self.data.classes)):
                            if d[len(d)-1] == self.data.classes[k]:
                                Arrg[k] = Arrg[k] +1
                                totG = totG+1

                ent = entropy(Arrl)+entropy(Arrg)
                if ent<minEntropy and totG >= minNodes and totL >= minNodes:
                    minEntropy=ent
                    ming=g
            m[i] = [m[i][0] + step*ming, minEntropy]
        Min = 99999999999999999
        Mini = []
        for i in range(len(m)):
            if m[i][1] < Min:
                Min = m[i][1]
                Mini = [m[i][0], i]
        return Mini

    def split(self, m, minnodes):
        if m==[]:
            return False
        i = m[1]
        val = m[0]
        dl= dataSet('')
        dl.fill(self.data.header,self.data.classes)
        dg= dataSet('')
        dg.fill(self.data.header,self.data.classes)

        count =0
        for d in self.data.Data:
            count = count+1
            if d[i] <= val:
                dl.Data.append(d.copy())
            else:
                dg.Data.append(d.copy())
        if len(dl.Data) < minnodes or len(dg.Data) < minnodes:
            return 'badsplit'
        self.value = m
        self.data.Data.clear()
        #rint('size = {}'.format(len(self.data.Data)))
        #print('size = {}'.format(len(dl.Data)))
        #print('size = {}'.format(len(dg.Data)))
        self.ans = ''
        self.Nodes.append(Tree(dl))
        self.Nodes.append(Tree(dg))
        for n in self.Nodes:
            n.setAns()
        return True

    # Populates the 'ans' field in a node as the most common class in the data
    # Used for determining output on the leaf nodes
    def setAns(self):
        Arrg = [0]*(len(self.data.classes))
        for d in self.data.Data:
            for k in range(len(Arrg)):
                if d[len(d)-1] == self.data.classes[k]:
                    Arrg[k] = Arrg[k] +1
        max = -1
        for k in range(len(Arrg)):
            if Arrg[k] > max:
                max = Arrg[k]
                self.ans = self.data.classes[k]


    # Primary training function
    def train(self, min_data):
        k = True
        T=self
        ex=[] # the exclusion list
        while k:
            c = T.biggestE(min_data,ex) #find candidate node
            if c[0] == -1:  #Checks one was found
                k=False
            else:
                b= c[0]  #the node
                m = b.findsplit(min_data)  #Finds best split
                k = b.split(m,min_data) #Tries split
                if k=='badsplit':
                    ex.append(b) #add bad splits to the exclusion list
                    k=True


        #T.dis()

    def testSet(self,D):
        ans = []
        for d in D.Data:
            ans.append((self.test(d),d[len(d)-1]))
        return ans

    def test(self, d):
        if self.value==0:
            return  self.ans
        if d[self.value[1]] <= self.value[0]:
            return self.Nodes[0].test(d)
        return self.Nodes[1].test(d)


    def Accuracy(self,A):
        n,d=0,0
        for a in A:
            if a[1]==a[0]:
                n=n+1
            d=d+1
        return n/d

    def Precision(self,A,string):
        n,d=0,0
        for a in A:
            if string == a[0]:
                if a[1]==a[0]:
                    n=n+1
                d=d+1
        return n/d


    def recall(self,A,string):
        n,d=0,0
        for a in A:
            if string==a[1]:
                if a[0]==a[1]:
                    n=n+1
                d=d+1
        return n/d
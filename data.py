import math
import random


class dataSet:
    header=[]
    Data=[]
    classes=[]


    def clone(self):
        d = dataSet('')
        d.header=self.header.copy()
        d.Data = self.Data.copy()
        d.classes = self.classes.copy()
        return d


    def fill(self,h,c):
        self.header = h.copy()
        self.classes = c.copy()

    def getTrain(self, size):
        d = dataSet('')
        d.header=self.header.copy()
        d.Data = []
        d.classes = self.classes.copy()
        for i in range(size):
            r=random.randint(0,len(self.Data)-1)
            d.Data.append(self.Data[r].copy())
            self.Data.remove(self.Data[r])
        return d

    def __init__(self, filepath):
        if filepath != '':
            file = open(filepath,"r")
            z = 1
            for line in file:
                x = line.split(",")
                if z==1:
                    self.header = x
                    z=2
                else:
                    x[len(x)-1] =  "".join(x[len(x)-1].split())
                    for i in range(len(x)-1):
                        x[i] = float(x[i])
                        self.Data.append(x)

            for d in self.Data:
                if d[len(d)-1] not in self.classes:
                    self.classes.append(d[len(d)-1])
        else:
            self.header=[]
            self.Data=[]
            self.classes=[]

    def minmax(self):
        if len(self.Data) == 0:
            return []
        x = [0]*(len(self.Data[0])-1)
        for i in range(len(x)):
            x[i] = [self.Data[0][i],self.Data[0][i]]
        for d in self.Data:
            for i in range(len(d) - 1):
                if d[i] > x[i][1]:
                    x[i][1]=d[i]
                if d[i] < x[i][0]:
                    x[i][0]=d[i]
        return x


    def columns(self, size):
        A = self.minmax()
        B=[0]*len(A)
        l = len(self.Data)//size
        bound = []
        for i in range(len(A)):
            bound.append([A[i][0]])
        for i in range(size):
            for k in range(len(A)):
                max = A[k][1]
                min = bound[k][len(bound[k])-1]
                x = (max+min)/2
                g = self.numin(bound[k][len(bound[k]) - 1], x, k)
                for q in range(400):
                    if g<l:
                        min=x
                        x= (max+x)/2
                    else:
                        max=x
                        x = (min+ x) / 2

                    g = self.numin(bound[k][len(bound[k]) - 1], x, k)
                bound[k].append(x)
        print(bound)
        ND = []
        for d in self.Data:
            nd = [0]*len(d)
            nd[len(d)-1] = d[len(d)-1]
            for k in range(len(bound)):
                for j in range(len(bound[k])):
                    if d[k] >= bound[k][j]:
                        nd[k] = nd[k] + 1
            ND.append(nd)
        self.Data=ND

    def numin(self,x,l,k):
        c=0
        for d in self.Data:
            if x<=d[k] and d[k] < l:
                c=c+1
        return c

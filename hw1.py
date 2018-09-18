from data import dataSet
from Tree import Tree


file=r"C:\Users\Donald Trump\Downloads\BiomechanicalData_column_3C_weka.csv"
file2=r"C:\Users\Donald Trump\Downloads\Biomechanical_Data_column_2C_weka.csv"
min_data = 12
trainsize = 210
testSize = 100
trials=1

total=0

for i in range(trials):
    D = dataSet(file2)
    T = Tree(D.getTrain(trainsize))


    T.Display(0)

    T.train(min_data)

    T.Display(0)

    ans = T.testSet(D.getTrain(testSize))

    print('Accuracy = {}'.format(T.Accuracy(ans)))
    for c in T.data.classes:
        print('Precision on {} = {}'.format(c,T.Precision(ans, c)))
    for c in T.data.classes:
        print('Recall on {} = {}'.format(c,T.recall(ans, c)))



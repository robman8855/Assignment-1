from data import dataSet
from Tree import Tree


file=r"path here"
min_data_per_node = 12
trainsize = 210
testSize = 100
trials=1

total=0

for i in range(trials):
    D = dataSet(file)
    T = Tree(D.getTrain(trainsize))


    T.Display(0)

    T.train(min_data_per_node)

    T.Display(0)

    ans = T.testSet(D.getTrain(testSize))

    print('Accuracy = {}'.format(T.Accuracy(ans)))
    for c in T.data.classes:
        print('Precision on {} = {}'.format(c,T.Precision(ans, c)))
    for c in T.data.classes:
        print('Recall on {} = {}'.format(c,T.recall(ans, c)))



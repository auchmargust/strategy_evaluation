import numpy as np

class BagLearner(object):
    def __init__(self, learner, verbose = False, kwargs={"leaf_size":1,"verbose":False}, bags=20, boost=False,):
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learner_list = [learner(**kwargs) for _ in range(0,bags)]

    def author(self):
        return 'jfeng89'

    def add_evidence(self, data_x, data_y):
        for learner in self.learner_list:
            n = np.random.choice(data_x.shape[0],data_x.shape[0],replace=True)
            bag_x = data_x[n]
            bag_y = data_y[n]
            learner.add_evidence(bag_x, bag_y)

    def query(self,Xtest):
        if self.verbose:
            print(f"Current Tree:{self.tree}")
        else:
            pass
        result = []
        for learner in self.learner_list:
            result.append(learner.query(Xtest))
        Y = np.mean(result,axis=0)
        return Y

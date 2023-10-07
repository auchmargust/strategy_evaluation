import numpy as np
class DTLearner(object):

    def __init__(self, leaf_size, verbose=False):
        self.tree = None
        self.leaf_size = leaf_size
        self.verbose = verbose

    def verbose(self):
        if self.verbose:
            print(f"Current Tree:{self.tree}")
        else:
            pass

    def author(self):
        return 'jfeng89'
    
    def add_evidence(self,data_x,data_y):
        new_data_y = np.transpose(np.array([data_y]))
        train_data = np.append(data_x,new_data_y,axis=1)
        self.tree = self.build_tree(train_data)

    def query(self,Xtest):
        return np.array([self.predict(sample) for sample in Xtest])

    def predict(self,sample):
        row = 0
        #while not reaching the leaf
        while self.tree[row][0] != 'leaf':
            SplitIndex = int(float(self.tree[row][0]))
            SampleValue = sample[SplitIndex]
            TreeSplitValue = float(self.tree[row][1])

            # Go to Left Sub Tree
            if SampleValue <= TreeSplitValue:
                # Continue moving down on the left sub tree
                row += int(float(self.tree[row][2]))
            # Go to right Sub Tree
            else:
                # Continue moving down on the right sub tree
                row += int(float(self.tree[row][3]))
        return float(self.tree[row][1])

    def build_tree(self,data):
        #Corner Cases
        if data.shape[0]<=self.leaf_size or np.all(data[:,-1]==data[:,-1][0]):
            return np.array([['leaf',np.mean(data[:,-1]),np.nan,np.nan]])

        else:
            #Find the best feature to split on
            SplitIndex = self.get_best_feature(data)

            #Determine the split value using median
            SplitVal=np.median(data[:,SplitIndex])

            # If split value is the largest, then empty right tree.
            if SplitVal==max(data[:,SplitIndex]):
                return np.array([['leaf',np.mean(data[:,-1]),np.nan,np.nan]])

            #Build the tree recusirvely
            lefttree = self.build_tree(data[data[:,SplitIndex]<=SplitVal])
            righttree = self.build_tree(data[data[:,SplitIndex]>SplitVal])
            root = np.array([[SplitIndex,SplitVal,1,lefttree.shape[0]+1]])
            return np.vstack((root,lefttree,righttree))

    def get_best_feature(self,data):
        #Get X and Y
        dataY = data[:,-1]
        dataX = data[:,:-1]
        FeatureCorrList = {}

        #Calculate each feature's correlation coefficient with y.
        for FeatureIndex in range(0,dataX.shape[1]):
            CorrMatrix = np.corrcoef(dataX[:,FeatureIndex],dataY)
            FeatureCorr = abs(CorrMatrix[0,1])
            FeatureCorrList.update({FeatureIndex:FeatureCorr})

        #Find the best feature as the one with largest feature correlation
        BestFeature = max(FeatureCorrList,key=FeatureCorrList.get)
        return BestFeature










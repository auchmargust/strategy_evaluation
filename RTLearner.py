import random
import numpy as np
import pandas as pd
from scipy.stats import stats


class RTLearner(object):
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

    def add_evidence(self, data_x, data_y):
        # new_data_y = np.array([data_y])
        train_data = pd.concat((data_x,data_y),axis=1,)
        self.tree = self.build_tree(train_data)

    def query(self, Xtest):
        return np.array([self.predict(sample) for i, sample in Xtest.iterrows()])

    def predict(self, sample):
        row = 0
        # while not reaching the leaf
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

    def build_tree(self, data):
        # Corner Cases
        if data.shape[0] <= self.leaf_size or np.all(data.iloc[:, -1] == data.iloc[:, -1][0]):
            mode = stats.mode(data.iloc[:,-1])[0]
            return np.array([['leaf', mode, np.nan, np.nan]])

        else:
            SplitIndex = np.random.randint(0,data.shape[1]-1)

            # Determine the split value using median
            randomIndex1 = random.randint(0, data.shape[0]-1)
            randomIndex2 = random.randint(0, data.shape[0]-1)
            SplitVal = (data.iloc[randomIndex1, SplitIndex]+data.iloc[randomIndex2, SplitIndex])/2

            # If split value is the largest, then empty right tree.
            if SplitVal == max(data.iloc[:, SplitIndex]):
                mode = stats.mode(data.iloc[:, -1])[0]
                return np.array([['leaf', mode, np.nan, np.nan]])

            # Build the tree recusirvely
            lefttree = self.build_tree(data.loc[data.iloc[:, SplitIndex] <= SplitVal])
            righttree = self.build_tree(data.loc[data.iloc[:, SplitIndex] > SplitVal])
            root = np.array([[SplitIndex, SplitVal, 1, lefttree.shape[0] + 1]])
            return np.vstack((root, lefttree, righttree))

    if __name__ == "__main__":
        print("the secret clue is 'zzyzx'")








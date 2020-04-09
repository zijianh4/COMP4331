import pandas as pd
import numpy as np
import time
import math

train_data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_2/train.txt')
test_data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_2/test.txt')

class Node:
    def __init__(self, samples):
        self.children = {}                         
        self.split_attribute = None
        self.samples = samples
        self.NURS = None

class Decision_Tree:
    def __init__(self, data):
        self.root = Node(data)
    
    # function to build decision tree recursively
    def build_Decision_Tree(self, node):
        # situation when all samples in the node belongs to the same class
        if len(node.samples['NURSERY'].unique()) == 1:
            node.NURS = node.samples['NURSERY'].unique()[0]
            return
        
        # situation when there is no remaining attributes for further partitioning 
        if len(node.samples.columns) == 1:
            node.NURS = node.samples.mode()['NURSERY']
            return
        
        # start of split the node
        # find the best attibute to split
        split_table = {}
        for attribute in node.samples.columns:
            if attribute != 'NURSERY':  
                possible_values = node.samples[attribute].unique()
                info_after_split = 0
                split_info = 0
                for value in possible_values:
                    info_after_split += len(node.samples[node.samples[attribute] == value]) / len(node.samples) * self.info(node.samples[node.samples[attribute] == value])
                    split_info -= len(node.samples[node.samples[attribute] == value]) / len(node.samples) * math.log(len(node.samples[node.samples[attribute] == value]) / len(node.samples), 2)
                split_table[attribute] = (self.info(node.samples)-info_after_split) / split_info
        node.split_attribute = max(split_table, key=split_table.get)
        
        # split the node
        for value in node.samples[node.split_attribute].unique():
            node.children[value] = Node((node.samples[node.samples[node.split_attribute] == value]).drop([node.split_attribute], axis = 1))
            self.build_Decision_Tree(node.children[value])
            
    # function to calculate entropy of a dataframe     
    def info(self, data):
        temp = data['NURSERY'].value_counts()
        prob_vector = temp / temp.sum()
        prob_vector_np = prob_vector.to_numpy()
        entropy = -np.sum(prob_vector_np * np.log2(prob_vector_np))
        return entropy
        
    # function to classify a new data point
    def classify(self, node, data):
        if node.NURS != None:
            return node.NURS
        else:
            return self.classify(node.children[data[node.split_attribute]], data)
        
train_start = time.time()
Decision_Tree = Decision_Tree(train_data)
Decision_Tree.build_Decision_Tree(Decision_Tree.root)
train_end = time.time()

test_start = time.time()
for i in range(len(test_data)):
    print(Decision_Tree.classify(Decision_Tree.root, test_data.iloc[i]))
test_end = time.time()

print('The training time is ' + str(train_end - train_start) + ' seconds.')
print('The testing time is ' + str(test_end - test_start) + ' seconds.')
# import libraries
import time
import pandas as pd

# read data
train_data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_2/train.txt')
test_data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_2/test.txt')

# function to calculate likelihood
def likelihood_function(data, parents, has_nurs, form, children, housing, finance, social, health, NURSERY):
    part_data = data[data['NURSERY'] == NURSERY]
    likelihood_1 = len(part_data[part_data['parents'] == parents]) / len(part_data)
    likelihood_2 = len(part_data[part_data['has_nurs'] == has_nurs]) / len(part_data)
    likelihood_3 = len(part_data[part_data['form'] == form]) / len(part_data)
    likelihood_4 = len(part_data[part_data['children'] == children]) / len(part_data)
    likelihood_5 = len(part_data[part_data['housing'] == housing]) / len(part_data)
    likelihood_6 = len(part_data[part_data['finance'] == finance]) / len(part_data)
    likelihood_7 = len(part_data[part_data['social'] == social]) / len(part_data)
    likelihood_8 = len(part_data[part_data['health'] == health]) / len(part_data)
    return likelihood_1 * likelihood_2 * likelihood_3 * likelihood_4 * likelihood_5 * likelihood_6 * likelihood_7 * likelihood_8

# functino to calculate evidence
def evidence_function(data, parents, has_nurs, form, children, housing, finance, social, health):
    evidence_1 = len(data[data['parents'] == parents]) / len(data)
    evidence_2 = len(data[data['has_nurs'] == has_nurs]) / len(data)
    evidence_3 = len(data[data['form'] == form]) / len(data)
    evidence_4 = len(data[data['children'] == children]) / len(data)
    evidence_5 = len(data[data['housing'] == housing]) / len(data)
    evidence_6 = len(data[data['finance'] == finance]) / len(data)
    evidence_7 = len(data[data['social'] == social]) / len(data)
    evidence_8 = len(data[data['health'] == health]) / len(data)
    return evidence_1 * evidence_2 * evidence_3 * evidence_4 * evidence_5 * evidence_6 * evidence_7 * evidence_8

# function of Naive Bayes Classifier
def Naive_Bayes(train_data):
    result = {}
    for parents in train_data['parents'].unique():
        for has_nurs in train_data['has_nurs'].unique():
            for form in train_data['form'].unique():
                for children in train_data['children'].unique():
                    for housing in train_data['housing'].unique():
                        for finance in train_data['finance'].unique():
                            for social in train_data['social'].unique():
                                for health in train_data['health'].unique():
                                    candidate_class = {}
                                    for NURSERY in train_data['NURSERY'].unique():
                                        likelihood = likelihood_function(train_data, parents, has_nurs, form, children, housing, finance, social, health, NURSERY)
                                        prior = len(train_data[train_data['NURSERY'] == NURSERY])
                                        evidence = evidence_function(train_data, parents, has_nurs, form, children, housing, finance, social, health)
                                        posteriori = likelihood * prior / evidence
                                        candidate_class[NURSERY] = posteriori
                                    result_class = max(candidate_class, key=candidate_class.get)
                                    result[tuple([parents, has_nurs, form, children, housing, finance, social, health])] = result_class
    return result

# train the Naive Bayes Classifier
train_start = time.time()
NB_result = Naive_Bayes(train_data)
train_end = time.time()

# test the Naive Bayes Classifier
test_start = time.time()
for i in range(len(test_data)):
    print(NB_result[tuple(test_data.iloc[i].tolist())])
test_end = time.time()

print('The training time is ' + str(train_end - train_start) + ' seconds.')
print('The testing time is ' + str(test_end - test_start) + ' seconds.')
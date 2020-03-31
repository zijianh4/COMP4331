import time
# data preprocessing
ins = open('a1dataset.txt', 'r')
data = []
for line in ins:
    number_strings = line.split() # Split the line on runs of whitespace
    numbers = [int(n) for n in number_strings] # Convert to integers
    data.append(numbers) # Add the "row" to your list
    
# function to generate the frequent items
def generate_item(data, minsup):
    items = {}
    for transaction in data:
        for i in transaction:
            if i in items:
                items[i] += 1
            else:
                items[i] = 1
    
    frequent_items = []
    for item in items:
        if items[item] >= minsup:
            frequent_items.append([item])
    return frequent_items

# function to generate a new candidate by merging two itemsets
def generate_candidate(itemset_1, itemset_2):
    new_itemset = []
    for i in range(len(itemset_1) - 1):
        new_itemset.append(itemset_1[i])
    if (itemset_1[-1] < itemset_2[-1]):
        new_itemset.append(itemset_1[-1])
        new_itemset.append(itemset_2[-1])
    else:
        new_itemset.append(itemset_2[-1])
        new_itemset.append(itemset_1[-1])
    return new_itemset

# function to check whether the first k-1 items of two itemsets of length k are the same
def check(itemset_1, itemset_2):
    for i in range(len(itemset_1) - 1):
        if itemset_1[i] != itemset_2[i]:
            return False
    return True
    
# function to generate candidates of size (k+1) by merging two frequent itemsets of length k
def generate_candidates(old_candidates):
    new_candidates = []
    for i in range(len(old_candidates)):
        for j in range(i+1, len(old_candidates)):
            if check(old_candidates[i], old_candidates[j]):
                new_itemset = generate_candidate(old_candidates[i], old_candidates[j])
                new_candidates.append(new_itemset)
    return new_candidates

# function to check whether two itemsets of length k are the same
def equal(itemset_1, itemset_2):
    for i in range(len(itemset_1)):
        if itemset_1[i] != itemset_2[i]:
            return False
    return True

# function to check whether an itemset has infrequent subsets
def check_subset(itemset, old_candidates):
    for i in range(len(itemset)):
        subset = list()
        for j in range(len(itemset)):
            if i != j:
                subset.append(itemset[j])
        find = False
        for old_candidate in old_candidates:
            if equal(subset, old_candidate):
                find = True
                break
        if find == False:
            return False
    return True

# function to prune candidates which has infrequent subsets
def prune(candidates, old_candidates):
    after_prune_result = []
    for itemset in candidates:
        if check_subset(itemset, old_candidates):
            after_prune_result.append(itemset)
    return after_prune_result

# function to check whether an itemset appear in a transaction or not
def find_in_record(itemset, transaction):
    for item in itemset:
        if item not in transaction:
            return False
    return True

# function to count the support of an itemset
def count(itemset, data):
    counter = 0
    for transaction in data:
        if find_in_record(itemset, transaction):
            counter += 1
    return counter

# the main function of apriori algorithm
def apriori(data, minsup):
    Lk = generate_item(data, minsup)
    freq_itemsets = []
    for i in Lk:
        freq_itemsets.append(i)
    while(len(Lk) > 0):
        candidate_k = generate_candidates(Lk)
        candidate_k = prune(candidate_k, Lk)
        Lk = []
        for itemset in candidate_k:
            if count(itemset, data) >= minsup:
                Lk.append(itemset)
                freq_itemsets.append(itemset)
    return freq_itemsets

start = time.time()
frequent_itemsets = apriori(data,400)
end = time.time()
time_taken = end - start
print("The time taken is " + str(time_taken))
print("The number of frequent itemset is " + str(len(frequent_itemsets)) + ", which are")
print(frequent_itemsets)
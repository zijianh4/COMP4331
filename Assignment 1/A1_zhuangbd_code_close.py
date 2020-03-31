import itertools
import time

ins = open('a1dataset.txt', 'r')
data = []
for line in ins:
    number_strings = line.split() # Split the line on runs of whitespace
    numbers = [int(n) for n in number_strings] # Convert to integers
    data.append(numbers) # Add the "row" to your list
minsup = 400

# function to generate the frequent items
def frequent_one_item(data, minsup):
    items = {}
    for record in data:
        for i in record:
            if i in items:
                items[i] = items[i] + 1
            else:
                items[i] = 1
                
    frequent_items = []
    for item in items:
        if items[item] >= minsup:
            frequent_items.append([item])
    return frequent_items

# class of Hash node
class Hash_node:
    def __init__(self):
        self.children = {}           
        self.leaf_status = True      
        self.bucket = {}             

# class of hash tree
class HashTree:
    def __init__(self, max_leaf_count, max_child_count):
        self.root = Hash_node()
        self.max_leaf_count = max_leaf_count
        self.max_child_count = max_child_count
        self.frequent_itemsets = []
    
    # hash function for making HashTree
    def hash_function(self, val):
        return int(val) % self.max_child_count
    
    # function to recursive insertion to make hashtree
    def recursive_insert(self, node, itemset, index, count):
        # if reaching the max depth of the tree
        if index == len(itemset):
            if itemset in node.bucket:
                node.bucket[itemset] += count
            else:
                node.bucket[itemset] = count
            return

        # if node is leaf
        if node.leaf_status:                             
            if itemset in node.bucket:
                node.bucket[itemset] += count
            else:
                node.bucket[itemset] = count
            # if bucket capacity increases
            if len(node.bucket) == self.max_leaf_count:  
                for old_itemset, old_count in node.bucket.items():

                    hash_key = self.hash_function(old_itemset[index])  
                    if hash_key not in node.children:
                        node.children[hash_key] = Hash_node()
                    self.recursive_insert(node.children[hash_key], old_itemset, index + 1, old_count)

                del node.bucket
                node.leaf_status = False
        #if node is not leaf
        else:                                            
            hash_key = self.hash_function(itemset[index])
            if hash_key not in node.children:
                node.children[hash_key] = Hash_node()
            self.recursive_insert(node.children[hash_key], itemset, index + 1, count)

    def insert(self, itemset):
        itemset = tuple(itemset)
        self.recursive_insert(self.root, itemset, 0, 0)

    # funnction to add support to candidate itemsets. 
    def add_support(self, itemset):
        transverse_node = self.root
        itemset = tuple(itemset)
        index = 0
        while True:
            if transverse_node.leaf_status:
                if itemset in transverse_node.bucket:    
                    transverse_node.bucket[itemset] += 1 
                break
            hash_key = self.hash_function(itemset[index])
            if hash_key in transverse_node.children:
                transverse_node = transverse_node.children[hash_key]
            else:
                break
            index += 1

    # to transverse the hashtree to get frequent itemsets with minimum support count
    def get_frequent_itemsets(self, node, support_count, frequent_itemsets):
        if node.leaf_status:
            for key, value in node.bucket.items():
                if value >= support_count:                       #if it satisfies the condition
                    frequent_itemsets.append(list(key))          #then add it to frequent itemsets.
            return

        for child in node.children.values():
            self.get_frequent_itemsets(child, support_count, frequent_itemsets)

# function to generate length (k-1) subset of candidate of length k
def subset_generation(candidate_k_data, l):
    return map(list, set(itertools.combinations(candidate_k_data, l)))  

# apriori generate function to generate candidate of length k
def apriori_generate(dataset, k):
    candidate_k = []
    #join step
    len_lk = len(dataset)
    for i in range(len_lk):
        for j in range(i+1, len_lk):
            L1 = list(dataset[i])[:k - 2]
            L2 = list(dataset[j])[:k - 2]
            if L1 == L2:
                candidate_k.append(sorted(list(set(dataset[i]) | set(dataset[j]))))

    #prune step
    final_candidate_k = []
    for candidate in candidate_k:
        all_subsets = list(subset_generation(set(candidate), k - 1))
        found = True
        for i in range(len(all_subsets)):
            value = list(sorted(all_subsets[i]))
            if value not in dataset:
                found = False
        if found == True:
            final_candidate_k.append(candidate)

    return candidate_k,final_candidate_k

# function to generate hash tree from candidate itemsets
def generate_hash_tree(candidate_itemsets, max_leaf_count, max_child_count):
    htree = HashTree(max_child_count, max_leaf_count)             #create instance of HashTree
    for itemset in candidate_itemsets:
        htree.insert(itemset)                                     #to insert itemset into Hashtree
    return htree

# function to generate subsets of itemsets of size k
def generate_k_subsets(dataset, length):
    subsets = []
    for itemset in dataset:
        subsets.extend(map(list, itertools.combinations(itemset, length)))
    return subsets

values = frequent_one_item(data, minsup)

# remove infrequent 1 itemsets from transactions
data_1 = []
for i in range(0, len(data)):
    list_value = []
    for j in range(0, len(data[i])):
        if [data[i][j]] in values:
            list_value.append(data[i][j])
    data_1.append(list_value)
    
# main apriori algorithm function
def apriori(L1, minsup):
    k = 2;
    L = []
    L.append(0)
    L.append(L1)
    #maximum number of items in bucket
    max_leaf_count = 10
    #maximum number of child you want for a node
    max_child_count = 3

    start = time.time()
    while(len(L[k-1]) > 0):
        candidate_k, final_candidate_k = apriori_generate(L[k-1], k)                 # generate candidate itemsets
        h_tree = generate_hash_tree(candidate_k, max_leaf_count, max_child_count)       # generate hash tree
        k_subsets = generate_k_subsets(data_1, k)                  # generate subsets of each transaction
        for subset in k_subsets:
            h_tree.add_support(subset)                                  # add support count to itemsets in hashtree
        lk = []
        h_tree.get_frequent_itemsets(h_tree.root, minsup, lk)                  #get frequent itemsets
        L.append(lk)
        k = k + 1
    end = time.time()
    return L, (end-start)


L_value, time_taken = apriori(values, minsup)

# check whether an itemset appear in a record or not
def find_in_record(itemset, record):
    for item in itemset:
        if item not in record:
            return False
    return True

# count the support of an itemset
def count(itemset, data):
    counter = 0
    for record in data:
        if find_in_record(itemset, record):
            counter += 1
    return counter

# function to check supsets relationship
def check_sup(itemset, sup_itemset):
    return set(itemset).issubset(set(sup_itemset))

# function to check whether an itemset is closed
def check_closed(itemset):
    k = len(itemset)
    flag = True
    for sup_itemset in L_value[k+1]:
        if check_sup(itemset, sup_itemset) == True:
            if count(itemset, data) > count(sup_itemset, data):
                flag = True
            else:
                flag = False
                break
    return flag

# find frequent closed itemsets
closed_frequent_itemset = []
for i in range(len(L_value)):
    if i != 0:
        itemsets = L_value[i]
        for itemset in itemsets:
            if check_closed(itemset) == True:
                closed_frequent_itemset.append(itemset)
                
print("Closed frequent itemsets are")
print(closed_frequent_itemset)

# function to check whether an itemset is maximal frequent
def check_maximal(itemset):
    k = len(itemset)
    flag = True
    for sup_itemset in L_value[k+1]:
        if check_sup(itemset, sup_itemset) == True:
            flag = False
            break
    return flag

# find maximal frequent itemsets
maximal_frequent_itemsets = []
for i in range(len(L_value)):
    if i != 0:
        itemsets = L_value[i]
        for itemset in itemsets:
            if check_maximal(itemset) == True:
                maximal_frequent_itemsets.append(itemset)

print("Maximal frequent itemsets are")
print(maximal_frequent_itemsets)
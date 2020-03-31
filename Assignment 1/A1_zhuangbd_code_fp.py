import time

ins = open('a1dataset.txt', 'r')
data = []
for line in ins:
    number_strings = line.split() # Split the line on runs of whitespace
    numbers = [int(n) for n in number_strings] # Convert to integers
    data.append(numbers) # Add the "row" to your list
    
# class of FP Tree node
class Node:
    def __init__(self, node_name, count, parent_node):
        self.name = node_name
        self.count = count
        self.node_link = None
        self.parent = parent_node
        self.children = {}
        
# class of FP growth
class Fp_growth():
    # function to update header table
    def update_header(self, node, target_node):
        # go through the node link
        while node.node_link != None:
            node = node.node_link
        node.node_link = target_node
    
    # function to update FP tree
    def update_fptree(self, itemset, node, header_table):
        # when the item is a child
        if itemset[0] in node.children:
            node.children[itemset[0]].count += 1
        # when the item is not a child
        else:
            # add it to the children
            node.children[itemset[0]] = Node(itemset[0], 1, node)
            # update the header table
            if header_table[itemset[0]][1] == None:
                header_table[itemset[0]][1] = node.children[itemset[0]]
            else:
                self.update_header(header_table[itemset[0]][1], node.children[itemset[0]])
                
        if len(itemset) > 1:
            self.update_fptree(itemset[1:], node.children[itemset[0]], header_table)

    # function to create FP Tree
    def create_fptree(self, data_set, min_support):
        # count the items in the dataset
        item_count = {}
        for transaction in data_set:
            for item in transaction:
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
        
        # collect the frequent items
        header_table = {}
        for k in item_count:
            if item_count[k] >= min_support:
                header_table[k] = item_count[k]

        frequent_itemset = set(header_table.keys())
        
        # if there is no frequent item
        if len(frequent_itemset) == 0:
            return None, None
        
        #initiate the header table
        for k in header_table:
            header_table[k] = [header_table[k], None] 
        tree_header = Node('head node', 1, None)
            
        # build FP Tree
        for transaction in data_set:
            local_dic = {}
            for item in transaction:
                if item in frequent_itemset: 
                    local_dic[item] = header_table[item][0] 
            if len(local_dic) > 0:
                # order the itemset
                order_item = [value[0] for value in sorted(local_dic.items(), key=lambda x:x[1], reverse=True)]
                # update the FP Tree
                self.update_fptree(order_item, tree_header, header_table)
        return tree_header, header_table

    # function to generate node path by adding parent nodes one by one
    def generate_path(self, node, node_path):
        if node.parent != None:
            node_path.append(node.parent.name)
            self.generate_path(node.parent, node_path)
    
    # function to find all frequent path of a node
    def find_cond_base(self, node_name, header_table):
        tree_node = header_table[node_name][1]
        cond_base = {}
        while tree_node != None:
            node_path = []
            self.generate_path(tree_node, node_path)
            if len(node_path) > 1:
                cond_base[frozenset(node_path[:-1])] = tree_node.count 
            tree_node = tree_node.node_link 
        return cond_base

    # function to generate connditional FP Tree
    def create_cond_fptree(self, header_table, min_support, temp, frequent_items, support_data):
        freqs = [value[0] for value in sorted(header_table.items(), key=lambda p:p[1][0])]
        
        for freq in freqs:
            frequent_set = temp.copy()
            frequent_set.add(freq)
            frequent_items.add(frozenset(frequent_set))
            
            if frozenset(frequent_set) not in support_data:
                support_data[frozenset(frequent_set)]=header_table[freq][0]
            else:
                support_data[frozenset(frequent_set)]+=header_table[freq][0]

            cond_base = self.find_cond_base(freq, header_table)
            cond_dataset = []
            for item in cond_base:
                item_temp = list(item)
                item_temp.sort()
                for i in range(cond_base[item]):
                    cond_dataset.append(item_temp)
            
            # recursively FP Tree
            cond_tree, current_headtable = self.create_fptree(cond_dataset, min_support)
            if current_headtable != None:
                self.create_cond_fptree(current_headtable, min_support, frequent_set, frequent_items,support_data) 

    def generate_freq_itemsets(self, data_set, min_support):
        frequent_itemset = set()
        support_data = {}
        tree_header, header_table = self.create_fptree(data_set, min_support)
        self.create_cond_fptree(header_table, min_support, set(), frequent_itemset,support_data)
        
        # put frequent itemsets into result
        max_l = 0
        for i in frequent_itemset:
            if len(i)>max_l:max_l=len(i)
        result = [set() for _ in range(max_l)]
        for i in frequent_itemset:
            result[len(i)-1].add(i)
        
        return result, support_data 
    
min_support = 400
fp = Fp_growth()
start = time.time()
frequent_itemsets, support_data = fp.generate_freq_itemsets(data, min_support)
end = time.time()
print("Time spent: " + str(end - start))
print(frequent_itemsets)
import csv
import math


# eg. {'1':['1','0']} which means there is one attribute called '1', and it has two possible values, '0' and '1'.
# in this program, because there are 1600 attributes, I will use a function to modify this dict, and leave it empty now.
attribute_key = {}
target_attribute = ''
numeric_attributes = []
useless_attribute = []

# a node class, attribute will record how the entire data have been sorted
# dataSet is the dataSet after the entire dataSet have been sorted in the way that is recorded in attribute
# entropy is calculated based on the dataSet, when it reaches 0.0, it means that the dataset is pure
# uptree is the connection to the uptree, it could be a node class or None
# subtree is the connection to the subtree, it could be a list of node class or []
class node():
    def __init__(self, attribute, dataSet, uptree=None):
        self.dataSet = dataSet
        self.attribute = attribute
        self.entropy = getEntropy(dataSet)
        self.uptree = uptree
        self.subtree = []

    def __str__(self):
        result = 'Attributes: ' + str(self.attribute) + '\nentropy: ' + str(self.entropy)
        result += '\nuptree: '
        if self.uptree is None:
            result += str(self.uptree) + '\nsubtree: \n' + self.print_subtree()
        else:
            result += str(self.uptree.attribute) + ' ' + str(
                self.uptree.entropy) + '\nsubtree: \n' + self.print_subtree() + '\n'
            index = list(attribute_key.keys()).index(target_attribute)
        return result

    def print_subtree(self):
        if self.subtree == []:
            return 'None'
        else:
            result = ''
            for i in range(len(self.subtree)):
                result += (str(i) + '. ' + str(self.subtree[i].attribute) + ' ' + str(self.subtree[i].entropy) + '\n')
            return result

    # show how many of each target value is in the dataset
    def show_result(self):
        number = {}
        index = list(attribute_key.keys()).index(target_attribute)
        for i in self.dataSet:
            if i[index] in number:
                number[i[index]] += 1
            else:
                number[i[index]] = 1
        print(number)


# get the entropy of a dataSet
def getEntropy(dataSet):
    number = {}
    index = list(attribute_key.keys()).index(target_attribute)
    for i in dataSet:
        if i[index] in number:
            number[i[index]] += 1
        else:
            number[i[index]] = 1
    total = len(dataSet)
    entropy = 0
    for i in number:
        entropy -= (number[i] / total * math.log((number[i] / total), 2))
    return entropy


# get the entropy of a divided dataSet, this can be used to calculate the information gain
def getDivideSetEntropy(dividedSet):
    entropy = 0
    total = 0
    for i in dividedSet:
        entropy += len(i) * getEntropy(i)
        for j in i:
            total += 1
    entropy /= total
    return entropy


# if the second parameter is left blank
# this function will choose the attribute that can most efficiently divide the dataSet of an old_node
# and attach the new_node that are generated to the old_node
# if the second parameter is not blank
# this function will use the attribute provided to sort the data and do the same thing as before
def choose_attribute(old_node, minnum=0, maxdepth=-1, final_attribute=''):
    nodes = []
    if final_attribute != '':
        dividedSet = divideDataSet(old_node.dataSet, final_attribute)
        for singleSet in range(len(dividedSet)):
            entropy = getDivideSetEntropy(dividedSet)
            new_node_attribute = old_node.attribute.copy()
            new_node_attribute[final_attribute] = attribute_key[final_attribute][singleSet]
            new_node = node(new_node_attribute, dividedSet[singleSet], old_node)
            nodes.append(new_node)
    else:
        unusedAttributes = list(attribute_key.keys() - old_node.attribute.keys() - set(numeric_attributes) -
                                set(useless_attribute))
        unusedAttributes.remove(target_attribute)
        entropy = 100
        final_attribute = ''
        if unusedAttributes == set() or old_node.entropy == 0.0 or \
                (len(old_node.attribute) == maxdepth and maxdepth > -1) :
            return []
        for attribute in unusedAttributes:
            dividedSet = divideDataSet(old_node.dataSet, attribute)
            ifcontinue = False
            for i in dividedSet:
                if len(i) < minnum:
                    ifcontinue = True
                    break
            if ifcontinue:
                continue
            if entropy > getDivideSetEntropy(dividedSet):
                nodes = []
                entropy = getDivideSetEntropy(dividedSet)
                final_attribute = attribute
                for singleSet in range(len(dividedSet)):
                    new_node_attribute = old_node.attribute.copy()
                    new_node_attribute[attribute] = attribute_key[attribute][singleSet]
                    new_node = node(new_node_attribute, dividedSet[singleSet], old_node)
                    nodes.append(new_node)
        if entropy == old_node.entropy:
            return []
    if nodes != []:
        old_node.subtree = nodes
        print('\nSorting ' + str(old_node.attribute) + ' based on: ' + final_attribute + '\nentropy: ' + str(
            entropy) + '\ninformation gain: ' + str(old_node.entropy - entropy) + '\n')
    return nodes


# this is a driver that uses the functions to generate model and print how the dataSet is sorted
def computing(node_list, minnum, maxdepth):
    for i in node_list:
        print(str(i)[:-15])
    print('------------------------------------------')
    for i in node_list:
        result = choose_attribute(i, minnum, maxdepth)
        if result != []:
            computing(result, minnum, maxdepth)


# this will divide the dataSet according to the attribute provided, and return a list of dataSet that has been divided
def divideDataSet(dataset, attribute):
    index = list(attribute_key.keys()).index(attribute)
    possible = len(attribute_key[attribute])
    dividedSet = []
    for i in range(possible):
        dividedSet.append([])
    for i in dataset:
        dividedSet[attribute_key[attribute].index(i[index])].append(i)
    return dividedSet


# this function will take the root node of a model and return the information about the nodes that do not have subtree
def getLeaf(beginningNode, leaves):
    if beginningNode.subtree != []:
        for i in beginningNode.subtree:
            leaves += getLeaf(i, leaves)
        if beginningNode.uptree != None:
            return []
        else:
            return leaves
    else:
        index = list(attribute_key.keys()).index(target_attribute)
        attribute = beginningNode.attribute
        result = {}
        for i in beginningNode.dataSet:
            if i[index] in result:
                result[i[index]] += 1
            else:
                result[i[index]] = 1
        judge = ''
        number = 0
        for i in result:
            if result[i] > number:
                judge = i
                number = result[i]
        return [[attribute, judge, len(beginningNode.dataSet), number, beginningNode.entropy]]


# this function export a model to a txt file, there will be all the attribute and possible value, the target attribute
# and possible value, and the model that has been established (included attribute, predict result, number of occurrence,
# and entropy
def exportModel(beginningNode):
    file = open('model.txt', 'w', encoding='utf-8')
    file.write('attributes:\n')
    file.write(str(attribute_key) + '\n')
    file.write('numeric:\n')
    file.write(str(numeric_attributes) + '\n')
    leaves = getLeaf(beginningNode, [])
    file.write('result:\n')
    file.write(str(leaves))
    file.close()


# an interactive_mode, really did not write much about it, you can show the current node, show the subtree nodes,
# show the uptree nodes, move the current node, and sort the current node.
def interactive_mode(fileName, targetAttribute, numericAttributes):
    global target_attribute, numeric_attributes
    target_attribute = targetAttribute
    numeric_attributes = numericAttributes
    content = updateTrainingSet(fileName)
    if numeric_attributes !=[]:
        content = numeric(content, numeric_attributes)
    print(len(content))
    tree = node({}, content)
    # input
    words = input()
    # 'stop' will close the program
    while words != 'stop':
        # show the current node
        if words == 'show':
            print(tree)
        # show the upper node
        elif words == 'show upper':
            print(tree.uptree)
        # show the subtree
        elif words == 'show sub':
            print(tree.print_subtree())
        elif words == 'show result':
            tree.show_result()
        # move the current node up or down, if down, a list of subtree will show and you can make the selection
        elif words == 'move':
            direction = input('up or down: ')
            if direction == 'up':
                if tree.uptree != None:
                    tree = tree.uptree
                    print('moved')
                else:
                    print('no uptree')
            elif direction == 'down':
                if tree.subtree == []:
                    print('no subtree')
                else:
                    print(tree.print_subtree())
                    number = int(input('which subtree: '))
                    try:
                        tree = tree.subtree[number]
                        print('moved')
                    except:
                        print('invalid input')
        # sort the data according to a specific attribute, a list of possible attributes will show and you can make
        # selection
        elif words == 'sort':
            print('available sorting options')
            for i in range(len(attribute_key.keys())):
                print(str(i) + '. ' + (list(attribute_key)[i]))
            number = int(input('which option: '))
            try:
                attribute = list(attribute_key)[number]
                choose_attribute(tree, final_attribute=attribute)
                print('sorted')
            except:
                print('invalid input')
        # delete the subtree
        elif words == 'delete sub':
            tree.subtree = []
            print('deleted')
        words = input()


# make the prediction based on the existing model file (model.txt) and the input from test.csv
# if the prediction is wrong, enter the right value, and this prediction question will be moved to training set
def makePrediction(fileName):
    file = open('model.txt', 'r', encoding='utf-8')
    content = file.readlines()
    file.close()
    numeric_attributes = eval(content[3])
    feature = eval(content[5])
    with open(fileName + '.csv', encoding='utf-8', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            for result in feature:
                fit = True
                for attribute in result[0]:
                    if attribute.split('<=')[0] in numeric_attributes:
                        if float(data[attribute.split('<=')[0]]) > float(attribute.split('<=')[1]):
                            if result[0][attribute] == 'yes':
                                fit = False
                        else:
                            if result[0][attribute] == 'no':
                                fit = False
                    elif data[attribute] != result[0][attribute]:
                        fit = False
                if fit:
                    print('\n\n\n     Prediction: ' + result[1] + '\n\n\n')
        csvfile.close()
    return


# read the header and data in the csv file, and establish environment for training
def updateTrainingSet(fileName):
    with open(fileName + '.csv', encoding='utf-8', newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        attribute = next(reader)
        for i in attribute:
            attribute_key[i] = []
        csvfile.close()
    content = []
    with open(fileName + '.csv', encoding='utf-8', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            for attribute in data:
                if data[attribute] not in attribute_key[attribute]:
                    attribute_key[attribute].append(data[attribute])
            content.append(list(data.values()))
        csvfile.close()
    return content


# this function will turn numeric attributes into many individual dummy variable
def numeric(content, numeric_attributes):
    for numeric_attribute in numeric_attributes:
        index = list(attribute_key).index(numeric_attribute)
        valueSet = []
        for data in content:
            valueSet.append(data[index])
        valueSet = list(set(valueSet))
        valueSet.sort()
        for number in valueSet:
            attribute_key[numeric_attribute + '<=' + number] = ['yes', 'no']
        for data in content:
            for number in valueSet:
                if float(data[index]) <= float(number):
                    data.append('yes')
                else:
                    data.append('no')
    return content


# this function is used to train the data and export model
def training(fileName, targetAttribute, numericAttributes=[], useless=[], minnum=0, maxdepth=-1):
    global target_attribute, numeric_attributes, useless_attribute
    target_attribute = targetAttribute
    numeric_attributes = numericAttributes
    useless_attribute = useless
    content = updateTrainingSet(fileName)
    if numeric_attributes !=[]:
        content = numeric(content, numeric_attributes)
    tree = node({}, content)
    computing([tree], minnum, maxdepth)
    exportModel(tree)


# instruction:
#   training('bank-data', 'pep', numericAttributes=['income', 'age', 'children'], maxdepth=5, minnum=20)
#   This means:
#       the training set is bank-data.csv
#       pep is the target value (the predicted attribute)
#       numericAttributes is a list of numeric attributes, in the example it is income, age, number of children
#       useless is a list of attributes, which you do not want to include in the learning process
#       maxdepth is the maximum depth of the tree, in this case is 5
#	minnum is the minimum size of sorted dataSet in this case is 20
#
#   makePrediction('test')
#       This function will read the data in test.csv and make prediction based on model.txt in the root folder.


training('denver_dummy', 'Group', minnum=20)
#makePrediction('test')
#interactive_mode('bank-data', 'pep', numericAttributes=['children', 'income', 'age'])

import getch

class letterNode(object):  # The letter node

    def __init__(self, char):  # Char is the letter assigned to the node
        self.character = char  # Set self.character as the character
        self.children = []  # A list of all the words that have been added to the letter
        self.wordComplete = False  # Status of the word
        self.counter = 1  #Number of options
        self.completed=1

def add(letterNodeObject, word):
    """
    Adding a word in the trie structure
    """
    node = letterNodeObject
    for letter in word:
        foundInChild = False # Search for the character in the present node
        for child in node.children:
            if child.character == letter:  # If the node already exists
                child.counter += 1  # increase the counter
                node = child  # Move to this already created node
                foundInChild = True  # foundInChild so no need to create a new node
                break

        if not foundInChild:  # No previous node
            new_node = letterNode(letter)  # Create a new node with the next letter
            node.children.append(new_node)  # Append this new node ot the child list but only branching when necessary
            node = new_node # Move to the newly created node
    node.wordComplete = True

def find_prefix(parentNode, prefix):
    node = parentNode
    if not parentNode.children:  # If there is no children of the parent node
        return False, 0
    for letter in prefix:
        charNotFound = True
        for child in node.children:
            if child.character == letter:
                charNotFound = False  # We found the character
                node = child  # Move to the next node by assigning to that child
                break
        if charNotFound:  # If we did not find a prediction
            return False, 0
    return True, node.counter  #This means we found the prefix and how many words can be predicted

def readTrie(parentNode,prefix):
    node = parentNode
    if not parentNode.children:  # If there is no children of the parent node
        return False, 0
    for letter in prefix:
        charNotFound = True
        for child in node.children:
            if child.character == letter:
                charNotFound = False  # We found the character
                node = child  # Move to the next node by assigning to that child
                break
        if charNotFound:  # If we did not find a prediction
            return False, 0, ["No words available"]

    rootNode= node
    predictedWord=[]
    choices=node.counter
    # print("The number of possible choices = " + str(node.counter))
    # print("The number of available letter nodes = " + str(len(rootNode.children)))
    word=""
    while node.children:  # While there is children in the node
        if node.wordComplete == True:  # If word complete
            predictedWord.append(prefix + word)
            if len(node.children) == 1:  # Shortcut if there is only one option
                node = node.children[0]
                word += node.character

        if len(node.children) >= 1:  # Shortcut if there is only one option
            node = node.children[0]
            word += node.character


    predictedWord.append(prefix + word)
    return True,choices,predictedWord  # This means we found the prefix and how many words can be predicted


if __name__ == "__main__":
    root = letterNode('h')
    add(root, "hackthon")
    add(root, 'hack')
    add(root, "haca")
    add(root, 'hammer')
    phrase=""
    while True:
        input=getch.getch()
        try:
            if int(input)==0:
                phrase = phrase[:-1]
        except:
            phrase += input

        print(phrase)

        flag,options,words,=readTrie(root,phrase)
        print("There is " +str(options) +" predictions available.\n"
                                         "Press the corresponding number to autocomplete.\n"
                                         "The predictions are as follows:\n"
                                         "\t0. Backspace")
        for i in range(len(words)):
            print("\t" + str(i+1) + ". " + words[i])
            try:
                for i in range(len(words)):
                    if int(input)==i+1:
                        phrase=words[i]
            except:
                pass
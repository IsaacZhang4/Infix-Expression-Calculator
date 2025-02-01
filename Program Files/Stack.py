from Node import Node

class Stack:

    def __init__(self):
        self.top = None

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top, out))

    __repr__ = __str__

    def isEmpty(self):
        return self.top is None

    def __len__(self):
        count = 0
        currNode = self.top
        # Iterate through stack and add to count until bottom
        while currNode:
            count += 1
            currNode = currNode.next
        return count

    def push(self, value):
        newNode = Node(value)
        # Set next to current top node and then replace top with newNode
        newNode.next = self.top
        self.top = newNode

    def pop(self):
        topNode = self.top
        # If not empty, set top node to next
        if topNode:
            self.top = topNode.next
            return topNode.value
        # Return None is Empty
        return None

    def peek(self):
        topNode = self.top
        # If not empty, return top node value, else, return None
        if topNode:
            return topNode.value
        else:
            return None
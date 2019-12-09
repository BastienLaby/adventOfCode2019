# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, name, parent=None):
        assert parent is None or isinstance(parent, Node)
        self.parent = parent
        self.name = name
        self.children = []

    def addChild(self, child):
        assert isinstance(child, Node)
        child.parent = self
        self.children.append(child)

    def lengthToParent(self, parentName='COM'):
        node = self
        length = 0
        while node.name != parentName:
            length += 1
            node = node.parent
        return length

    @property
    def length(self):
        return self.lengthToParent()

    @property
    def parents(self):
        parents = []
        node = self
        while node.parent is not None:
            parents.append(node.parent)
            node = node.parent
        return parents

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def createTreeFromOrbitList(orbitList):

    nodeTree = {}
    for orbit in orbitList:
        parent, child = orbit.split(')')
        for p in [parent, child]:
            # here, we could use nodeTree.sedafault(p, Node(p)), but
            # the Node constructor will be called BEFORE the existence test of setdefault() functions
            # so its not very effective if we do heavy operations in Node __init__ function later
            if p not in nodeTree:
                nodeTree[p] = Node(p)
        nodeTree[parent].addChild(nodeTree[child])

    return nodeTree


def computeOrbitsChecksum(nodeTree):
    return sum([planet.length for planet in nodeTree.values()])


def getMinimumOrbitalTransfer(tree, src, dst):

    commonParent = list(set(tree[dst].parents) & set(tree[src].parents)))[0]
    if commonParent is None:
        print('No common parent found between %s and %s.' % (tree[src], tree[dst]))
        return

    return tree[src].lengthToParent(commonParent.name) - 1 + tree[dst].lengthToParent(commonParent.name) - 1

if __name__ == '__main__':

    data = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
        data = f.readlines()

    # puzzle 1 tests

    testTree = createTreeFromOrbitList(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'])
    assert 'COM' in testTree and testTree['COM'].parent is None
    assert computeOrbitsChecksum(testTree) == 42

    # puzzle 1 answer

    puzzleTree = createTreeFromOrbitList([i.strip() for i in data])
    assert 'COM' in puzzleTree and puzzleTree['COM'].parent is None
    print(computeOrbitsChecksum(puzzleTree))

    # puzzle 2 tests

    testTree = createTreeFromOrbitList(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN'])
    assert 'COM' in testTree and testTree['COM'].parent is None
    assert getMinimumOrbitalTransfer(testTree, 'YOU', 'SAN') == 4
    assert getMinimumOrbitalTransfer(testTree, 'YOU', 'SAN') ==  getMinimumOrbitalTransfer(testTree, 'SAN', 'YOU')

    # puzzle 2 answer

    print(getMinimumOrbitalTransfer(tree, 'YOU', 'SAN'))

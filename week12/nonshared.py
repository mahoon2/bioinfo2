import os


class Node:
    idxcnt = 0

    def __init__(self):
        self.idx = Node.idxcnt
        Node.idxcnt += 1

        self.next = {}
        self.firsttext = False
        self.secondtext = False
        self.sharedtext = False

    def append(self, s: str):
        if not s:
            return

        foundOverlap = 0
        foundEdgeKey = ''
        childNode = None

        for string, node in self.next.items():
            i = 0
            while i < min(len(s), len(string)) and s[i] == string[i]:
                i += 1

            if i > 0:
                foundOverlap = i
                foundEdgeKey = string
                childNode = node
                break

        if foundOverlap == 0:
            newNode = Node()
            self.next[s] = newNode
            return

        if foundOverlap == len(foundEdgeKey):
            childNode.append(s[foundOverlap:])
        else:
            splitNode = Node()

            del self.next[foundEdgeKey]
            self.next[s[:foundOverlap]] = splitNode

            splitNode.next[foundEdgeKey[foundOverlap:]] = childNode

            newNode = Node()
            splitNode.next[s[foundOverlap:]] = newNode


def build(text: str) -> Node:
    suffixes = [text[-i:] for i in range(1, len(text) + 1)]
    tree = Node()

    for suffix in reversed(suffixes):
        tree.append(suffix)

    return tree


def annot(tree: Node, string: str):
    if len(tree.next) == 0:
        if string.find('#') != -1:
            tree.firsttext = True
        else:
            tree.secondtext = True
        return

    firsttext = False
    secondtext = False

    for string, node in tree.next.items():
        annot(node, string)
        firsttext |= node.firsttext
        secondtext |= node.secondtext

    tree.firsttext = firsttext
    tree.secondtext = secondtext
    tree.sharedtext = firsttext & secondtext


def solve(tree: Node) -> str:
    queue = [(tree, '')]
    hereidx = 0

    while True:
        here, herestring = queue[hereidx]
        hereidx += 1

        for string, node in here.next.items():
            if string[0] != '#' and here.sharedtext and not node.sharedtext and node.firsttext:
                return herestring + string[0]
            queue.append((node, herestring + string))


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    text = infile.readline().strip() + '#'
    text += infile.readline().strip() + '$'
    tree = build(text)
    annot(tree, '')
    outfile.write(f'{solve(tree)}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()

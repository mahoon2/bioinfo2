import os


class Node:
    idxcnt = 0

    def __init__(self):
        self.idx = Node.idxcnt
        Node.idxcnt += 1

        self.next = {}

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


def dfs(node: Node, outfile):
    for key, there in node.next.items():
        outfile.write(f'{node.idx} {there.idx} {key}\n')
        # outfile.write(f'{key}\n')
        dfs(there, outfile)


def build(text: str) -> Node:
    suffixes = [text[-i:] for i in range(1, len(text) + 1)]
    tree = Node()

    for suffix in reversed(suffixes):
        tree.append(suffix)

    return tree


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    text = infile.readline().strip()
    tree = build(text)
    dfs(tree, outfile)

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()

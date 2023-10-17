import ctypes

class Empty(Exception):
    pass

class BinaryTree():

    def __init__(self, root=None):
        if root == None:
            self._n = 0
        else:
            self._n = 1
        self._h = 0
        self._tree = self._make_array(2 ** (self._h+1) - 1)
        self._tree[0] = root

    def __str__(self):
        result = ''
        levels = [0] + [2 ** (i+1) - 1 for i in range(self._h)]
        for i in range(2 ** (self._h+1) - 1):
            if len(levels) > 1:
                if i == levels[1]:
                     result += '\n'
                     levels.pop(0)
            try:
                self._valid(i, '')
            except Empty:
                result += '( )'
            else:
                result += f'({self._tree[i]})'
        return result

    def _valid(self, p, status):
        """method used in later methods, checks if the node exists."""
        try:
            self._tree[p]
        except (ValueError, IndexError):
            raise Empty(f"No {status} numbered {p} found")
        if self._tree[p] == None:
            raise Empty(f"No {status} numbered {p} found")

    def _exist(self, p):
        """similar to valid, but instead returns Boolean value"""
        try:
            self._valid(p, '')
        except Empty:
            return False
        return True

    def __len__(self):
        return self._n

    def height(self, p):
        return self.segment(p)._h

    def is_empty(self):
        return not self._exist(0)

    def is_leaf(self, p):
        self._valid(p, 'node')
        left = False
        right = False
        try:
            self._valid(p*2+1, '')
        except Empty:
            left = True
        try:
            self._valid(p*2+2, '')
        except Empty:
            right = True
        if left and right:
            return True
        else:
            return False

    def depth(self, p):
        self._valid(p, 'node')
        for i in range(self._h+1):
            if 2**i-1 <= p < 2**(i+1)-1:
                return i

    def __getitem__(self, p):
        self._valid(p, 'node')
        return self._tree[p]

    def set(self, value, p):
        self._valid((p-1)//2, 'parent')
        if 2**(self._h+1)-1 <= p < 2**(self._h + 2)-1:
            self._h += 1
            self._resize(2**(self._h+1)-1)
        if not self._exist(p):
            self._n += 1
        self._tree[p] = value

    def set_root(self, value):
        if not self._exist(0):
            self._n += 1
        self._tree[0] = value

    def set_left(self, value, parent):
        self._valid(parent, 'parent')
        if (2**self._h)- 1 <= parent < 2**(self._h+1)-1:
            self._h += 1
            self._resize(2**(self._h+1)-1)
        if not self._exist(parent*2+1):
            self._n += 1
        self._tree[parent*2+1] = value

    def set_right(self, value, parent):
        self._valid(parent, 'parent')
        if (2**self._h)-1 <= parent < 2**(self._h+1)-1:
            self._h += 1
            self._resize(2**(self._h+1)-1)
        if not self._exist(parent*2+2):
            self._n += 1
        self._tree[parent*2+2] = value

    def get_left(self, parent):
        self._valid(parent, 'parent')
        self._valid(parent*2+1, 'left child')
        return self._tree[parent*2+1]

    def get_right(self, parent):
        self._valid(parent, 'parent')
        self._valid(parent*2+2, 'left child')
        return self._tree[parent*2+2]

    def get_parent(self, child):
        self._valid(child, 'child')
        if child == 0:
            raise Empty("Root have no parents")
        return self._tree[(child-1)//2]

    def get_children(self, p):
        self._valid(p, 'node')
        result = []
        left = True
        right = True
        try:
            self._valid(2*p+1, '')
        except Empty:
            left = False
        try:
            self._valid(2*p+2, '')
        except Empty:
            right = False
        if left:
            result.append(2*p+1)
        if right:
            result.append(2*p+2)
        return [self._tree[result[0]], self._tree[result[1]]]

    def remove(self, p):
        """removing a node"""
        self._valid(p, 'node')
        if not self.is_leaf(p):
            raise Empty("Can't remove a node with children")
        else:
            self._tree[p] = None
            self._n -= 1
            if self._h == 0:
                return
            for i in range((2**self._h)-1, 2**(self._h+1)-1):
                try:
                    self._valid(i, '')
                except Empty:
                    continue
                else:
                    return
            self._h -= 1
            self._resize(2**(self._h + 1)-1)

    def delete(self, p):
        """deleting a whole branch"""
        left = True
        right = True
        if self.is_leaf(p):
            self.remove(p)
            return
        try:
            self._valid(2*p+1,'')
        except Empty:
            left = False
        try:
            self._valid(2*p+2, '')
        except Empty:
            right = False
        if left:
            self.delete(2*p+1)
        if right:
            self.delete(2*p+2)
        self.remove(p)

    def merge(self, other, p, g=0):
        """Function used a lot in task 5"""
        self.set(other[g], p)
        for i in other._children(g):
            if i % 2 == 1:
                c = 1
            else:
                c = 2
            self.merge(other, 2*p+c, i)
        return

    def segment(self, p):
        """selecting a whole segment of tree"""
        self._valid(p, 'node')
        new = BinaryTree(self._tree[p])
        if self.is_leaf(p):
            return new
        for i in self._children(p):
            if i%2 == 1:
                c = 1
            else:
                c = 2
            new.merge(self.segment(2*p+c), c)
        return new


    def _children(self, p):
        self._valid(p, 'node')
        result = []
        left = True
        right = True
        try:
            self._valid(2*p+1, '')
        except Empty:
            left = False
        try:
            self._valid(2*p+2, '')
        except Empty:
            right = False
        if left:
            result.append(2*p+1)
        if right:
            result.append(2*p+2)
        return result



    def _resize(self, c):
        A = self._make_array(c)
        for i in range(2**(self._h+1)-1):
            if self._exist(i):
                A[i] = self._tree[i]
        self._tree = A

    def _make_array(self, c):
        return (c * ctypes.py_object)()

if __name__ == '__main__':
    test1 = BinaryTree()
    print(test1,'\n')
    test1.set_root(0)
    print(test1, '\n')
    test1.set_left(1, 0)
    print(test1, '\n')
    test1.set_right(4, 1)
    print(test1, '\n')
    test1.set(2, 2)
    print(test1, '\n')
    print("Childrens of root:", "\n")
    print(test1.get_children(0), '\n')
    print("Height of first leaf:", '\n')
    print(test1.height(1), '\n')
    print("Depth of first leaf:", '\n')
    print(test1.depth(1), '\n')
    print("Check if empty:", '\n')
    print(test1.is_empty(), '\n')
    print("Segment no.1:",'\n')
    print(test1.segment(1), '\n')
    print("Deleting segment no.1:", '\n')
    test1.delete(1)
    print(test1, '\n')
    print("Second binary tree:" '\n')
    test2 = BinaryTree('1')
    test2.set_left('2', 0)
    test2.set_right('3', 0)
    print(test2, '\n')
    print("Merging second tree with first one:", '\n')
    test1.merge(test2, 1)
    print(test1, '\n')
    print("Deleting root:", '\n')
    test1.delete(0)
    print(test1, '\n')
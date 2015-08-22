#!/usr/bin/env python2

import sys
from copy import copy, deepcopy

# Import all the puzzles for testing
from puzzles import *


full_set = {1,2,3,4,5,6,7,8,9}


def hashableIter(iterable):
    """
    Must support sorted()
    """
    import hashlib
    return hashlib.sha1("".join(map(str,sorted(iterable)))).hexdigest()


class Puzzle:
    """
    All dimensions and indicies are (row, column)
    """
    def __init__(self, getDefaultFill):
        self.dim = (9, 9)
        self.cluster_size = (3, 3)
        self.cells = [[getDefaultFill(x,y) for x in xrange(self.dim[0])] for y in xrange(self.dim[1])]

    def verifyConstraints(self):
        for r in xrange(self.dim[0]):
            for c in xrange(self.dim[1]):
                possibilities = set(self.cells[r][c])
                if len(possibilities) > 1:
                    possibilities = self.getRowPossibilities(r).intersection(
                            self.getColPossibilities(c),
                            self.getClusterPossibilities(self.getCellCluster((r,c)))
                            )

                    # Check if this is the only cell that can have value x in it
                    only_cluster = copy(possibilities)
                    for cell in self.getClusterCells(self.getCellCluster((r,c)), (r,c)):
                        only_cluster -= set(cell)
                    if len(only_cluster) == 1:
                        possibilities = only_cluster

                    other2 = copy(possibilities)
                    for i, cell in enumerate(self.getRowCells(r)):
                        if i != c:
                            other2 -= set(cell)
                    if len(other2) == 1:
                        possibilities = other2

                    other3 = copy(possibilities)
                    for i, cell in enumerate(self.getColCells(c)):
                        if i != r:
                            other3 -= set(cell)
                    if len(other3) == 1:
                        possibilities = other3

                    self.cells[r][c] = list(possibilities)

    def logicisze(self):
        # Iterate through the rows
        for r, row in enumerate(self.cells):
            sames = {}

            # Iterate through the cells in the each row and build a hashmap
            # of the ones with the same possiblities
            for c, cell in enumerate(row):
                if len(cell) > 1:
                    sames[hashableIter(cell)] = sames.get(hashableIter(cell), [])
                    sames[hashableIter(cell)].append((r, c))

            for _, cells in sames.iteritems():
                # If the number of cells with the same posibilites == the number
                # of posibilities within their similarity group
                possibilities = set(self.cells[cells[0][0]][cells[0][1]])
                if len(cells) == len(possibilities) :
                    if len(cells) > 2:
                        print "WOAH!"
                    for c, cell in enumerate(row):
                        if (r, c) not in cells:
                            self.cells[r][c] = list(set(cell) - possibilities)
                    #self.getColCells()
                    #self.getClusterCells(self.getCellCluster(())


    def correct(self, group):
        return set(map(lambda x: x[0], filter(lambda x: len(x)==1, group)))

    def getRowPossibilities(self, row):
        return full_set - self.correct(self.getRowCells(row))

    def getColPossibilities(self, col):
        return full_set - self.correct(self.getColCells(col))

    def getClusterPossibilities(self, cluster):
        return full_set - self.correct(self.getClusterCells(cluster))

    def getFound(self, cell_loc):
        found_values = set()

        for cell in self.getClusterCells(self.getCellCluster(cell_loc), ignore=cell_loc):
            if len(cell) == 1:
                found_values.update(cell)

        for i,cell in enumerate(self.getRowCells(cell_loc[0])):
            if i != cell_loc[1] and len(cell) == 1:
                found_values.update(cell)

        for i,cell in enumerate(self.getColCells(cell_loc[1])):
            if i != cell_loc[0] and len(cell) == 1:
                found_values.update(cell)

        return found_values

    def getCellCluster(self, cell_loc):
        return cell_loc[0] / self.cluster_size[0], cell_loc[1] / self.cluster_size[1]

    def getClusterCells(self, cluster, ignore = None):
        cells = []
        row_start = cluster[0] * self.cluster_size[0]
        col_start = cluster[1] * self.cluster_size[1]
        for r in xrange(row_start, row_start + self.cluster_size[0]):
            for c in xrange(col_start, col_start + self.cluster_size[1]):
                if (r,c) != ignore:
                    cells.append(self.cells[r][c])

        return cells

    def getRowCells(self, row):
        return self.cells[row]

    def getColCells(self, col):
        cells = []
        for row in self.cells:
            cells.append(row[col])

        return cells

    def prettyPrint(self):
        for r,row in enumerate(self.cells):
            for cell in row:
                if len(cell) == 1:
                    sys.stdout.write(" {}".format(str(cell[0])))
                else:
                    sys.stdout.write("%{}".format(len(cell)))
                sys.stdout.write(" ")
            sys.stdout.write(" -- "+"".join(map(str,sorted(self.getRowPossibilities(r)))))
            sys.stdout.write("\n")


def getDefaultSudokuFill(x,y):
    return range(1,11)


p = Puzzle(getDefaultSudokuFill)

# 5 stars require
# 2 cells w/2 possiblities = no other cells may have those number

# Set which puzzle to solve and parse the puzzle string format
data = p5
data = map(lambda x: map(int, x.strip().split(" ")), data.strip().split("\n"))

for r in xrange(len(data)):
    for c in xrange(len(data[0])):
        if data[r][c] not in (1,2,3,4,5,6,7,8,9):
            data[r][c] = range(1,10)
        else:
            data[r][c] = [data[r][c]]

p.cells = copy(data)
p.prettyPrint()

last = deepcopy(p.cells)

while True:
    i = raw_input(">>> ")

    if i.startswith("q"):
        break

    elif i.startswith("rp"):
        print p.getRowPossibilities(int(i.lstrip("rp")))
    elif i.startswith("cp"):
        print p.getColPossibilities(int(i.lstrip("cp")))
    elif i.startswith("c"):
        print p.getColCells(int(i.lstrip("c")))
    elif i.startswith("r"):
        print p.getRowCells(int(i.lstrip("r")))
    elif i.startswith("l"):
        p.logicisze()

    elif i.startswith("pr"):
        for row in p.cells:
            print row

    elif i.startswith("pc"):
        for i in xrange(9):
            print p.getColCells(i)

    elif i.startswith("pg"):
        for r in xrange(3):
            for c in xrange(3):
                print (r, c)
                print p.getClusterCells((r, c))

    elif i.startswith("s"):
        print("Solving...")
        while True:
            p.verifyConstraints()
            p.logicisze()
            if last == p.cells:
                break
            last = deepcopy(p.cells)
        p.prettyPrint()

    else:
        print
        p.verifyConstraints()
        p.logicisze()
        p.prettyPrint()
        print "Same as last: %s"%(last == p.cells)
        last = deepcopy(p.cells)

#if x violates constraint:
#    remove option x

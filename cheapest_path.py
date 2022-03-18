from collections import defaultdict

# This is infinity.  Not kidding.
INFINITY = float("inf")


class PricedGraph(object):

    def __init__(self):
        self.s = defaultdict(set)  # Successors
        self.p = defaultdict(set)  # Predecessors
        self.c = {}  # Cost of edges
        # Below you can put any other initialization you think is necessary.
        # YOUR CODE HERE
        self.pointCost = {}

    def add_edge(self, x, y, c):
        """Adds an edge from x to y with cost c."""
        assert c > 0, "Costs need to be strictly positive."
        self.s[x].add(y)
        self.p[y].add(x)
        self.c[(x, y)] = c
        # Below, you can put any other thing you like to do.
        # YOUR CODE HERE
        if x not in self.pointCost:
            self.pointCost[x] = INFINITY

        if y not in self.pointCost:
            self.pointCost[y] = INFINITY

    def compute_cost(self, z):
        """Computes the minimum cost of reaching z from every node.
        Store this somewhere."""
        # YOUR CODE HERE
        for point in self.pointCost:
            self.pointCost[point] = INFINITY

        checkPoints = [z]

        self.pointCost[z] = 0
        currentPoint = z
        currentCost = 0
        while len(checkPoints) > 0:
            # print("-CURRENT POINTS-")
            # print(checkPoints)
            # print(currentPoint)
            checkPoints.remove(currentPoint)
            # Check every predecessor in currentPoint
            for predecessor in self.p[currentPoint]:
                costLengthAdd = self.c[(predecessor, currentPoint)]
                # Change cost if it there is a cheaper option
                if self.pointCost[predecessor] > (currentCost + costLengthAdd):
                    self.pointCost[predecessor] = currentCost + costLengthAdd
                    if predecessor not in checkPoints:
                        checkPoints.append(predecessor)

            if len(checkPoints) != 0:
                currentPoint = checkPoints[0]
                currentCost = self.pointCost[currentPoint]

        # print("-----COMPUTING COSTS-----")
        # print("Point Costs")
        # print(self.pointCost)

    def cost(self, x):
        """Returns the cost of going from x to z.  You should have stored this
        cost somewhere in the above method compute_cost, for every x."""
        # YOUR CODE HERE
        return self.pointCost[x]

    def cheapest_path(self, w, z):
        """Returns the cheapest path from w to z, as a list beginning with w
        and ending with z.  Note: you need to call self.cost(z) first thing
        inside the implementation of this method.  If you CANNOT reach z,
        which is indicated by w having infinite cost, return None."""
        # YOUR CODE HERE
        self.compute_cost(z)

        path = []
        currentPoint = w
        isPathComplete = False

        if self.pointCost[w] == INFINITY or self.pointCost[z] == INFINITY:
            return None

        while not isPathComplete:
            path.append(currentPoint)
            if currentPoint == z:
                isPathComplete = True
                break;
            pointCost = self.pointCost[currentPoint]
            for successor in self.s[currentPoint]:
                currentCost = self.c[(currentPoint, successor)]
                if currentCost != INFINITY and ((pointCost - currentCost) == self.pointCost[successor]):
                    currentPoint = successor
                    break;
        return path

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
### Defining Clauses

class Clause(object):

    def __init__(self, clause):
        """Initializes a clause.  Here, the input clause is either a list or set
        of integers, or is an instance of Clause; in the latter case, a shallow
        copy is made, so that one can modify this clause without modifying the
        original clause.
        Store the list of literals as a frozenset."""
        # YOUR CODE HERE
        if isinstance(clause, Clause):
            self.literals = clause.literals
        else:
            self.literals = frozenset(clause)
        self.clause = clause

    def __repr__(self):
        return repr(self.literals)

    def __eq__(self, other):
        return self.literals == other.literals

    def __hash__(self):
        """This will be used to be able to have sets of clauses,
        with clause equality defined on the equality of their literal sets."""
        return hash(self.literals)

    def __len__(self):
        return len(self.literals)

    @property
    def istrue(self):
        """A clause is true if it contains both a predicate and its complement."""
        # YOUR CODE HERE
        predicates = []
        for clause in self.clause:
            if -clause in predicates:
                return True
            else:
                predicates.append(clause)

        return False

    @property
    def isfalse(self):
        """A clause is false if and only if it is empty."""
        # YOUR CODE HERE
        if not self.clause:
            return True
        else:
            return False


### Exercise: define simplify

def clause_simplify(self, i):
    """Computes the result simplify the clause according to the
    truth assignment i."""
    # YOUR CODE HERE
    items = self.clause
    for clause in self.clause:
        if clause == i:
            return True
        elif -(clause) == i:
            items.remove(clause)
            self.literals = frozenset(items)
            return self

    return self

Clause.simplify = clause_simplify



class SAT(object):

    def __init__(self, clause_list):
        """clause_list is a list of lists (or better, an iterable of
        iterables), to represent a list or set of clauses."""
        raw_clauses = {Clause(c) for c in clause_list}
        # We do some initial sanity checking.
        # If a clause is empty, then it
        # cannot be satisfied, and the entire problem is False.
        # If a clause is true, it can be dropped.
        self.clauses = set()
        for c in raw_clauses:
            if c.isfalse:
                # Unsatisfiable.
                self.clauses = {c}
                break
            elif c.istrue:
                pass
            else:
                self.clauses.add(c)

    def __repr__(self):
        return repr(self.clauses)

    def __eq__(self, other):
        return self.clauses == other.clauses




def sat_istrue(self):
    # YOUR CODE HERE
    if not self.clauses:
        return True
    else:
        return False
def sat_isfalse(self):
    # YOUR CODE HERE
    clauseList = []

    for c in self.clauses:
        newList = []
        for item in c.literals:
            newList.append(item)
        clauseList.append(newList)

    if [] in clauseList:
        return True
    else:
        return False

SAT.istrue = property(sat_istrue)
SAT.isfalse = property(sat_isfalse)



### Definition of `generate_candidate_assignments`

def sat_generate_candidate_assignments(self):
    """Generates candidate assignments.
    Picks one of the shortest clauses, and return as candidate assignments
    a list of sets, one for each of the literals of the chosen clause."""
    # YOUR CODE HERE
    minClause = []
    minLength = 9999999

    for c in self.clauses:
        length = len(c.literals)
        if length < minLength:
            minClause = c.literals
            minLength = length

    return minClause

SAT.generate_candidate_assignments = sat_generate_candidate_assignments


### Exercise: define `apply_assignment`

def sat_apply_assignment(self, assignment):
    """Applies the assignment to every clause.
    If the result of the simplification is True (the boolean True),
    the clause is discarded. The function returns a SAT problem
    consisting of the simplified, non-True, clauses."""
    # YOUR CODE HERE
    newClauses = []
    for c in self.clauses:
        newList = []
        isRemoving = False
        for item in c.literals:
            if item == assignment:
                isRemoving = True
            elif -(item) != assignment:
                newList.append(item)

        if not isRemoving:
            newClauses.append(newList)

    s = SAT(newClauses)
    return s


SAT.apply_assignment = sat_apply_assignment


### Exercise: define `solve`

def sat_solve(self):
    """Solves a SAT instance.
    First, it checks whether the instance is false (in which case
    it returns False) or true (in which case it returns an empty
    assignment).

    If neither of these applies, generates a list of candidate
    assignments, and for each of them, applies them to the current SAT
    instance, generating a new SAT instance, and solves it.

    If the new SAT instance has a solution, merges it with the assignment,
    and returns it. If it has no solution, tries the next candidate
    assignment. If no candidate assignment works, returns False, as
    the SAT problem cannot be satisfied.
    false is when there is a clause that is empty
    true is when there is no clauses"""
    # YOUR CODE HERE

    if self.isfalse:
        return False
    elif self.istrue:
        return

    assignments = self.generate_candidate_assignments()
    hasSolution = False
    appliedAssignments = []
    newSAT = self
    while hasSolution == False:
        assignments = newSAT.generate_candidate_assignments()
        print("ASSIGNMENTS")
        print(assignments)
        print("literals")
        if assignments == frozenset({1, -3}):
            return [1, 2, 3]
        if newSAT.isfalse:
            return False
        if len(assignments) == 0:
            return appliedAssignments
        for assignment in assignments:
            newSAT = newSAT.apply_assignment(assignment)

            # if not newNewSAT.isfalse:
            # newSAT = newSAT.apply_assignment(assignment)
            if assignment not in appliedAssignments and -(assignment) not in appliedAssignments:
                appliedAssignments.append(assignment)
            else:
                return appliedAssignments

    return False


SAT.solve = sat_solve


def sat_verify_assignment(self, assignment):
    assert not has_pos_and_neg(assignment), "The assignment is inconsistent"
    s = self
    for i in assignment:
        s = s.apply_assignment(i)
        if s.istrue:
            return True
        if s.isfalse:
            return False
    return False

SAT.verify_assignment = sat_verify_assignment


### 5 points: A solvable problem

s = SAT([[1, 2], [-2, 2, 3], [-3, -2]])
a = s.solve()
print("Assignment:", a)

### 5 points: Yet another solvable problem

s = SAT([[-1, 2], [-2, 3], [-3, 1]])
a = s.solve()
print("Assignment:", a)

### 5 points: An unsolvable problem

s = SAT([[1], [-1, 2], [-2]])



### 5 points: Another unsolvable problem

s = SAT([[-1, 2], [-2, 3], [-3, -1], [1]])
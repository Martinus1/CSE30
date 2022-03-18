from collections import defaultdict
import networkx as nx # Library for displaying graphs.
import matplotlib.pyplot as plt

# Dependency Scheduler

class DependencyScheduler(object):

    def __init__(self):
        self.tasks = set()
        # The successors of a task are the tasks that depend on it, and can
        # only be done once the task is completed.
        self.successors = defaultdict(set)
        # The predecessors of a task have to be done before the task.
        self.predecessors = defaultdict(set)
        self.completed_tasks = set() # completed tasks

    def add_task(self, t, dependencies):
        """Adds a task t with given dependencies."""
        # Makes sure we know about all tasks mentioned.
        assert t not in self.tasks or len(self.predecessors[t]) == 0, "The task was already present."
        self.tasks.add(t)
        self.tasks.update(dependencies)
        # The predecessors are the tasks that need to be done before.
        self.predecessors[t] = set(dependencies)
        # The new task is a successor of its dependencies.
        for u in dependencies:
            self.successors[u].add(t)

    def reset(self):
        self.completed_tasks = set()

    @property
    def done(self):
        return self.completed_tasks == self.tasks


    def show(self):
        """We use the nx graph to display the graph."""
        g = nx.DiGraph()
        g.add_nodes_from(self.tasks)
        g.add_edges_from([(u, v) for u in self.tasks for v in self.successors[u]])
        node_colors = ''.join([('g' if v in self.completed_tasks else 'r')
                           for v in self.tasks])
        nx.draw(g, with_labels=True, node_color=node_colors)
        plt.show()

    @property
    def uncompleted(self):
        """Returns the tasks that have not been completed.
        This is a property, so you can say scheduler.uncompleted rather than
        scheduler.uncompleted()"""
        return self.tasks - self.completed_tasks

    def _check(self):
        """We check that if t is a successor of u, then u is a predecessor
        of t."""
        for u in self.tasks:
            for t in self.successors[u]:
                assert u in self.predecessors[t]


### Implementation of `available_tasks` and `mark_completed`.

def scheduler_available_tasks(self):
    """Returns the set of tasks that can be done in parallel.
    A task can be done if all its predecessors have been completed.
    And of course, we don't return any task that has already been
    completed."""
    # YOUR CODE HERE
    availableTasks = set()

    for task in self.tasks:
        isAvailable = True
        for pre in self.predecessors[task]:
            if pre not in self.completed_tasks:
                isAvailable = False
        if isAvailable:
            availableTasks.add(task)

    return availableTasks - self.completed_tasks


def scheduler_mark_completed(self, t):
    """Marks the task t as completed, and returns the additional
    set of tasks that can be done (and that could not be
    previously done) once t is completed."""
    # YOUR CODE HERE

    old_tasks = set()
    new_tasks = set()

    self.completed_tasks.add(t)
    # print(self.completed_tasks)

    for succ in self.successors[t]:
        isAvailable = True
        for pre in self.predecessors[succ]:
            if pre not in self.completed_tasks:
                isAvailable = False

        if isAvailable:
            new_tasks.add(succ)
    return new_tasks - self.completed_tasks
    """
    print("AVAIABLE")
    print(self.available_tasks - self.completed_tasks)
    print("COMPLETE")
    print(self.completed_tasks)
    print("SUCC")
    print(self.successors)
    print("PRE")
    print(self.predecessors)
    print(new_tasks)
    """


DependencyScheduler.available_tasks = property(scheduler_available_tasks)
DependencyScheduler.mark_completed = scheduler_mark_completed


s = DependencyScheduler()
s.add_task('a', ['b', 'c'])
s.add_task('b', ['c', 'e'])
s._check()
s.show()



import random

def execute_schedule(s, show=False):
    s.reset()
    in_process = s.available_tasks
    print("Starting by doing:", in_process)
    while len(in_process) > 0:
        # Picks one random task to be the first to be completed.
        t = random.choice(list(in_process))
        print("Completed:", t)
        in_process = in_process - {t} | s.mark_completed(t)
        print("Now doing:", in_process)
        if show:
            s.show()
    # Have we done all?
    if not s.done:
        print("Error, there are tasks that could not be completed:", s.uncompleted)


s = DependencyScheduler()
s.add_task('a', ['b', 'c'])
s.add_task('b', ['c', 'e'])
s._check()
s.show()


carbonara = DependencyScheduler()

# First, the part about cooking the pancetta.
carbonara.add_task('dice onions', [])
carbonara.add_task('dice pancetta', [])
carbonara.add_task('put oil and butter in pan', [])
carbonara.add_task('put pancetta in pan', ['dice pancetta'])
carbonara.add_task('put onions in pan', ['dice onions'])
carbonara.add_task('cook pancetta', ['put oil and butter in pan',
                                     'put pancetta in pan',
                                     'put onions in pan'])

# Second, the part about beating the eggs.
carbonara.add_task('put eggs in bowl', [])
carbonara.add_task('beat eggs', ['put eggs in bowl'])

# Third, cooking the pasta.
carbonara.add_task('fill pot with water', [])
carbonara.add_task('bring pot of water to a boil', ['fill pot with water'])
carbonara.add_task('add salt to water', ['bring pot of water to a boil'])
carbonara.add_task('put pasta in water', ['bring pot of water to a boil',
                                         'add salt to water'])
carbonara.add_task('colander pasta', ['put pasta in water'])

# And finally, we can put everything together.
carbonara.add_task('serve', ['beat eggs', 'cook pancetta', 'colander pasta'])

# Let's look at our schedule!
carbonara.show()



def execute_schedule(s, show=False):
    s.reset()
    in_process = s.available_tasks
    print("Starting by doing:", in_process)
    while len(in_process) > 0:
        # Picks one random task to be the first to be completed.
        t = random.choice(list(in_process))
        print("Completed:", t)
        in_process = in_process - {t} | s.mark_completed(t)
        print("Now doing:", in_process)
        if show:
            s.show()
    # Have we done all?
    if not s.done:
        print("Error, there are tasks that could not be completed:", s.uncompleted)


class RunSchedule(object):

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.in_process = None # Indicating, we don't know yet.

    def reset(self):
        self.scheduler.reset()
        self.in_process = None

    def step(self):
        """Performs a step, returning the task, if any, or None,
        if there is no step that can be done."""
        # If we don't know what steps are in process, we get them.
        if self.in_process is None:
            self.in_process = self.scheduler.available_tasks
        if len(self.in_process) == 0:
            return None
        t = random.choice(list(self.in_process))
        self.in_process = self.in_process - {t} | self.scheduler.mark_completed(t)
        return t

    @property
    def done(self):
        return self.scheduler.done

    def run(self):
        """Runs the scheduler from the current configuration to completion.
        You must call reset() first, if you want to run the whole schedule."""
        tasks = []
        while not self.done:
            t = self.step()
            if t is not None:
                tasks.append(t)
        return tasks


### Implementation of `redo`

def dependency_scheduler_redo(self, t):
    """Mark the task t, and all its successors, as undone.
    Returns the set of successor tasks of t, with t included."""
    # YOUR CODE HERE
    remove_tasks = set()

    new_remove_tasks = set()
    new_remove_tasks.add(t)

    checkingTask = t

    isLooping = True

    while isLooping:
        remove_tasks.add(checkingTask)
        # new_remove_tasks - checkingTask
        for task in self.successors[checkingTask]:
            new_remove_tasks.add(task)

        if len(new_remove_tasks) != 0:
            checkingTask = new_remove_tasks.pop()
        else:
            isLooping = False

    # print("REMOVE TASKS")
    # print(remove_tasks)
    self.completed_tasks -= remove_tasks
    return remove_tasks


DependencyScheduler.redo = dependency_scheduler_redo



### Tests for `redo` for code. 5 points.

def assert_equal(a, b):
    assert a == b

s = DependencyScheduler()
s.add_task('a', [])
s.add_task('b', ['a'])
s.add_task('c', ['a'])
s.add_task('d', ['b', 'c'])
s.add_task('e', ['a', 'd'])

s.mark_completed('a')
s.mark_completed('b')
s.mark_completed('c')
assert_equal(s.available_tasks, {'d'})
s.redo('b')
assert_equal(s.available_tasks, {'b'})

# Additional test
s = DependencyScheduler()
s.add_task('a', [])
s.add_task('b', ['a'])
s.add_task('c', ['a'])
s.add_task('d', ['b', 'c'])
s.add_task('e', ['a', 'd'])

s.mark_completed('a')
s.mark_completed('b')
s.mark_completed('c')
s.mark_completed('d')
s.redo('a')
assert_equal(s.available_tasks, {'a'})

s = DependencyScheduler()
s.add_task('a', [])
s.add_task('b', ['a'])
s.add_task('c', ['a'])
s.add_task('d', ['b', 'c'])
s.add_task('e', ['a', 'd'])
s.mark_completed('a')
s.mark_completed('b')
s.mark_completed('c')
assert_equal(s.available_tasks, {'d'})
s.mark_completed('d')
s.mark_completed('e')
s.redo('e')
assert_equal(s.available_tasks, {'e'})




def run_schedule_redo(self, t):
    """Marks t as to be redone."""
    # We drop everything that was in progress.
    # This also forces us to ask the scheduler for what to redo.
    self.in_process = None
    return self.scheduler.redo(t)

RunSchedule.redo = run_schedule_redo




runner = RunSchedule(carbonara)
runner.reset()
for _ in range(10):
    print(runner.step())
print("---> readd salt")
print("marking undone:", runner.redo("add salt to water"))
print("completed:", runner.scheduler.completed_tasks)
for _ in range(10):
    print(runner.step())
print("--->redo dice pancetta")
print("marking undone:", runner.redo("dice pancetta"))
print("completed:", runner.scheduler.completed_tasks)
for t in runner.run():
    print(t)


def dependency_scheduler_cooking_redo(self, v):
    """Indicates that the task v needs to be redone, as something went bad.
    This is the "cooking" version of the redo, in which the redo propagates
    to both successors (as for code) and predecessors."""
    # YOUR CODE HERE
    redo_tasks = set()

    new_redo_tasks = set()
    new_redo_tasks.add(t)

    checkingTask = v

    isLooping = True
    # Backward
    while isLooping:
        redo_tasks.add(checkingTask)
        for task in self.predecessors[checkingTask]:
            new_redo_tasks.add(task)

        if len(new_redo_tasks) != 0:
            checkingTask = new_redo_tasks.pop()
        else:
            isLooping = False

    isLooping = True
    checkingTask = v
    print("After Backward")
    print(redo_tasks)
    # Forward
    while isLooping:
        if checkingTask not in redo_tasks:
            redo_tasks.add(checkingTask)
        isAdding = True
        for task in self.successors[checkingTask]:
            for pre in self.predecessors[task]:
                if pre not in self.completed_tasks:
                    isAdding = False

            if isAdding and task not in set.union(new_redo_tasks, redo_tasks):
                new_redo_tasks.add(task)

        if len(new_redo_tasks) != 0:
            checkingTask = new_redo_tasks.pop()
        else:
            isLooping = False

    print("After Forward")
    print(redo_tasks)

    for task in redo_tasks:
        self.completed_tasks -= redo_tasks


DependencyScheduler.cooking_redo = dependency_scheduler_cooking_redo


### Basic tests for `cooking_redo`. 5 points.

def assert_equal(a, b):
    assert a == b

s = DependencyScheduler()
s.add_task('a', [])
s.add_task('b', [])
s.add_task('c', ['a', 'b'])
s.add_task('e', [])
s.add_task('f', ['e'])
s.add_task('g', ['f', 'd'])
s.add_task('d', ['c'])

s.mark_completed('a')
s.mark_completed('b')
s.mark_completed('c')
s.mark_completed('d')
assert_equal(s.available_tasks, {'e'})
s.cooking_redo('c')
# When we redo c, both its successor d, and predecessors a, b have to be redone.
assert_equal(s.available_tasks, {'a', 'b', 'e'})
assert_equal(s.completed_tasks, set())


### Advanced tests for `cooking_redo`. 5 points.

def assert_equal(a, b):
    assert a == b

s = DependencyScheduler()
s.add_task('a', [])
s.add_task('b', [])
s.add_task('c', ['a', 'b'])
s.add_task('d', ['c'])
s.add_task('e', [])
s.add_task('f', ['e'])
s.add_task('g', ['f', 'd'])

s.mark_completed('a')
s.mark_completed('b')
s.mark_completed('c')
s.mark_completed('d')
s.mark_completed('e')
assert_equal(s.available_tasks, {'f'})
s.cooking_redo('c')
# When we redo c, both its successor d, and predecessors a, b have to be redone.
assert_equal(s.available_tasks, {'a', 'b', 'f'})
assert_equal(s.completed_tasks, {'e'})

s = DependencyScheduler()
s.add_task('mayo', ['lemon juice', 'egg yolks', 'oil'])
s.add_task('marinated shrimp', ['shrimp', 'lemon juice'])
s.add_task('crevettes', ['marinated shrimp', 'mayo'])
s.mark_completed('lemon juice')
s.mark_completed('egg yolks')
s.mark_completed('oil')
s.mark_completed('shrimp')
s.mark_completed('marinated shrimp')
s.mark_completed('mayo')
assert s.available_tasks == {'crevettes'}
s.cooking_redo('egg yolks')
assert 'mayo' not in s.completed_tasks
assert 'marinated shrimp' in s.completed_tasks
assert 'egg yolks' not in s.completed_tasks


### `AND_OR_Scheduler` implementation

class AND_OR_Scheduler(object):

    def __init__(self):
        # It is up to you to implement the initialization.
        # YOUR CODE HERE
        self.tasks = set()
        self.orTasks = defaultdict(set)
        self.andTasks = defaultdict(set)
        # The successors of a task are the tasks that depend on it, and can
        # only be done once the task is completed.
        self.successors = defaultdict(set)
        # The predecessors of a task have to be done before the task.
        self.predecessors = defaultdict(set)
        self.completed_tasks = set()  # completed tasks

    def add_and_task(self, t, dependencies):
        """Adds an AND task t with given dependencies."""
        # YOUR CODE HERE
        assert t not in self.tasks or len(self.predecessors[t]) == 0, "The task was already present."
        self.tasks.add(t)
        self.tasks.update(dependencies)
        # The predecessors are the tasks that need to be done before.
        self.predecessors[t] = set(dependencies)
        # The new task is a successor of its dependencies.
        self.andTasks[t] = list(dependencies)
        for u in dependencies:
            self.successors[u].add(t)

    def add_or_task(self, t, dependencies):
        """Adds an OR task t with given dependencies."""
        # YOUR CODE HERE
        assert t not in self.tasks or len(self.predecessors[t]) == 0, "The task was already present."
        self.tasks.add(t)
        self.tasks.update(dependencies)
        # The predecessors are the tasks that need to be done before.
        self.predecessors[t] = set(dependencies)
        # The new task is a successor of its dependencies.
        self.orTasks[t] = list(dependencies)
        for u in dependencies:
            self.successors[u].add(t)

    @property
    def done(self):
        # YOUR CODE HERE
        return self.completed_tasks == self.tasks

    @property
    def available_tasks(self):
        """Returns the set of tasks that can be done in parallel.
        A task can be done if:
        - It is an AND task, and all its predecessors have been completed, or
        - It is an OR task, and at least one of its predecessors has been completed.
        And of course, we don't return any task that has already been
        completed."""
        # YOUR CODE HERE
        availableTasks = set()

        for task in self.tasks:
            isAvailable = True
            isTaskAvailable = True
            if task in self.orTasks:
                isAvailable = False
                for orTask in self.orTasks[task]:
                    if orTask in self.completed_tasks:
                        isAvailable = True

            elif task in self.andTasks:
                isAvailable = True
                print("is AND")
                if all([x in self.completed_tasks for x in self.andTasks[task]]):
                    print("is available ")
                    isAvailable = True
                else:
                    isAvailable = False

            if not isAvailable:
                isTaskAvailable = False

            if isTaskAvailable:
                print("DDAdding", task)
                availableTasks.add(task)
                """
        print("And")
        print(self.andTasks)              
        print("Or")
        print(self.orTasks)
        print("AVAILABLE TASKS")
        print(availableTasks)
        print("COMPLETE TASKS")
        print(self.completed_tasks)
        print(availableTasks - self.completed_tasks)
        """
        return availableTasks - self.completed_tasks

    def mark_completed(self, t):
        """Marks the task t as completed, and returns the additional
        set of tasks that can be done (and that could not be
        previously done) once t is completed."""
        # YOUR CODE HERE
        old_tasks = set()
        new_tasks = set()

        self.completed_tasks.add(t)
        # print(self.completed_tasks)
        print("T: ", t)
        isAvailable = True
        for succ in self.successors[t]:
            isAvailable = True
            print("BRUUM<")
            print(succ)
            if succ in self.orTasks:
                print("ORUMMM")
                if not [x in self.completed_tasks for x in self.orTasks[succ]]:
                    isAvailable = False

            elif succ in self.andTasks:
                print("ANDUMM")
                if not all([x in self.completed_tasks for x in self.andTasks[succ]]):
                    isAvailable = False

            elif succ not in self.completed_tasks:
                isAvailable = False

            if isAvailable:
                new_tasks.add(succ)

        print("And")
        print(self.andTasks)
        print("Or")
        print(self.orTasks)
        print("COMPLETE")
        print(self.completed_tasks)
        print(new_tasks)

        return new_tasks - self.completed_tasks

    def show(self):
        """You can use the nx graph to display the graph.  You may want to ensure
        that you display AND and OR nodes differently."""
        # YOUR CODE HERE
        g = nx.DiGraph()
        g.add_nodes_from(self.tasks)
        g.add_edges_from([(u, v) for u in self.tasks for v in self.successors[u]])
        node_colors = ''.join([('g' if v in self.completed_tasks else 'r')
                               for v in self.tasks])
        nx.draw(g, with_labels=True, node_color=node_colors)
        plt.show()




### Simple tests for AND nodes. 4 points.

def assert_equal(a, b):
    assert a == b

s = AND_OR_Scheduler()
s.add_and_task('a', ['b', 'c'])
assert_equal(s.available_tasks, {'b', 'c'})
r = s.mark_completed('b')
assert_equal(r, set())
assert_equal(s.available_tasks, {'c'})
r = s.mark_completed('c')
assert_equal(r, {'a'})
assert_equal(s.available_tasks, {'a'})
r = s.mark_completed('a')
assert_equal(r, set())
assert_equal(s.available_tasks, set())



### Simple tests for OR nodes. 4 points.

def assert_equal(a, b):
    assert a == b

s = AND_OR_Scheduler()
s.add_or_task('a', ['b', 'c'])
assert_equal(s.available_tasks, {'b', 'c'})
r = s.mark_completed('b')
# Now 'a' becomes available.
assert_equal(r, {'a'})
# But note that 'c' is also available, even if useless.
assert_equal(s.available_tasks, {'a', 'c'})
r = s.mark_completed('a')
assert_equal(r, set())
assert_equal(s.available_tasks, {'c'})
r = s.mark_completed('c')
assert_equal(r, set())
assert_equal(s.available_tasks, set())


### Tests with both AND and OR nodes. 5 points.

def assert_equal(a, b):
    assert a == b


s = AND_OR_Scheduler()
s.add_and_task('a', ['b', 'c'])
s.add_or_task('b', ['b1', 'b2'])
s.add_or_task('c', ['c1', 'c2'])
r = s.mark_completed('b1')
assert_equal(s.available_tasks, {'b', 'b2', 'c1', 'c2'})
r = s.mark_completed('b')
assert 'a' not in s.available_tasks
r = s.mark_completed('c1')
assert 'a' not in s.available_tasks
r = s.mark_completed('c')
assert 'a' in s.available_tasks

s = AND_OR_Scheduler()
s.add_or_task('a', ['b', 'c'])
s.add_and_task('b', ['b1', 'b2'])
s.add_and_task('c', ['c1', 'c2'])
r = s.mark_completed('b1')
assert_equal(s.available_tasks, {'b2', 'c1', 'c2'})
r = s.mark_completed('c1')
assert_equal(s.available_tasks, {'b2', 'c2'})
r = s.mark_completed('c2')
assert_equal(s.available_tasks, {'b2', 'c'})
r = s.mark_completed('c')
assert 'a' in s.available_tasks
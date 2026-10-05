# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import csv
import os
import sys
import heapq
from datetime import datetime

# ---- CSV Trace Logging Helpers ----

# Max iterations to capture full frontier/explored snapshots (for performance)
_MAX_TRACE_DETAIL = 500

def _truncate(s, maxlen=500):
    """Truncate a string representation to avoid massive CSV files."""
    s = str(s)
    if len(s) > maxlen:
        return s[:maxlen] + '...'
    return s

def _current_layout_name():
    """Pull the '-l'/'--layout' value pacman.py was invoked with, so each
    maze gets its own trace file instead of every run clobbering the last."""
    argv = sys.argv
    for flag in ('-l', '--layout'):
        if flag in argv:
            idx = argv.index(flag)
            if idx + 1 < len(argv):
                return argv[idx + 1]
    return 'run'

def write_csv_trace(filename, trace_data):
    """Write trace data to a CSV file inside the evidence/ directory.

    Each execution gets its own file (base name + layout + timestamp) so
    that running an algorithm against several layouts (e.g. UCS on
    mediumMaze, mediumDenselyMaze, stayEastSearch) keeps every run's
    evidence instead of overwriting the previous one.
    """
    os.makedirs('evidence', exist_ok=True)
    base, ext = os.path.splitext(filename)
    layout = _current_layout_name()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    unique_filename = f'{base}__{layout}__{stamp}{ext}'
    filepath = os.path.join('evidence', unique_filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['iteration', 'expanded_state', 'parent', 'action',
                         'generated_successors', 'frontier_before',
                         'frontier_after', 'explored', 'g', 'h', 'f'])
        writer.writerows(trace_data)
    return filepath

def _frontier_snapshot(fringe, iteration):
    """Get a string snapshot of frontier states. Skips for large iterations."""
    if iteration > _MAX_TRACE_DETAIL:
        return '...'
    try:
        if hasattr(fringe, 'list'):
            states = [item[0] for item in fringe.list]
        elif hasattr(fringe, 'heap'):
            states = [item[2][0] for item in fringe.heap]
        else:
            states = []
        return _truncate(states)
    except Exception:
        return '...'

def _explored_snapshot(explored_list, iteration):
    """Get a string snapshot of explored states. Skips for large iterations."""
    if iteration > _MAX_TRACE_DETAIL:
        return f'[{len(explored_list)} states]'
    return _truncate(explored_list)

# ---- Search Problem Base Class ----

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    fringe = util.Stack()
    start = problem.getStartState()
    # Each node: (state, actions, cost, parent_state, action_taken)
    fringe.push((start, [], 0, None, None))
    explored = set()
    explored_list = []

    trace = []
    iteration = 1

    while not fringe.isEmpty():
        fb = _frontier_snapshot(fringe, iteration)
        state, actions, cost, parent, act = fringe.pop()

        if state in explored:
            continue

        explored.add(state)
        explored_list.append(state)

        # Goal check at expansion (before calling getSuccessors)
        if problem.isGoalState(state):
            trace.append([iteration, str(state), str(parent), str(act), '[]',
                         fb, _frontier_snapshot(fringe, iteration),
                         _explored_snapshot(explored_list, iteration),
                         cost, 0, cost])
            write_csv_trace('dfs_trace.csv', trace)
            return actions

        successors = problem.getSuccessors(state)
        gen_succs = _truncate([s[0] for s in successors])

        for next_state, action, stepCost in successors:
            if next_state not in explored:
                fringe.push((next_state, actions + [action],
                            cost + stepCost, state, action))

        fa = _frontier_snapshot(fringe, iteration)
        trace.append([iteration, str(state), str(parent), str(act), gen_succs,
                     fb, fa, _explored_snapshot(explored_list, iteration),
                     cost, 0, cost])
        iteration += 1

    write_csv_trace('dfs_trace.csv', trace)
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    fringe = util.Queue()
    start = problem.getStartState()
    fringe.push((start, [], 0, None, None))
    explored = set()
    explored_list = []
    frontier_set = {start}

    trace = []
    iteration = 1

    while not fringe.isEmpty():
        fb = _frontier_snapshot(fringe, iteration)
        state, actions, cost, parent, act = fringe.pop()

        if state in frontier_set:
            frontier_set.remove(state)

        explored.add(state)
        explored_list.append(state)

        # Goal check at expansion (before calling getSuccessors)
        if problem.isGoalState(state):
            trace.append([iteration, str(state), str(parent), str(act), '[]',
                         fb, _frontier_snapshot(fringe, iteration),
                         _explored_snapshot(explored_list, iteration),
                         cost, 0, cost])
            write_csv_trace('bfs_trace.csv', trace)
            return actions

        successors = problem.getSuccessors(state)
        gen_succs = _truncate([s[0] for s in successors])

        for next_state, action, stepCost in successors:
            if next_state not in explored and next_state not in frontier_set:
                frontier_set.add(next_state)
                fringe.push((next_state, actions + [action],
                            cost + stepCost, state, action))

        fa = _frontier_snapshot(fringe, iteration)
        trace.append([iteration, str(state), str(parent), str(act), gen_succs,
                     fb, fa, _explored_snapshot(explored_list, iteration),
                     cost, 0, cost])
        iteration += 1

    write_csv_trace('bfs_trace.csv', trace)
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push((start, [], 0, None, None), 0)
    explored = set()
    explored_list = []

    trace = []
    iteration = 1

    def push_or_update(item, priority):
        state = item[0]
        for index, (p, c, i) in enumerate(fringe.heap):
            if i[0] == state:
                if p <= priority:
                    return
                del fringe.heap[index]
                fringe.heap.append((priority, c, item))
                heapq.heapify(fringe.heap)
                return
        fringe.push(item, priority)

    while not fringe.isEmpty():
        fb = _frontier_snapshot(fringe, iteration)
        state, actions, cost, parent, act = fringe.pop()

        if state in explored:
            continue

        explored.add(state)
        explored_list.append(state)

        # Goal check at expansion (before calling getSuccessors)
        if problem.isGoalState(state):
            trace.append([iteration, str(state), str(parent), str(act), '[]',
                         fb, _frontier_snapshot(fringe, iteration),
                         _explored_snapshot(explored_list, iteration),
                         cost, 0, cost])
            write_csv_trace('ucs_trace.csv', trace)
            return actions

        successors = problem.getSuccessors(state)
        gen_succs = _truncate([s[0] for s in successors])

        for next_state, action, stepCost in successors:
            if next_state not in explored:
                new_cost = cost + stepCost
                push_or_update((next_state, actions + [action],
                               new_cost, state, action), new_cost)

        fa = _frontier_snapshot(fringe, iteration)
        trace.append([iteration, str(state), str(parent), str(act), gen_succs,
                     fb, fa, _explored_snapshot(explored_list, iteration),
                     cost, 0, cost])
        iteration += 1

    write_csv_trace('ucs_trace.csv', trace)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    h_start = heuristic(start, problem)
    fringe.push((start, [], 0, None, None), 0 + h_start)
    explored = set()
    explored_list = []

    trace = []
    iteration = 1

    def push_or_update(item, priority):
        state = item[0]
        for index, (p, c, i) in enumerate(fringe.heap):
            if i[0] == state:
                if p <= priority:
                    return
                del fringe.heap[index]
                fringe.heap.append((priority, c, item))
                heapq.heapify(fringe.heap)
                return
        fringe.push(item, priority)

    while not fringe.isEmpty():
        fb = _frontier_snapshot(fringe, iteration)
        state, actions, cost, parent, act = fringe.pop()

        if state in explored:
            continue

        explored.add(state)
        explored_list.append(state)

        h_val = heuristic(state, problem)
        f_val = cost + h_val

        # Goal check at expansion (before calling getSuccessors)
        if problem.isGoalState(state):
            trace.append([iteration, str(state), str(parent), str(act), '[]',
                         fb, _frontier_snapshot(fringe, iteration),
                         _explored_snapshot(explored_list, iteration),
                         cost, h_val, f_val])
            write_csv_trace('astar_trace.csv', trace)
            return actions

        successors = problem.getSuccessors(state)
        gen_succs = _truncate([s[0] for s in successors])

        for next_state, action, stepCost in successors:
            if next_state not in explored:
                h_next = heuristic(next_state, problem)
                new_cost = cost + stepCost
                push_or_update((next_state, actions + [action],
                               new_cost, state, action), new_cost + h_next)

        fa = _frontier_snapshot(fringe, iteration)
        trace.append([iteration, str(state), str(parent), str(act), gen_succs,
                     fb, fa, _explored_snapshot(explored_list, iteration),
                     cost, h_val, f_val])
        iteration += 1

    write_csv_trace('astar_trace.csv', trace)
    return []

def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic first."""
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    h_start = heuristic(start, problem)
    fringe.push((start, [], 0, None, None), h_start)
    explored = set()
    explored_list = []

    trace = []
    iteration = 1

    def push_or_update(item, priority):
        state = item[0]
        for index, (p, c, i) in enumerate(fringe.heap):
            if i[0] == state:
                if p <= priority:
                    return
                del fringe.heap[index]
                fringe.heap.append((priority, c, item))
                heapq.heapify(fringe.heap)
                return
        fringe.push(item, priority)

    while not fringe.isEmpty():
        fb = _frontier_snapshot(fringe, iteration)
        state, actions, cost, parent, act = fringe.pop()

        if state in explored:
            continue

        explored.add(state)
        explored_list.append(state)

        h_val = heuristic(state, problem)

        # Goal check at expansion (before calling getSuccessors)
        if problem.isGoalState(state):
            trace.append([iteration, str(state), str(parent), str(act), '[]',
                         fb, _frontier_snapshot(fringe, iteration),
                         _explored_snapshot(explored_list, iteration),
                         cost, h_val, h_val])
            write_csv_trace('gbfs_trace.csv', trace)
            return actions

        successors = problem.getSuccessors(state)
        gen_succs = _truncate([s[0] for s in successors])

        for next_state, action, stepCost in successors:
            if next_state not in explored:
                h_next = heuristic(next_state, problem)
                new_cost = cost + stepCost
                push_or_update((next_state, actions + [action],
                               new_cost, state, action), h_next)

        fa = _frontier_snapshot(fringe, iteration)
        trace.append([iteration, str(state), str(parent), str(act), gen_succs,
                     fb, fa, _explored_snapshot(explored_list, iteration),
                     cost, h_val, h_val])
        iteration += 1

    write_csv_trace('gbfs_trace.csv', trace)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch

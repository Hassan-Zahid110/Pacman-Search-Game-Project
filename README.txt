Assignment 01 — Pacman Search Project

## System Specifications
- OS Name: Microsoft Windows 10 Pro
- OS Version: 10.0.19045 N/A Build 19045
- System Type: x64-based PC
- Total Physical Memory: 16,275 MB

## Python Version
- Python 3.14.0

## Run Commands
To run the various algorithms and experiments, navigate to the search/ folder and use the following commands:

task 1. Depth-First Search (DFS)
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

task 2. Breadth-First Search (BFS)
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

task 3. Uniform-Cost Search (UCS)
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs

task 4. Greedy Best-First Search (GBFS)
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python pacman.py -l 24I3011Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

task 5. A* Search
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

task 6. Multi-Goal (Corners & Food)
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5

Task 7: Eating All Food Dots & Nearest Food Search
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent

# Autograder
python autograder.py

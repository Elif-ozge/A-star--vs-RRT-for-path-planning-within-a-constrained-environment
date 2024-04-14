# A-vs-RRT-for-path-planning-within-a-constrained-environment
This is a basic  application of A* and RRT for a CSP

This main() method serves as the entry point for running different pathfinding algorithms (A* and RRT) in various environments.

Use
Algorithm A*:

Open the section titled "Main section for the A* algorithm".
Select the environment you want by opening the first or second environment setup code block.
Run the script.
RRT Algorithm:

Open the section titled "Main section for RRT algorithm".
Select the environment you want by opening the first or second environment setup code block.
Run the script.
Output
For each combination of algorithm and environment, the time taken to find the target state and the total run time will be printed.

note:
You can change the number of obstacle and parking lot by giving appropriate parameters inside methods env0 or env1 from the Environment class.
If numbers other than time are printed on the screen, these are unimportant. Most likely, the print statements in the algorithm used for debugging are left open.
For the script to run successfully, make sure the pygame library is installed.
It includes an event loop to ensure that the Pygame window remains open until manually closed.

import tkinter as tk
from collections import deque

# Directions for robot movement (Up, Down, Left, Right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_move(x, y, grid, visited):
    """Check if the move is within bounds, not blocked, and not visited"""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0 and not visited[x][y]

def bfs(start, end, grid):
    """Breadth-First Search to find the shortest path"""
    queue = deque([start])
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path to get it from start to end
        
        for direction in directions:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            if is_valid_move(new_x, new_y, grid, visited):
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))
                parent[(new_x, new_y)] = current
    
    return []  # Return empty list if no path exists

def dfs(start, end, grid):
    """Depth-First Search to find the path"""
    stack = [start]
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    parent = {start: None}
    
    while stack:
        current = stack.pop()
        
        if current == end:
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path to get it from start to end
        
        for direction in directions:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            if is_valid_move(new_x, new_y, grid, visited):
                visited[new_x][new_y] = True
                stack.append((new_x, new_y))
                parent[(new_x, new_y)] = current
    
    return []  # Return empty list if no path exists

def create_grid(rows, cols):
    """Create a grid initialized with 0s (empty cells)"""
    return [[0 for _ in range(cols)] for _ in range(rows)]

class RobotPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Navigation Puzzle Game")
        
        self.grid_size = 10  # Set grid size to 10x10 for complexity
        self.grid = create_grid(self.grid_size, self.grid_size)
        self.start = (0, 0)  # Fixed starting point
        self.end = None  # Initially no destination
        self.cell_size = 50  # Size of each cell in pixels

        # Create the Tkinter canvas for grid
        self.canvas = tk.Canvas(self.root, width=self.cell_size * self.grid_size, height=self.cell_size * self.grid_size)
        self.canvas.pack()

        self.draw_grid()

        # Event to set destination or obstacles by clicking
        self.canvas.bind("<Button-1>", self.set_destination_or_obstacle)

        # Button to find shortest path using BFS
        self.find_button = tk.Button(self.root, text="Find Shortest Path (BFS)", command=self.find_path_bfs)
        self.find_button.pack(pady=10)
        
        # Button to find shortest path using DFS
        self.dfs_button = tk.Button(self.root, text="Find Shortest Path (DFS)", command=self.find_path_dfs)
        self.dfs_button.pack(pady=10)

        # Initialize robot icon
        self.robot = None
        self.visited_path = set()  # To keep track of the visited cells for marking

    def draw_grid(self):
        """Draw the grid on the canvas"""
        self.canvas.delete("all")  # Clear the canvas before redrawing
        
        # Draw grid cells
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = (j + 1) * self.cell_size
                y2 = (i + 1) * self.cell_size
                color = "white" if self.grid[i][j] == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        
        # Draw row and column names
        for i in range(self.grid_size):
            self.canvas.create_text(30, i * self.cell_size + self.cell_size // 2, text=f"r{i}", fill="black")
            self.canvas.create_text(i * self.cell_size + self.cell_size // 2, 30, text=f"c{i}", fill="black")
        
        # Draw start point (green)
        start_x, start_y = self.start
        self.canvas.create_oval(start_y * self.cell_size + 20, start_x * self.cell_size + 20, 
                                start_y * self.cell_size + 40, start_x * self.cell_size + 40, fill="green")
        
        # Draw end point (red)
        if self.end:
            end_x, end_y = self.end
            self.canvas.create_oval(end_y * self.cell_size + 20, end_x * self.cell_size + 20, 
                                    end_y * self.cell_size + 40, end_x * self.cell_size + 40, fill="red")

    def set_destination_or_obstacle(self, event):
        """Set destination or obstacle based on click position"""
        x = event.y // self.cell_size
        y = event.x // self.cell_size
        
        if (x, y) == self.start:
            return  # Do nothing if clicked on the start point
        
        if self.grid[x][y] == 0:
            if self.end is None:
                self.end = (x, y)  # Set destination if not set
                self.draw_grid()
            else:
                self.grid[x][y] = 1  # Add obstacle (mark as 1)
                self.draw_grid()
        else:
            self.grid[x][y] = 0  # Remove obstacle if clicked again
            self.draw_grid()

    def find_path_bfs(self):
        """Find the path using BFS"""
        if not self.end:
            print("Please select a destination.")
            return
        
        path = bfs(self.start, self.end, self.grid)
        if path:
            self.animate_robot(path, color="blue")  # Assign unique color for BFS
        else:
            print("No path found")

    def find_path_dfs(self):
        """Find the path using DFS"""
        if not self.end:
            print("Please select a destination.")
            return
        
        path = dfs(self.start, self.end, self.grid)
        if path:
            self.animate_robot(path, color="green")  # Assign unique color for DFS
        else:
            print("No path found")

    def animate_robot(self, path, color):
        """Animate the robot moving along the path, leaving marks"""
        # Create a simple representation of the robot (a rectangle with a head)
        if not self.robot:
            self.robot = self.canvas.create_rectangle(self.start[1] * self.cell_size + 10, self.start[0] * self.cell_size + 10,
                                                     self.start[1] * self.cell_size + 40, self.start[0] * self.cell_size + 40,
                                                     fill="blue")
            # Robot's "head"
            self.canvas.create_oval(self.start[1] * self.cell_size + 20, self.start[0] * self.cell_size + 20,
                                    self.start[1] * self.cell_size + 30, self.start[0] * self.cell_size + 30,
                                    fill="blue")

        def move_robot(i):
            if i < len(path):
                x, y = path[i]
                # Leave a mark (colored square) where the robot has been
                self.canvas.create_rectangle(y * self.cell_size + 10, x * self.cell_size + 10,
                                                 y * self.cell_size + 40, x * self.cell_size + 40,
                                                 fill=color)
                # Move the robot
                self.canvas.coords(self.robot, y * self.cell_size + 10, x * self.cell_size + 10,
                                   y * self.cell_size + 40, x * self.cell_size + 40)
                self.root.after(200, move_robot, i + 1)  # Move robot every 200ms
        
        move_robot(0)

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotPuzzleApp(root)
    root.mainloop()
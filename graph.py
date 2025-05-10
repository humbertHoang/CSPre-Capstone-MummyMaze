from collections import deque

class Graph:
    def __init__(self, row_count, col_count):
        self.row_count = row_count
        self.col_count = col_count
        self.adjacency_list = {}
        
    def add_rectangle_vertex(self):
        total_vertexes = self.row_count * self.col_count 
        
        for vertex in range(total_vertexes):
            self.adjacency_list[vertex] = []
            

    def add_edge(self, vertex1, vertex2):

        self.adjacency_list[vertex1].append(vertex2)

        self.adjacency_list[vertex2].append(vertex1)
        

    def add_rectangle_edges(self):
        for row in range(self.row_count):
            for col in range(self.col_count):

                current = row * self.col_count + col
                

                if col < self.col_count - 1:
                    self.add_edge(current, current + 1)

                if row < self.row_count - 1:
                    self.add_edge(current, current + self.col_count)


    def find_all_paths(self, start, end):
        if start < 0 :
            return False

        queue = deque([[start]])
        shortest_paths = []
        visited = set([start])
        min_length = None

        while queue:
            path = queue.popleft()
            current = path[-1]

            for neighbor in self.adjacency_list[current]:
                if neighbor in visited and (min_length is not None and len(path) >= min_length):
                    continue
                
                new_path = list(path)
                new_path.append(neighbor)

                if neighbor == end:
                    shortest_paths.append(new_path[1]) # for game

                    min_length = len(new_path)
                else:
                    queue.append(new_path)
                    visited.add(neighbor)
        
        return shortest_paths


    def find_next_step(self, start, end):
        if start < 0:
            return None

        visited = set([start])
        queue = deque([[start]])
        
        while queue:

            path = queue.popleft()
            curr_vertex = path[-1]
            
            for neighbor in self.adjacency_list[curr_vertex]:
                if neighbor in visited:
                    continue
                
                new_path = list(path)
                new_path.append(neighbor)
                

                if neighbor == end:
                    return new_path[1] if len(new_path) > 1 else end
                    # return new_path
                queue.append(new_path)
                visited.add(neighbor)


graph = Graph(6, 6)

graph.add_rectangle_vertex()
graph.add_rectangle_edges()

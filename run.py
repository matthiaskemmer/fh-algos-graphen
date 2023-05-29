import csv
import time 
import heapq

class Graph:
    def __init__(self):
        self.data = dict()

    def load_data(self, path: str):
        with open(path, "r") as file:
            reader = csv.reader(file, delimiter=" ", quotechar='"')
            for row in reader:
                line_name = row[0].strip(":")
                stations = row[1:]
                self.__load_station_data(stations, line_name)
    
    def find_path(self, start: str, end: str):
        print(f"Search path between '{start}' and '{end}'")

        startTime = time.time() # MESSUNG LAUFZEIT DES ALGORITHMUS START
        # Dijkstra
        distances = {station: float('inf') for station in self.data.keys()}
        distances[start] = 0
        previous = {station: None for station in self.data.keys()}
        line_changes = {station: 0 for station in self.data.keys()}
        visited = set() #empty set data structure
        start_line = None

        while True:
            min_distance = float('inf')
            min_station = None
            for station in self.data.keys():
                if distances[station] < min_distance and station not in visited:
                    min_distance = distances[station]
                    min_station = station

            if min_station is None or min_station == end:
                break

            visited.add(min_station)

            for neighbor, cost, line_name in self.data[min_station]:
                new_distance = distances[min_station] + cost
                line_change_cost = 0 if previous[min_station] is None or line_name == previous[min_station][1] else 1
                new_distance += line_change_cost

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = (min_station, line_name)
                    if start_line is None:
                        start_line = line_name
                    line_changes[neighbor] = line_changes[min_station] + line_change_cost

        # shortest path
        path = []
        current = end
        while current:
            path.append(current)
            current = previous[current][0] if current != start else None
        path = path[::-1]  # reverse path
        
        endeTime = time.time() # MESSUNG LAUFZEIT DES ALGORITHMUS ENDE
        elapsedTime = (endeTime - startTime) * 1000
        
        for i, station in enumerate(path):
            if i == 0:
                if start_line is not None:
                    print(f"Start at Line {start_line}: \n", end="")
            print(station, end="")
            if i < len(path) - 1:
                if previous[station] is not None and previous[station][1] != previous[path[i + 1]][1]:
                    print(f"\n(Line change to {previous[path[i + 1]][1]})", end="")
            print()

        print("The Dijkstra Algorithm using heapq algorithm took {:.3f}ms to find the path".format(elapsedTime))
        print(f"Total distance: {distances[end]}")
        print(f"Total line changes: {line_changes[end]}")
    
    def find_path1(self, start: str, end: str):
        print(f"Search path between '{start}' and '{end}'")

        startTime = time.time()  

        # Dijkstra
        distances = {station: float('inf') for station in self.data.keys()}
        distances[start] = 0
        previous = {station: None for station in self.data.keys()}
        line_changes = {station: 0 for station in self.data.keys()}
        visited = set()  # Empty set
        start_line = None

        queue = [(0, start)]  # priority queue of (distance, station) tuples
        while queue:
            current_distance, current_station = heapq.heappop(queue)
            if current_station == end:
                break

            if current_distance > distances[current_station]:
                continue

            visited.add(current_station)

            for neighbor, cost, line_name in self.data[current_station]:
                if neighbor not in visited:
                    new_distance = current_distance + cost
                    line_change_cost = 0 if previous[current_station] is None or line_name == previous[current_station][1] else 1
                    new_distance += line_change_cost

                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = (current_station, line_name)
                        if start_line is None:
                            start_line = line_name
                        line_changes[neighbor] = line_changes[current_station] + line_change_cost
                        heapq.heappush(queue, (new_distance, neighbor))
                        #print(queue)

        # Shortest path
        path = []
        current = end
        while current:
            path.append(current)
            current = previous[current][0] if current != start else None
        path = path[::-1]  # reverse path

        endTime = time.time()  
        elapsedTime = (endTime - startTime) * 1000  # time in milliseconds

        for i, station in enumerate(path):
            if i == 0:
                if start_line is not None:
                    print(f"Start at Line {start_line}: \n", end="")
            print(station, end="")
            if i < len(path) - 1:
                if previous[station] is not None and previous[station][1] != previous[path[i + 1]][1]:
                    print(f"\n(Line change to {previous[path[i + 1]][1]})", end="")
            print()

        print("The Dijkstra Algorithm using heapq algorithm took {:.3f}ms to find the path".format(elapsedTime))
        print(f"Total distance: {distances[end]}")
        print(f"Total line changes: {line_changes[end]}")

    def __load_station_data(self, stations: list[str], line_name: str):
        for i in range(0, len(stations) - 1, 2):
            station1 = stations[i]
            cost = int(stations[i + 1])
            station2 = stations[i + 2]

            if station1 not in self.data.keys():
                self.data[station1] = list()
            if station2 not in self.data.keys():
                self.data[station2] = list()

            self.data[station1].append((station2, cost, line_name))
            self.data[station2].append((station1, cost, line_name))

    def user_input(self):
        start, end = False, False
        while not start or not end:
            start = input("Start station: ")
            if start not in self.data.keys():
                print(f"Start station '{start}' was not found.")
                start = False
                continue

            end = input("Destination station: ")
            if end not in self.data.keys():
                print(f"Destination station '{end}' was not found.")
                end = False

        if start and end:
            self.find_path(start, end) #not using heapq
            self.find_path1(start, end) # using heapq


if __name__ == "__main__":
    path = "data/UE03_data.txt"
    graph = Graph()
    graph.load_data(path)
    #print(graph.data["Westbahnhof"])  # Example station data
    #print(graph.data)
    graph.user_input()
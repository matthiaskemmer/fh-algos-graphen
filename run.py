import csv


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
        # TODO

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
            self.find_path(start, end)


if __name__ == "__main__":
    path = "data/UE03_data.txt"
    graph = Graph()
    graph.load_data(path)
    # print(graph.data["Westbahnhof"])  # Example station data
    graph.user_input()

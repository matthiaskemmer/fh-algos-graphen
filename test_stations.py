import csv

def list_all_stations():
    all_stations = set()
    path = "data/UE03_data.txt"
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=" ", quotechar='"')
        for row in reader:
            # all_stations.add(row[0].strip(":"))  # Line names
            stations = row[1:]
            for station in stations:
                if len(station) > 1:
                    all_stations.add(station)

    for item in sorted(all_stations):
        print(item)
    print(len(all_stations))

if __name__ == "__main__":
    list_all_stations()
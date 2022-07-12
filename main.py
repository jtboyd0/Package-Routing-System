import csv
import datetime
# Jacob Boyd ID: #001393514

"""
The WGUPS Package routing program was created to simulate the delivery of packages for the WGU headquarters.
The program allows the user to find a semi optimal route for package delivery so that each package can be delivered
to the correct location on time. The user is also able to retrieve information on any package at any time throughout
the routing process.

Time-space complexity for entirety of program.

 Space Complexity
 ----------------

    O(n^3)

 Time Complexity
 ----------------

    O(n^3*log(n))
"""

class ChainHashTable:
    """
    Class used to represent a chaining hash table data structure.

    Attributes
    ----------
    table : list
        a list of lists that contain items

    Methods
    ----------
    insert(key, item)
        Inserts an item into a list contained in the table

    search(key)
        Searches for a key in the table
    """

    def __init__(self, initial_capacity=10):
        """
        Parameters
        ----------
        initial_capacity : int, optional
            The number of lists that exist in the table. (Default is 10)
        """
        self.table = []
        for index in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        """
        Inserts an item with a given key into the table.

        Parameters
        ----------
        key : int
            The unique key that an item is given.
        item : Object
            The item that is stored in the hash(key) % len(table) bucket in the table.

        :returns true, If the item is added to the list.

        Space Complexity
        ----------------

            O(n)

        Time Complexity
        ----------------

            O(n)
        """
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        """
        Searches for an item in the table with a given key.

        Parameters
        ----------
        key : int
            The key that is used to identify an item in the table.

        Space Complexity
        ----------------

            O(n)

        Time Complexity
        ----------------

            O(n)
        """
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None


class Truck:
    """
    Class used to represent a truck for the 'WGUPS' service.

    Attributes
    ----------
    truck_id : int
        Unique id to identify the truck object
    packages : list
        A list of packages that are onboard the truck (Default is [])
    distance_traveled : float
        The total distance traveled by the truck (Default is 0.0)
    location_id : int
        The location id of where the truck is currently located (Default 0 (Hub))
    truck_time : Datetime
        The time onboard the truck
    rate : float
        The rate the truck travels (Default is 18.0)

    Methods
    ----------
    load_truck(priority_packages_list, non_priority_packages_list)
        Loads packages onto the truck. Packages that have priority are given the first chance to be loaded onto the
        truck and then non-priority packages are loaded.
    find_shortest_distance()
        Finds the package in the truck's on board packages with the shortest distance from the truck's current location.
    increment_time_and_distance(package_id)
        Increments the truck's distance travelled and truck's time based on the package found by the
         find_shortest_distance method.
    load_package(package_id)
        The load package method adds a package to the truck's package list and updates the packages status in the hash
         table.
    deliver_package(package_id)
        The deliver package method offloads the package from the truck and updates the packages status and delivered time.
    return_to_hub()
        The truck returns to the hub.
    """

    def __init__(self, truck_id, truck_time):
        """
        Parameters
        ----------
        truck_id : int
            Unique truck identifier
        truck_time : Datetime
            The time that the truck starts its day.
        """
        self.truck_id = truck_id
        self.packages = []
        self.distance_traveled = 0.0
        self.location_id = 0
        self.truck_time = truck_time
        self.rate = 18.0

    def load_truck(self, priority_packages_list, non_priority_packages_list):
        """
        Load truck loads the packages on to the truck.

        Parameters
        ----------
        priority_packages_list : list
            The list of priority packages
        non_priority_packages_list : list
            The list of non-priority packages

        Space Complexity
        ----------------

            O(n)

        Time Complexity
        ----------------

            O(n^2)
        """
        for p_id in priority_packages_list:
            if len(self.packages) == 16:
                break
            if p_id in self.packages:
                continue

            package = my_hash_packages.search(p_id)
            if package.req_truck == self.truck_id or package.req_truck == 0:
                if package.time_available <= self.truck_time:
                    if package.group == 0:
                        self.load_package(p_id)
                    elif len(self.packages) + group_count_dictionary[package.group] <= 16:
                        group_id = package.group
                        for pack_id in priority_packages_list:
                            package_with_group = my_hash_packages.search(pack_id)
                            if package_with_group.group == group_id:
                                self.load_package(pack_id)
        for p_id in non_priority_packages_list:
            if len(self.packages) == 16:
                break
            package = my_hash_packages.search(p_id)
            if package.time_available <= self.truck_time:
                self.load_package(package.id)

    def find_shortest_distance(self):
        """
        Finds the package in the truck's on board packages that is closest to the truck's current location.

        :return The package id of the package the shortest distance from the truck's current location

        Space Complexity
        ----------------

            O(n)

        Time Complexity
        ----------------

            O(n)
        """
        min_distance = 100
        package_id = -1
        for package in self.packages:
            package_location = my_hash_packages.search(package).loc_id
            package_distance = float(locations[self.location_id].distances[package_location])
            if package_distance < min_distance:
                package_id = package
                min_distance = package_distance
        return package_id

    def increment_time_and_distance(self, package_id):
        """
        Calculates the time and distance traveled and adds both respectively to the truck's attributes. (Modifying them)

        Parameters
        ----------
        package_id : int
            The package id that is closest to the truck's current location

        Space Complexity
        ----------------

            O(1)

        Time Complexity
        ----------------

            O(1)
        """
        package = my_hash_packages.search(package_id)
        package_location = package.loc_id
        distance = float(locations[self.location_id].distances[package_location])
        time_traveled = datetime.timedelta(seconds=float(distance / self.rate) * 3600)
        self.truck_time = self.truck_time + time_traveled
        self.distance_traveled = self.distance_traveled + distance
        self.location_id = package_location

    def load_package(self, package_id):
        """
        Loads a package onto the truck. (Adds a package to the Truck's package list)

        Parameters
        ----------
        package_id : int
            The id of the package to be added to the truck's package list.

        Space Complexity
        ----------------

            O(1)

        Time Complexity
        ----------------

            O(1)
        """
        loaded_package = my_hash_packages.search(package_id)
        loaded_package.time_pickup = self.truck_time
        self.packages.append(package_id)

    def deliver_package(self, package_id):
        """
        Offloads a package from the truck. (Removes a package from the Truck's package list)

        Parameters
        ----------
        package_id : int
            The id of the package to be removed from the truck's package list.

        Space Complexity
        ----------------

            O(1)

        Time Complexity
        ----------------

            O(1)
        """
        delivered_package = my_hash_packages.search(package_id)
        delivered_package.time_delivered = self.truck_time
        self.increment_time_and_distance(package_id)
        self.packages.remove(package_id)

    def return_to_hub(self):
        """
        The truck returns to the hub. (Location id 0)

        Space Complexity
        ----------------

            O(1)

        Time Complexity
        ----------------

            O(1)
        """
        distance = float(locations[self.location_id].distances[0])
        time_traveled = datetime.timedelta(seconds=float(distance / self.rate) * 3600)
        self.truck_time = self.truck_time + time_traveled
        self.distance_traveled = self.distance_traveled + distance
        self.location_id = 0


class Statuses:
    UNAVAILABLE = 'Package Unavailable'
    DEPOT = 'In Depot'
    EN_ROUTE = 'En Route'
    DELIVERED = 'Delivered'


class Package:
    """
    Class used to represent a package obtained and delivered by WGUPS.

    Attributes
    ----------
    id : int
        The package's unique identifier
    address : str
        The package's delivery address
    city : str
        The package's associated city
    state : str
        The package's associated state
    zip : str
        The package's associated zip code
    mass : float
        The package's associated mass
    group : int
        The package's associated group
    req_truck : int
        The truck id the package must be loaded onto
    status : str
        The package's status
    time_available : Datetime
        Time when the package become available in the hub
    time_pickup : Datetime
        Time when the package is picked up by a truck
    time_delivered : Datetime
        Time when the package has been delivered to its associated address
    deadline : Datetime
        Time when the package must be delivered by
    loc_id : int
        The location id of the address the package is being delivered to

    Methods
    ----------
    __str__
        Overrides the __str__ method for the package object to be able to display the object's properties
    """

    def __init__(self, p_id, address, city, state, p_zip, mass, group,
                 req_truck, status, time_available, time_pickup, time_delivered, deadline, loc_id):
        """
        Parameters
        ----------
        p_id : int
            The package's unique identifier
        address : str
            The package's delivery address
        city : str
            The package's associated city
        state : str
            The package's associated state
        p_zip : str
            The package's associated zip code
        mass : float
            The package's associated mass
        group : int
            The package's associated group
        req_truck : int
            The truck id the package must be loaded onto
        status : str
            The package's status
        time_available : Datetime
            Time when the package become available in the hub
        time_pickup : Datetime
            Time when the package is picked up by a truck
        time_delivered : Datetime
            Time when the package has been delivered to its associated address
        deadline : Datetime
            Time when the package must be delivered by
        loc_id : int
            The location id of the address the package is being delivered to
        """
        self.id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = p_zip
        self.mass = mass
        self.group = group
        self.req_truck = req_truck
        self.status = status
        self.time_available = time_available
        self.time_pickup = time_pickup
        self.time_delivered = time_delivered
        self.deadline = deadline
        self.loc_id = loc_id

    def __str__(self):
        """
        Overrides the __str__ method for the package object to display select package attributes.

        :return The string of the select package attributes

        Space Complexity
        ----------------

            O(1)

        Time Complexity
        ----------------

            O(1)
        """
        return f"{self.id:^5} {self.address:^40}{self.city:^20}{self.zip:^10}{self.mass:^10}{self.deadline.time().strftime('%H:%M:%S'):^15}{self.time_delivered.time().strftime('%H:%M:%S'):^15}"


class Location:
    """
    Class for the purpose of simulating a location that packages will be delivered to.

    Parameters
    ----------
    loc_id : int
        Unique location identifier
    name : str
        Name of the location
    address : str
        Address of the location
    distances : list
        List of distances to other locations
    """

    def __init__(self, loc_id, name, address, distances):
        """
        Parameters
        ----------
        loc_id : int
            Unique location identifier
        name : str
            Name of the location
        address : str
            Address of the location
        distances : list
            List of distances to other locations
        """
        self.loc_id = loc_id
        self.name = name
        self.address = address
        self.distances = distances


def load_package_data(file_name):
    """
    Method for creating package objects and adding those packages to a chaining hash table as well as a list of either
    priority or non-priority packages. Also, returns the number of packages handed to the hash table.

    Parameters
    ----------
    file_name : str
        The location of the file that contains the package object data.

    :return The number of packages in the file

    Space Complexity
    ----------------

        O(n)

    Time Complexity
    ----------------

        O(n^2)
    """
    num_of_packages = 0
    with open(file_name) as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',')
        next(data_reader)
        for row in data_reader:
            p_id = int(row[0])
            p_address = row[1]
            p_city = row[2]
            p_state = row[3]
            p_zip = row[4]
            p_mass = row[5]
            p_group = int(row[6])
            p_req_truck = int(row[7])
            p_status = row[8]
            p_time_available = datetime.datetime.strptime(row[9], '%H:%M').time()
            p_time_available = datetime.datetime.combine(datetime.date.today(), p_time_available)
            p_pickup_time = datetime.datetime.strptime(row[10], '%H:%M').time()
            p_pickup_time = datetime.datetime.combine(datetime.date.today(), p_pickup_time)
            p_time_delivered = datetime.datetime.strptime(row[11], '%H:%M').time()
            p_time_delivered = datetime.datetime.combine(datetime.date.today(), p_time_delivered)
            p_delivery_deadline = datetime.datetime.strptime(row[12], '%H:%M:%S').time()
            p_delivery_deadline = datetime.datetime.combine(datetime.date.today(), p_delivery_deadline)
            p_loc_id = -1
            for location in locations:
                if p_address in location.address:
                    p_loc_id = location.loc_id
            p = Package(p_id, p_address, p_city, p_state,
                        p_zip, p_mass, p_group, p_req_truck, p_status,
                        p_time_available, p_pickup_time, p_time_delivered,
                        p_delivery_deadline, p_loc_id)
            my_hash_packages.insert(p_id, p)
            num_of_packages += 1
            if p.group != 0:
                if p.group in group_count_dictionary.keys():
                    group_count_dictionary[p.group] += 1
                else:
                    group_count_dictionary[p.group] = 1

            if p.deadline < datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59, 59)) \
                    or p.req_truck != 0 or p.group != 0:
                priority_packages.append(p.id)
            else:
                non_priority_packages.append(p.id)
    return num_of_packages


def load_location_data(file_name):
    """
    Method to create location objects and add them to a list of locations.

    Parameters
    ----------
    file_name : str
        The location of the file that contains the location object data.
    """
    with open(file_name) as csv_file:
        location_reader = csv.reader(csv_file, delimiter=',')
        for row in location_reader:
            loc_id = int(row[0])
            loc_name = row[1]
            loc_address = row[2]
            loc_distances = row[3:]
            loc = Location(loc_id, loc_name, loc_address, loc_distances)
            locations.append(loc)


def route_packages(trucks):
    """
    route_packages is the core algorithm for loading and delivering packages from the whole of priority and non-priority
     package lists.

     Parameters
     ----------
     trucks : list
        The list of trucks that will be loading and delivering packages.

    Space Complexity
    ----------------

        O(n^3)

    Time Complexity
    ----------------

        O(n^3*log(n))
    """
    while priority_packages or non_priority_packages:
        for truck in trucks:
            truck.load_truck(priority_packages, non_priority_packages)
            while truck.packages:
                deliver_package = truck.find_shortest_distance()
                if deliver_package in priority_packages:
                    priority_packages.remove(deliver_package)
                elif deliver_package in non_priority_packages:
                    non_priority_packages.remove(deliver_package)
                truck.deliver_package(deliver_package)
            truck.return_to_hub()


def get_input_time():
    """
    get_input_time is a method for getting the hour, minute, and second inputted by a user and returning a time.
    :return input_time: The time inputted by the user.

    Space Complexity
    ----------------

        O(1)

    Time Complexity
    ----------------

        O(1)
    """
    hour = -1
    minute = -1
    second = -1
    print('Please enter a time\n')
    while hour > 23 or hour < 0:
        try:
            hour = int(input('Please input an hour value between 0 and 23: '))
        except ValueError:
            print('\nPlease enter an integer for the hour value...\n')
    print('\n')
    while minute > 59 or minute < 0:
        try:
            minute = int(input('Please input a minute value between 0 and 59: '))
        except ValueError:
            print('\nPlease enter an integer for the minute value.\n')
    print('\n')
    while second > 59 or second < 0:
        try:
            second = int(input('Please input a second value between 0 and 59: '))
        except ValueError:
            print('\nPlease enter an integer for the second value.\n')
    print('\n')
    input_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour, minute, second))
    print('Time: ', input_time.time())
    return input_time


# Locations is a list that stores location objects.
locations = []
load_location_data('data/location_data.csv')

# In load_package_data, packages are either added to priority packages or non_priority_packages.
priority_packages = []
non_priority_packages = []

# Each group of packages (Key) is given a (value) of how many packages are in the group.
group_count_dictionary = {}

# My hash packages stores all of the package objects in a chaining hash table data structure.
my_hash_packages = ChainHashTable()

# Creates and stores the package objects in my_hash_packages, and adds undelivered packages to either
# the priority_packages list or non_priority_packages list.
num_packages = load_package_data('data/package_data.csv')

# Create truck objects
truck_1 = Truck(1, datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0)))
truck_2 = Truck(2, datetime.datetime.combine(datetime.date.today(), datetime.time(9, 5, 0)))
truck_3 = Truck(3, datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0)))

# A list of active trucks
truck_list = [truck_1, truck_2]

# Call the core algorithm for loading and delivering packages to trucks.
route_packages(truck_list)

total_distance = 0
for truck in truck_list:
    total_distance += truck.distance_traveled

line = '\n--------------------------------------------------\n'
columns = f"{'ID':^5}{'Address':^40}{'City':^20}{'Zip':^10}{'Mass':^10}{'Deadline':^15}{'Time Delivered':^15}\t{'Status':^15}\n"

user_select_action_str = 'Please select an input:' \
                         '\n1 : Give data on all packages at a specific time' \
                         '\n2 : Give data on a specific package at a specific time' \
                         '\n3 : Quit' \
                         '\nYour Input: '

print(line)
print('Total number of miles driven to deliver all packages:', total_distance)
print(line)

user_input = '1'
user_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0))
while user_input != '3':
    user_input = input(user_select_action_str)
    print(line)
    if user_input in ['1', '2']:
        if user_input == '1':
            user_time = get_input_time()
            print(line)
            print('Printing package statuses at', user_time.time(), '...\n')
            print(columns)
            for key in range(1, num_packages + 1):
                package = my_hash_packages.search(key)
                if user_time < package.time_available:
                    print(package, f"{Statuses.UNAVAILABLE:^15}")
                elif user_time < package.time_pickup:
                    print(package, f"{Statuses.DEPOT:^15}")
                elif user_time < package.time_delivered:
                    print(package, f"{Statuses.EN_ROUTE:^15}")
                else:
                    print(package, f"{Statuses.DELIVERED:^15}")
        else:
            user_time = get_input_time()
            user_package_id = 0
            while user_package_id < 1 or user_package_id > (num_packages + 1):
                try:
                    user_package_id = int(input(f'Please input a package id between 1 and {num_packages}: '))
                except ValueError:
                    print('\nPlease enter an integer for the package id value.\n')
            package = my_hash_packages.search(user_package_id)
            print(line)
            print('Printing package status at', user_time.time(), '...\n')
            print(columns)
            if user_time < package.time_available:
                print(package, f"{Statuses.UNAVAILABLE:^15}")
            elif user_time < package.time_pickup:
                print(package, f"{Statuses.DEPOT:^15}")
            elif user_time < package.time_delivered:
                print(package, f"{Statuses.EN_ROUTE:^15}")
            else:
                print(package, f"{Statuses.DELIVERED:^15}")
        print(line)
    elif user_input == '3':
        print('Have a nice day! :)')
    else:
        print('Please select a valid input.')
        print(line)

#!/usr/bin/env python3
import math
import heapq

class Router:
    """Router class to store the weight, distance, neighbours,
    previous router and number of hops"""
    def __init__(self, label):
        self._label = label
        self._adjacent = {} #Router():weight pair
        # Set distance to infinity for all nodes
        self._distance = math.inf
        # Predecessor
        self._previous = None
        self._hops = math.inf

    def add_neighbour(self, neighbour, weight):
        """add the neighbour Router() object and the corresponding 
        weight into the self._adjacent dictionary"""
        self._adjacent[neighbour] = weight

    def remove_neighbour(self, neighbour):
        """remove the neighbour from the self._adjacent dictionary"""
        del self._adjacent[neighbour]

    def get_adjacent(self):
        """Get the self._adjacent dictonary which stores 
        all the neighbour:weight pair of the router"""
        return self._adjacent

    def get_label(self):
        """Return the label of the router"""
        return self._label

    def get_weight(self, neighbour):
        """Return the weight of edge to the named neighbour Router() object"""
        return self._adjacent[neighbour]

    def set_distance(self, dist):
        """Update the distance of the router"""
        self._distance = dist

    def get_distance(self):
        """Return the distance of the router"""
        return self._distance

    def set_previous(self, prev):
        """A pointer or a record of the selected routers' previous router in the shortest path.
        To construct and identify the shortest path after running Dijkstra"""
        self._previous = prev

    def get_previous(self):
        """Return the previous router in the shortest path"""
        return self._previous
    
    def get_hops(self):
        """Return the number of hops to the router"""
        return self._hops

    def set_hops(self, hops):
        """Update the newest hops of the router"""
        self._hops = hops

    def __lt__(self, other):
        """Use distance to compare the Routers() which is needed in Dijkstra 
        to get the Router with the shortest distance to visit.
        If the distances are the same, compare alphanumeric order of labels"""
        if self._distance != other.get_distance():
            return self._distance < other.get_distance()
        return self._label < other.get_label()

class NetworkGraph:
    """The Network graph that will contain the Routers() object and the edges"""

    def __init__(self):
        self._routers = dict() #label:Router() pair

    def add_router(self, label):
        """Method to add label:Router() pair to the NetworkGraph"""
        new_router = Router(label) #initlalise the router class
        self._routers[label] = new_router #add to the network graph
        return new_router

    def get_router(self, label):
        """Method to obtain the Router() object of the given label"""
        if label in self._routers:
            return self._routers[label]
        else:
            return None

    def get_routers(self):
        """Get the self._routers dictonary which stores all the
        Routers in the NetworkGraph in the format label:Router() pair"""
        return self._routers

    def update_edge(self, source, destination, new_weight):
        """Method to add edge, update to new weight if edge exist or remove edge in undirected network graph"""
        # Ensure source and destination routers are in the graph
        if source not in self.get_routers():
            self.add_router(source)
        if destination not in self.get_routers():
            self.add_router(destination)

        source_router = self.get_router(source)
        dest_router = self.get_router(destination)

        # Remove the edge (both directions) if new_weight is -1
        if new_weight == -1:
            # Check if the edge exists before attempting to remove
            if dest_router in source_router.get_adjacent() and source_router in dest_router.get_adjacent():
                source_router.remove_neighbour(dest_router)
                dest_router.remove_neighbour(source_router)
        else:
            # Update the weight of the edge from source to destination and vice versa
            source_router.add_neighbour(dest_router, new_weight)
            dest_router.add_neighbour(source_router, new_weight)

    def dijkstra_spf(self, start):
        """Apply Dijkstra Algorithm to the selected starting router"""
        #INITIALISATION
        router_list = list(self.get_routers().values())
        router_list_set = set(router_list) # N
        start_router = self.get_router(start)
        visited_routers = set()
        visited_routers.add(start_router) # N’ = {u}

        for router in router_list: #for all nodes v
            if router in start_router.get_adjacent(): #if v is a neighbour of u
                router.set_distance(router.get_weight(start_router)) #then D(v) = c(u,v)
                router.set_previous(start_router)
                router.set_hops(1)  # Direct neighbor, 1 hop from start
            else:
                router.set_distance(math.inf) #else D(v) = ∞
                router.set_previous(None)
                router.set_hops(math.inf)  # Initially set to infinity

        start_router.set_distance(0)
        start_router.set_hops(0)  # Start router has 0 hops to itself

        heapq.heapify(router_list) #convert the list to heap

        #LOOP
        while visited_routers != router_list_set: # while N' != N
            #find w not in N’ such that D(w) is a minimum
            current = heapq.heappop(router_list) #pop from the heap
            if current in visited_routers:
                continue
            visited_routers.add(current) # add w to N’
            for neighbour, weight in current.get_adjacent().items():
                if neighbour not in visited_routers:
                    new_distance = current.get_distance() + weight
                    new_hops = current.get_hops() + 1
                    if neighbour.get_distance() > new_distance:
                        neighbour.set_distance(new_distance) #D(v) = min(D(v), D(w)+ c(w,v) )
                        neighbour.set_previous(current)
                        neighbour.set_hops(new_hops)
                        #Push the updated neighbour back onto the heap
                        heapq.heappush(router_list, neighbour)
                    # if the distances are the same check the number of hops of the neighbour
                    elif neighbour.get_distance() == new_distance and neighbour.get_hops() > new_hops:
                        # if the number of hops of the neighbour is higher: 
                        # Set the previous router of the neighbour to current hop with the lesser hops
                        neighbour.set_previous(current)
                        neighbour.set_hops(new_hops)  # Update shorter hops

    def get_shortest_path(self, destination):
        """Method to retrieve the shortest path from source to destination."""
        # Check if a path to the destination router was found
        dest_router=self.get_router(destination)
        if dest_router.get_distance() == math.inf:
            return [], math.inf  # No path found, return empty path and infinite distance

        # Retrieve the shortest path and cost to the destination router
        path = []

        # Backtrack from destination to source to reconstruct the path
        current = dest_router
        while current:
            path.append(current.get_label())
            current = current.get_previous()

        return path, dest_router.get_distance()

    def print_neighbour_table(self, router):
        """Method to print neighbour table of the selected router"""
        current_router = self.get_router(router)
        neighbour_table = []

        #find all neighbours
        for neighbour, weight in current_router.get_adjacent().items():
            neighbour_table.append(f"{neighbour.get_label()}|{weight}")

        #sort alphabetically
        neighbour_table.sort()

        #print
        print(f"{router} Neighbour Table:")
        if neighbour_table:
            print("\n".join(neighbour_table))
        print("")  # Blank line at the end

    def print_lsdb_table(self, router):
        """Method to print LSDB table of the selected router by traversing via DFS"""
        current_router = self.get_router(router)
        lsdb_table = set()  # Use a set for efficient edge tracking compared to list
        linked_routers = [current_router]  # Use a list as a stack for DFS

        visited = set()  # Track visited routers to avoid cycles

        while linked_routers:
            current = linked_routers.pop()

            if current in visited:
                continue

            visited.add(current)

            for neighbour, weight in current.get_adjacent().items():
                # Ensure consistent order of router labels for LSDB entry
                if current.get_label() < neighbour.get_label():
                    lsdb_entry = f"{current.get_label()}|{neighbour.get_label()}|{weight}"
                else:
                    lsdb_entry = f"{neighbour.get_label()}|{current.get_label()}|{weight}"

                # Add the LSDB entry to the set (automatically handles duplicates)
                lsdb_table.add(lsdb_entry)

                # Add the neighbour to the stack
                if neighbour not in visited:
                    linked_routers.append(neighbour)

        # Convert the set to a sorted list for output
        sorted_lsdb_table = sorted(lsdb_table)

        # Print the LSDB table
        print(f"{router} LSDB:")
        if sorted_lsdb_table:
            print("\n".join(sorted_lsdb_table))
        print("")  # Blank line at the end

    def print_routing_table(self, router):
        """Method to print routing table of the selected router"""
        routing_table = []

        # Generate shortest path
        for destination in sorted(self.get_routers().keys()):
            if destination == router:
                continue  # Skip the current router itself

            # Get the shortest path to the destination router
            path, total_cost = self.get_shortest_path(destination)

            if path:
                next_hop = path[-2]  # Next hop in the shortest path (second to last router)
                routing_table.append(f"{destination}|{next_hop}|{total_cost}")

        # Print the Routing Table for the current router
        routing_table.sort()
        print(f"{router} Routing Table:")
        if routing_table:
            print("\n".join(routing_table))
        print("")  # Blank line at the end


def main():
    """Awaiting input until given END command"""
    # Create a network graph instance
    graft = NetworkGraph()
    current_stage = None
    while True:
        item = input().strip() #remove trailing space

        if item == "END":
            break #terminate the while loop

        #when receive LINKSTATE, next few lines will run codes under LINKSTATE
        if item == "LINKSTATE":
            current_stage = "LINKSTATE"
            continue

        #when receive UPDATE, next few lines will run codes under UPDATE
        if item == "UPDATE":
            current_stage = "UPDATE"
            continue

        #codes under LINKSTATE
        if current_stage == "LINKSTATE":
            #split the string
            parts = item.split()
            fro, to = parts[0].split("-")
            weight = parts[1]
            if len(parts) > 2:
                chosen_routers = parts[2].split(",")
            else:
                chosen_routers = []
            #add the edges
            graft.update_edge(fro, to, int(weight))
            #Print the output for each chosen routers
            if chosen_routers:
                for router in chosen_routers:
                    graft.dijkstra_spf(router)
                    graft.print_neighbour_table(router)
                    graft.print_lsdb_table(router)
                    graft.print_routing_table(router)

        #codes under UPDATE
        elif current_stage == "UPDATE":
            #split the string
            parts = item.split()
            fro, to = parts[0].split("-")
            weight = parts[1]
            if len(parts) > 2:
                chosen_routers = parts[2].split(",")
            else:
                chosen_routers = []
            #update the edges
            graft.update_edge(fro, to, int(weight))
            #Print the output for each chosen routers
            if chosen_routers:
                for router in chosen_routers:
                    graft.dijkstra_spf(router)
                    graft.print_neighbour_table(router)
                    graft.print_lsdb_table(router)
                    graft.print_routing_table(router)

        #default codes when the program starts
        else:
            graft.add_router(item) #initialise router nodes

if __name__ == "__main__":
    main()

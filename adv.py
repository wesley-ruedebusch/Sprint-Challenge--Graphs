from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class AdvTraversal():
    def __init__(self):
        self.graph = dict()
        self.path = []
        self.dir_reverse = {'n': 's', 'e': 'w', 's': 'n',  'w': 'e'}
        self.reverse_path = []
        self.current_room = player.current_room.id

    def traverse_graph(self):
        # add first room to get started
        self.graph[self.current_room] = {}
        exits = player.current_room.get_exits()
        for e in exits:
            self.graph[self.current_room].update({e: '?'})
            
        while len(self.graph) < len(room_graph):
            # check what moves are available
            moves = self.available_moves()
            # if there is an available new exit
            if moves != False:
                # move in a random direction through a new exit
                self.random_move(self.current_room, moves)
            # else, backtrack to last room with a new exit
            else:
                # else, navigate back to a room with an unexplored exit
                while moves is False:
                    # pop off the last reverse direction
                    backtrack_dir = self.reverse_path.pop()
                    player.travel(backtrack_dir)
                    self.current_room = player.current_room.id
                    self.path.append(backtrack_dir)
                    moves = self.available_moves()

        return self.path

    def available_moves(self):
        start_room = self.current_room
        exits = self.graph[start_room]
        new_moves = []
        for e in exits:
            if exits[e] == '?':
                new_moves.append(e)
        if len(new_moves) > 0:
            return new_moves
        else:
            return False

    def random_move(self, start_room, moves):
        direction = random.choice(moves)
        player.travel(direction)

        # set new room player is in
        self.current_room = player.current_room.id

        # if room is new and not in graph
        # add it and initialize possible exits
        if self.current_room not in self.graph:
            self.graph[self.current_room] = {}
            exits = player.current_room.get_exits()
            for e in exits:
                self.graph[self.current_room].update({e: '?'})

        # update graph with connection to new room
        self.graph[start_room][direction] = self.current_room
        # make the connection go both ways
        self.graph[self.current_room][self.dir_reverse[direction]] = start_room
        

        # add move to traversal path
        self.path.append(direction)
        self.reverse_path.append(self.dir_reverse[direction])


at = AdvTraversal()
traversal_path = at.traverse_graph()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

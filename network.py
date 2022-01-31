#!/usr/bin/python3
import sys

class Node():
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name
        self.points_to = None
        self.final_length = None
        self.is_checked = False

class Connection():
    def __init__(self, uid: int, connection1: int, connection2: int, length: (int, float)):
        self.uid = uid
        self.connection1 = connection1
        self.connection2 = connection2
        self.length = length

class Network():
    def __init__(self):
        self.nodes = []
        self.connections = []

def init():
    ### Erstellt das netzwerk
    net = Network()

    ### Erställt alle Punkte
    net.nodes.append(Node(0, "Arlhausen"))
    net.nodes.append(Node(1, "Morbach"))
    net.nodes.append(Node(2, "Chelzey"))
    net.nodes.append(Node(3, "X1"))
    net.nodes.append(Node(4, "Niedergau"))
    net.nodes.append(Node(5, "Delgar"))
    net.nodes.append(Node(6, "Imstadt"))
    net.nodes.append(Node(7, "Budingen"))
    net.nodes.append(Node(8, "X2"))
    net.nodes.append(Node(9, "Lupera"))
    net.nodes.append(Node(10, "Hundorf"))
    net.nodes.append(Node(11, "X3"))
    net.nodes.append(Node(12, "Giwelau"))
    net.nodes.append(Node(13, "Pappstadt"))
    net.nodes.append(Node(14, "Krupsing"))
    net.nodes.append(Node(15, "Eindhofen"))
    net.nodes.append(Node(16, "Flughafen"))
    net.nodes.append(Node(17, "Oppenhaim"))
    
    ### Erstellt die Verbindungen
    net.connections.append(Connection(0,  0, 1, 36))
    net.connections.append(Connection(1,  0, 5, 36))
    net.connections.append(Connection(2,  1, 6, 43))
    net.connections.append(Connection(3,  1, 2, 31))
    net.connections.append(Connection(4,  2, 6, 40))
    net.connections.append(Connection(5,  1, 3, 12))
    net.connections.append(Connection(6,  2, 3, 23))
    net.connections.append(Connection(7,  3, 4, 29))
    net.connections.append(Connection(8,  0, 7, 69))
    net.connections.append(Connection(9,  3, 7, 26))
    net.connections.append(Connection(10, 0, 4, 22))
    net.connections.append(Connection(11, 4, 5, 20))
    net.connections.append(Connection(12, 5, 7, 64))
    net.connections.append(Connection(13, 5, 9, 95))
    net.connections.append(Connection(14, 4, 8, 30))
    net.connections.append(Connection(15, 7, 8, 32))
    net.connections.append(Connection(16, 8, 9, 40))
    net.connections.append(Connection(17, 6, 7, 34))
    net.connections.append(Connection(18, 7, 10, 30))
    net.connections.append(Connection(19, 8, 11, 23))
    net.connections.append(Connection(20, 9, 10, 106))
    net.connections.append(Connection(21, 6, 10, 65))
    net.connections.append(Connection(22, 6, 13, 55))
    net.connections.append(Connection(23, 10, 13, 34))
    net.connections.append(Connection(24, 10, 11, 29))
    net.connections.append(Connection(25, 9, 12, 58))
    net.connections.append(Connection(26, 11, 12, 30))
    net.connections.append(Connection(27, 11, 14, 20))
    net.connections.append(Connection(28, 10, 14, 31))
    net.connections.append(Connection(29, 13, 14, 25))
    net.connections.append(Connection(30, 12, 14, 58))
    net.connections.append(Connection(31, 13, 16, 57))
    net.connections.append(Connection(32, 13, 17, 91))
    net.connections.append(Connection(33, 14, 16, 29))
    net.connections.append(Connection(34, 14, 15, 31))
    net.connections.append(Connection(35, 12, 15, 60))
    net.connections.append(Connection(36, 15, 16, 79))
    net.connections.append(Connection(37, 16, 17, 14))
    net.connections.append(Connection(38, 15, 17, 102))

    ### return the Preperated Network
    return net

def clean_net(net):
    for node in net.nodes:
        node.final_length = None
        node.is_checked = False
        node.points_to = None

def gen_dot(net, name):
    import subprocess
    with open(f"{name}.dot", "w") as f:
        f.write("graph %s{\n" % name)
        for node in net.nodes:
            f.write(f'    {node.uid} [label="{node.name}"]\n')
        for connection in net.connections:
            f.write(f'    {connection.connection1} -- {connection.connection2} [label="{connection.length}"]\n')
        f.write("}\n")
    args = ["sfdp","-Tsvg",f"{name}.dot","-o",f"{name}.svg"]
    subprocess.call(args)
        
        


def get_connections(uid, net):
    connections = []
    for connection in net.connections:
        if connection.connection1 == uid or connection.connection2 == uid:
            connections.append(connection)
    return connections

def get_node(uid, net):
    target_node = None
    for node in net.nodes:
        if node.uid == uid:
            target_node = node
            break
    return target_node

def get_node_index(uid, net):
    index = 0
    for node in net.nodes:
        if node.uid == uid:
            break
        else:
            index += 1
    return index

def main():
    net = init()
    clean_net(net)      # not needed in this case

    starting_node = 9
    target_node = 16

    net.nodes[starting_node].final_length = 0
    while True:
        # grab the node with the shortest path
        node_id = None
        for node in net.nodes:
            if (node.is_checked == False) and (node.final_length != None):
                if node_id == None:
                    node_id = node.uid
                elif get_node(node_id, net).final_length > node.final_length:
                    node_id = node.uid
        # check if the network has been solved yet
        if node_id == None:
            break

        # get the connections and "true" node id
        true_node_id = get_node_index(node_id, net)
        connections = get_connections(node_id, net)

        # mark the current node as checked
        net.nodes[true_node_id].is_checked = True


        for connection in connections:
            # gets the connected node id, and waylength
            if connection.connection1 == node_id:
                node_connection_id = connection.connection2
            else:
                node_connection_id = connection.connection1
            length = connection.length

            # gets the "true" node id and calculates the new length
            true_node_connection_id = get_node_index(node_connection_id, net)
            new_length = net.nodes[true_node_id].final_length + length

            # main logic of the algoryth
            if net.nodes[true_node_connection_id].is_checked:       # checks if node has been checked already
                continue # Node is checked already


            # checks if the Node doesnt have a length yet or
            # checks if the Node length is longer than the new length
            elif net.nodes[true_node_connection_id].final_length == None or net.nodes[true_node_connection_id].final_length > new_length:
                net.nodes[true_node_connection_id].points_to = node_id          # updates the pointer
                net.nodes[true_node_connection_id].final_length = new_length    # updates the length
            
    path = [target_node]
    node = target_node
    while True:
        node = net.nodes[node].points_to
        path.insert(0, node)
        if node == starting_node:
            break
    print(net.nodes[target_node].final_length)
    print(path)
        



if __name__ == "__main__":
    main()
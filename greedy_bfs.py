import collections
 
def main():
    global f 
    f= set()
    starting_node = [[0, 0]]
    jugs = set_jug_values()
    goal_amount = set_goal(jugs)
    check_dict = {}
    
    search(starting_node, jugs, goal_amount, check_dict)
    print('\nexplored nodes:',f)
    print('no of explored nodes:',len(f))

def get_index(node):
    return pow(7, node[0]) * pow(5, node[1])

def set_jug_values():
    
    jugs = []
    temp = int(input("Enter first jug volume (>1): "))
    while temp < 1:
        temp = int(input("Enter a valid amount (>1): "))       
    jugs.append(temp)
    
    temp = int(input("Enter second jug volume (>1): "))
    while temp < 1:
        temp = int(input("Enter a valid amount (>1): "))     
    jugs.append(temp)
    
    return jugs
 
def set_goal(jugs):
     
    max_amount = max(jugs[0], jugs[1])
    s = "Enter the goal amount of water (1 - {0}): ".format(max_amount)
    goal_amount = int(input(s))
    while goal_amount < 1 or goal_amount > max_amount:
        goal_amount = int(input("Enter a valid amount (1 - {0}): ".format(max_amount)))
        
    return goal_amount

def is_goal(path, goal_amount):
    return abs(path[-1][0] - goal_amount) == 0

def been_there(node, check_dict):
    return check_dict.get(get_index(node), False)

def next_transitions(jugs, path, check_dict):
      
    result = []
    next_nodes = []
    node = []
    
    a_max = jugs[0]
    b_max = jugs[1]
    
    a = path[-1][0]   
    b = path[-1][1]   

    # 1. fill in the first jug
    node.append(a_max)
    node.append(b)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 2. fill in the second jug
    node.append(a)
    node.append(b_max)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 3. second jug to first jug
    node.append(min(a_max, a + b))
    node.append(b - (node[0] - a))   
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 4. first jug to second jug
    node.append(min(a + b, b_max))
    node.insert(0, a - (node[0] - b))
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 5. empty first jug
    node.append(0)
    node.append(b)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 6. empty second jug
    node.append(a)
    node.append(0)
    if not been_there(node, check_dict):
        next_nodes.append(node)

    # create a list of next paths
    for i in range(0, len(next_nodes)):
        temp = list(path)
        temp.append(next_nodes[i])
        result.append(temp)
        
    else:
        for nnode in next_nodes:
            f.add((nnode[0],nnode[1]))
           
    return result

def transition(old, new, jugs):
    a = old[0]
    b = old[1]
    a_prime = new[0]
    b_prime = new[1]
    a_max = jugs[0]
    b_max = jugs[1]

    if a > a_prime:
        if b == b_prime:
            return "Clear {0}-liter jug:\t\t\t".format(a_max)
        else:
            return "Pour {0}-liter jug into {1}-liter jug:\t".format(a_max, b_max)
    else:
        if b > b_prime:
            if a == a_prime:
                return "Clear {0}-liter jug:\t\t\t".format(b_max)
            else:
                return "Pour {0}-liter jug into {1}-liter jug:\t".format(b_max, a_max)
        else:
            if a == a_prime:
                return "Fill {0}-liter jug:\t\t\t".format(b_max)
            else:
                return "Fill {0}-liter jug:\t\t\t".format(a_max)


def print_path(path, jugs):
    print("initial state :\t\t\t\t", tuple(path[0]))
    for i in  range(0, len(path) - 1):
        print(i+1,":", transition(path[i], path[i+1], jugs), tuple(path[i+1]))

def search(starting_node, jugs, goal_amount, check_dict):
     
    print("\n--- Implementing GBFS ---")

    goal = []
    accomplished = False
    
    q = collections.deque()
    q.append(starting_node)
    
    while len(q) != 0:
        path = q.pop()
        check_dict[get_index(path[-1])] = True
        if is_goal(path, goal_amount):
            accomplished = True
            goal = path
            break

        next_moves = next_transitions(jugs, path, check_dict)
        if(len(next_moves) == 1):
            q.appendleft(next_moves[0])
        else:
            if(abs(next_moves[0][-1][0] - goal_amount) >= abs(next_moves[1][-1][0] - goal_amount)):
                q.append(next_moves[1])
            else:
                q.append(next_moves[0])
        
                

    if accomplished:
        print("The goal is achieved\nPrinting the sequence of the moves...\n")
        print_path(goal, jugs)
    else:
        print("Problem cannot be solved.")


if __name__ == '__main__':
    main()
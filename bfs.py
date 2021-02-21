import copy

class Card:
    def __init__(self,string):
        
        coler = string[-1]
        string = string[:-1]
        number = int(string)
        self.coler = coler
        self.number = number
        
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.number == other.number and self.coler == other.coler

    def __str__(self):
        return "{}{}".format(self.number, self.coler)

    
    def __repr__(self):  
        return "{}{}".format (self.number, self.coler)  

    



states = []
frontier = []
explored = []

k,m,n = map(int,input().split())
def get_input():
    state = {}
    for x in range(k+1):
        state[x] = [] 
    state[0]=[""]
    for x in range(1,k+1):
        for i in input().split():
            if i == "#":
                state[x].append("#")
            else:
                state[x].append(Card(i)) 
    states.append(state)
    frontier.append(state)
    # print(state)
    return state

def print_state(state):
    for i in state.keys():
        if i ==0 :
            print("path is:")
            for i in state[0][1:]:
                print(i)
            print()
            # pass
        else:       
            for x in state[i]:
                print(x , end = " ")
            print()
    print()


def goal_check(state):
    for hand in range(1,k+1):
        if state[hand][-1] =='#':
            continue
        for i in  range(len(state[hand])-1):
            if (state[hand][i].coler == state[hand][i+1].coler) and (state[hand][i].number > state[hand][i+1].number) :
                pass
            else:
                return False
    return True

def equal_dicts(d1, d2, ignore_key):
    # ignored = set(ignore_keys)
    for k1, v1 in d1.items():
        if k1 is not  ignore_key and (k1 not in d2 or d2[k1] != v1):
            return False
    for k2, v2 in d2.items():
        if k2 is not ignore_key and k2 not in d1:
            return False
    return True

def move_Card(state,source_hand,des_hand,flag):
    n_state = copy.deepcopy(state)
    if flag:
        n_state[des_hand].pop()
    card = n_state[source_hand].pop()
    if(len(n_state[source_hand]) == 0):
        n_state[source_hand].append('#')
    n_state[des_hand].append(card)
    string = "card '{}' move from hand {} to hand {}".format(card,source_hand,des_hand)
    n_state[0].append(string)

    for i in states:
        if(equal_dicts(n_state,i,0)):
            return False,0
    states.append(n_state)
    frontier.append(n_state)
    if (goal_check(n_state)):
        print("we found goal")
        return True,n_state
    else:
        return False,0


def succesor(state):
    explored.append(state)
    for source_hand in range(1,k+1):
        try:
            last_card_of_source_hand =state[source_hand][-1]
         
            if last_card_of_source_hand=='#':
                continue
            # print("source_hand ",end=" ")
            # print(state[source_hand])
            for des_hand in range(1,k+1):
             
                if des_hand == source_hand : 
                    continue
                # print("des_hand ",end=" ")
                # print(state[des_hand])
                last_card_of_des_hand = state[des_hand][-1]
                if last_card_of_des_hand=='#':
                    flag,goal_state=move_Card(state,source_hand,des_hand,1)
                    if(flag): 
                        return True,goal_state
                    continue
                
                if last_card_of_des_hand.number > last_card_of_source_hand.number:
                    flag,goal_state=move_Card(state,source_hand,des_hand,0)
                    if(flag):
                        return True,goal_state
                
        except:
            pass
    
    return False,0


def bfs():
    get_input()

    while True:
        if frontier:
            expanding = frontier.pop(0)
            goal,goal_state = succesor(expanding)
            if(goal):
                print("answer depth:",len(goal_state[0])-1,"\n")
                print_state(goal_state)
                print("created nodes: ",len(states))
                print("expanded node: ",len(explored))
                break
        else :
            print("there is no answer")
            print("created nodes: ",len(states))
            print("expanded node: ",len(explored))
            break

        

bfs()


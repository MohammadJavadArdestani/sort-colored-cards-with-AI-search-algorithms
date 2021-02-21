import copy


class Card:
    def __init__(self,string):
        
        coler = string[-1]
        string = string[:-1]
        number = int(string)
        self.coler = coler
        self.number = number

    def __str__(self):
        return "{}{}".format(self.number, self.coler)
    
    def __repr__(self):  
        return "{}{}".format (self.number, self.coler)  

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.number == other.number and self.coler == other.coler


all_states = 0
cost = -1
states = []
frontier = []
explored = []


k,m,n = map(int,input().split())


def get_input():
    state = {}
    state[cost] = []
    for x in range(k+1):
        state[x] = [] 
    state[0]=[""]
    for x in range(1,k+1):
        for i in input().split():
            if i == "#":
                state[x].append("#")
            else:
                state[x].append(Card(i)) 
    h = hurstic(state)
    state[cost] =[0,h,h]
    states.append(state)
    frontier.append(state)
    print_state(state)
    return state

def print_state(state):
    for i in state.keys():
        if i ==0 :
            # pass
            print("path is:")
            for i in state[0][1:]:
                print(i)
            print()
        else:       
            for x in state[i]:
                print(x , end = " ")
            print()
    print()


def hurstic(state):
    counter = 0
    for hand in state.keys():
        color_set = set({})
        displacement_counter = 0
        if hand != 0 and hand != cost and state[hand][-1] != '#' : 
            for card_id in  range(len(state[hand])-1):
                    first_card = state[hand][card_id]
                    second_card = state[hand][card_id+1]
                    color_set.add(first_card.coler)
                    if first_card.number < second_card.number :
                        displacement_counter +=1 
            last_Card_inhand = state[hand][-1]
            color_set.add(last_Card_inhand.coler)
            
            # print("coler is {} dis is {} for hand {}".format(len(color_set)-1,displacement_counter,hand) )
        counter += max(len(color_set)-1,displacement_counter)

    return counter



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


def equal_dicts(d1, d2, ignore_keys):
    for k1, v1 in d1.items():
        if k1 not in ignore_keys and (k1 not in d2 or d2[k1] != v1):
            return False
    for k2, v2 in d2.items():
        if k2 not in ignore_keys and k2 not in d1:
            return False
    return True


def move_Card(state,org_hand,des_hand,flag):
    n_state = copy.deepcopy(state)
    if flag:
        n_state[des_hand].pop()
    card = n_state[org_hand].pop()
    if(len(n_state[org_hand]) == 0):
        n_state[org_hand].append('#')
    n_state[des_hand].append(card)
    string = "card '{}' move from hand {} to hand {}".format(card,org_hand,des_hand)
    n_state[0].append(string)
    parrent_real_cost = state[cost][0]
    h = hurstic(n_state)
    n_state[cost] = [parrent_real_cost+1,h,h+parrent_real_cost+1]
    # print("n_stttttttt",n_state)
    global all_states
    for i in states:
        if(equal_dicts(n_state,i,[0,cost])):
            # print("reapeteeeeed n_st", end="")
            # print_state(n_state)
            if n_state[cost][2]<i[cost][2]:
                all_states +=1
                i = n_state 
            return False,0
    # print(" n_st", end="")
    # print_state(n_state)
    all_states +=1
    states.append(n_state)
    frontier.append(n_state)
    if (goal_check(n_state)):
        print("we found goal")
        return True,n_state
    else:
        return False,0
    # print(states)


def succesor(state):
    explored.append(state)
    for org_hand in range(1,k+1):
        try:
            last_card_of_org_hand =state[org_hand][-1]
         
            if last_card_of_org_hand=='#':
                continue

            for des_hand in range(1,k+1):
          
                if des_hand == org_hand : 
                    continue
                last_card_of_des_hand = state[des_hand][-1]
                if last_card_of_des_hand=='#':
                    flag,goal_state=move_Card(state,org_hand,des_hand,1)
                    if(flag): 
                        return True,goal_state
                    continue

                if last_card_of_des_hand.number > last_card_of_org_hand.number:
                    flag,goal_state=move_Card(state,org_hand,des_hand,0)
                    if(flag):
                        return True,goal_state
                
        except:
            pass
    
    return False,0


def bfs():
    get_input()
    # i = 0;
    # exp = 0
    while True:
        # print(len(frontier))
        if frontier:
            minimum = frontier[0][cost][2]
            index = 0
            for i in range(1,len(frontier)) :
                s = frontier[i]
                # print(minimum)
                
                if minimum >= s[cost][2]:
                    # print(s[4])
                    minimum = s[cost][2]
                    index  = i 
            # print("index ",index)
            expanding = frontier.pop(index)
            # explored.append(expanding)
            # depth = len(expanding[0])-1
            # print(depth)
            # print("from: ")
            # print_state(expanding)
            # print("**")
            # exp = exp +1 
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
        # i= i+1
        # print("iteration",i)
        

# bfs()
get_input()

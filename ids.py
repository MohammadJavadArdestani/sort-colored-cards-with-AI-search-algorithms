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


Start_cutoff = 3
cutoff_increment = 9 
states = []
frontier = []
expanded = 0

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
    states.append(n_state)
    frontier.append(n_state)




def succesor(state):
    global expanded
    expanded = expanded + 1
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
                    move_Card(state,org_hand,des_hand,1)
            
                if last_card_of_des_hand.number > last_card_of_org_hand.number:
                    move_Card(state,org_hand,des_hand,0)
        except:
            pass
    # 
    return False

counter_created = 0
counter_expaand = 0


def dls(cutoff,input):
        
    while True:
        # print(len(frontier))
        if frontier:
            expanding = frontier.pop()
            goal = goal_check(expanding)
            if (goal):
                print("answer depth:",len(expanding[0])-1,"\n")
                print_state(expanding)
                print("created nodes: ",len(states))
                print("expanded nodes: ",expanded)
                return True
            if (len(expanding[0]))-1 ==cutoff:
                continue
            else:
                succesor(expanding)
        else :
            print("there is no answer in cutoff ",cutoff)
            print("created nodes: ",len(states))
            print("expanded node: ",expanded)
            return False


def ids():
    input_state =  get_input()
    global states,frontier,expanded, counter_created, counter_expaand

    for i in range(cutoff_increment):
        
        print("\n\nin cutoff:",Start_cutoff+i )
        if(dls(Start_cutoff+i,input_state)):
            counter_created += len(states)
            counter_expaand +=expanded
            break
        else:
         
            counter_created += len(states)
            counter_expaand +=expanded
            print("summed states ",len(states))
            print("created now : ",counter_created)
            print("expand now : ",counter_expaand)
            states = states[:1] 
            frontier = states[:1]
            expanded = 0
    print(counter_created)
    print(counter_expaand)

ids()
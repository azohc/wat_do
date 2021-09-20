#! /bin/python
# kaizen practice proposer
# by azohc juanchozass@gmail.com
# ¿cultivate consitency? ¿¿at what?? let chance decide what you practice next

from random import randint
import time
from timeit import default_timer as timer
from datetime import datetime
import back

debug = False
suspense = True

JOKER_WILDCARD = "do whatever you feel like doing"
MAKE_MUSIC = "make music"
PRAC_DJ = "prac dj"
PRAC_CODE = "code ur projex"
GET_PRESENT = "get present"
GET_LITERATE = "get literate"
CLEAN_ROOM = "clean room"

activities = [JOKER_WILDCARD, MAKE_MUSIC, PRAC_DJ, PRAC_CODE, GET_PRESENT, GET_LITERATE, CLEAN_ROOM]  # nopep8
chances   =  [11,             22,         22,      44,        33,          33,           11        ]  # nopep8

sub_activity_map = {
    MAKE_MUSIC: ['melodics', 'sample', 'trap', 'drill', 'armonica'],
    PRAC_DJ: ['bjios', 'freestyle'],
    PRAC_CODE: ['ux course', 'yalarma', 'wat do: sqlite', 'tomato timers'],
    GET_PRESENT: ['wim hof', 'pranayama', 'guided', 'unguided', 'chikung'],
    GET_LITERATE: ['futureauth', 'journaling', 'history read', 'ebook', 'real book']
}

assert(len(activities) == len(chances))


def debug_print(msg):
    if debug:
        print(msg)

def wait(t):
    if suspense:
        time.sleep(t)

# TODO implement with cyclic array and simulate a wheel spin

def accumulate_chances(chances):
    debug_print(chances[0])
    i = 1
    while(i < len(chances)):
        chances[i] += chances[i-1]
        debug_print(chances[i])
        i += 1


def welcome():
    global now
    now_str = now.strftime("%d/%m/%Y, %H:%M:%S")
    wait(2)
    print(f"\nhello, it is {now_str}")
    wait(1)
    
def add_to_stat_map(activity, map):
    if activity.name not in map:
        map[activity.name] = (activity.duration, 1)
    else:
        map[activity.name] = (map[activity.name][0] + activity.duration, map[activity.name][1] + 1)
    
    if activity.sub_activity != None:
        if activity.sub_activity not in map:
            map[activity.sub_activity] = (activity.duration, 1)
        else:
            map[activity.sub_activity] = (map[activity.sub_activity][0] + activity.duration, map[activity.sub_activity][1] + 1)
        


def print_history_recents():
    print("")
    for days in [1,7, 30]:
        activity_history = back.get_activity_history_in_past_days(days)
        info_str = "past " + (f"{days} days" if days != 1 else "24 hours") + ":"
        
        # gather stats
        activity_time_bout_map = {} # activity name -> (elapsed_time, num_bouts) over days
        for a in activity_history:
            add_to_stat_map(a, activity_time_bout_map)

        if len(activity_time_bout_map) == 0:
            continue

        # build string
        for a in activities:
            if a in activity_time_bout_map:
                info_str += f"\n  {activity_time_bout_map[a][1]}x {a}, total {activity_time_bout_map[a][0]/60} minutes"
                if a in sub_activity_map:
                    for sub_a in sub_activity_map[a]:
                        if sub_a in activity_time_bout_map:
                            info_str += f"\n\t{activity_time_bout_map[sub_a][1]}x {sub_a}, total {activity_time_bout_map[sub_a][0]/60} minutes"
                    
        info_str += "\n"    
                
        print(info_str)


def print_history_totals():
    activity_map = {} # activity name -> list of activity objects
    for act in back.get_all_activities():
        activity_name = act.name
        if not activity_name in activity_map:
            activity_map[activity_name] = list()
        activity_map[activity_name].append(act)

    for activity_name in activities:
        if activity_name in activity_map:
            total_elapsed = 0
            for act in activity_map[activity_name]:
                total_elapsed += act.duration
                num_bouts = len(activity_map[activity_name])
                bouts_str = f"{num_bouts} bout" + ("s" if num_bouts > 1 else "") + " of work"
            print(f"{activity_name}: {bouts_str}, {(total_elapsed/60):.{3}} minutes in total")

    print("\n")


def roll(max = sum(chances)):
    wait(0.5)
    print("rolling in 3...")
    wait(1)
    print("2...")
    wait(1)
    print("1...")
    wait(randint(1, 3))

    print("")
    number = randint(0, max)
    print(f"{number}/{max} is the roll")
    return number

def pick_activity_index(number):
    i = 0
    while(i < len(chances) and number > chances[i]):
        i += 1
    if (i == len(chances)):
        i -= 1
    return i

def do_and_record_activity(activity, sub_activity):
    go_str = f"go {activity}" 
    if sub_activity != None:
        go_str += f", do {sub_activity} this time"
    print(f"{go_str}")
    print("")
    wait(2)
    input("press enter to start the task")
    start = timer()
    wait(2)
    input("\npress enter to confirm the activity has been done\n")
    back.add_activity(activity, sub_activity, timer() - start)

# setup
now = datetime.now()
welcome()
accumulate_chances(chances)
print_history_recents()
# print_history_totals() 


# roll
input("press enter to roll for a task")
number = roll()
activity = activities[pick_activity_index(number)]
sub_activity = None

# check if pick is parent category
if activity in sub_activity_map:
    wait(2)
    print("you got a parent task...")
    wait(1)
    input(f"\npress enter to roll for a subtask")
    number = roll(len(sub_activity_map[activity])-1)
    sub_activity = sub_activity_map[activity][number]
    

do_and_record_activity(activity, sub_activity)

input("enter to exit")
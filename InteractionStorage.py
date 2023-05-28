import numpy as np 
import random as rm
from tqdm import tqdm
from datetime import datetime
import time
import pandas as pd

def current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def random_valandpct(range_list,population_pct,all_lists,p):
    for i,j in tqdm(zip(range_list,population_pct),desc="Making Population"):
        temp_list = list(range(i[0],i[1]))
        all_lists = all_lists + temp_list
        p = p + [j/len(temp_list)]*len(temp_list)
    return all_lists,p

def range_count(range_list,start,end):
    count = 0
    for num in range_list:
        if num >= start and num <= end:
            count += 1
    return count

def make_interactions(society_age_list,ageGroup_list,interactionRange_list,society_interaction_list=[]):
    for i,j in tqdm(enumerate(society_age_list),desc="Individual interaction count"):
        for m,sublist in enumerate(ageGroup_list):
            if j >= sublist[0] and j <= sublist[1]:
                society_interaction_list.append(rm.randint(interactionRange_list[m][0],interactionRange_list[m][1]))
    return society_interaction_list

def append_matrix(x,y,z):
    global matrix
    matrix[x, 0].append(y)
    matrix[x, 1].append(z)
    matrix[y, 0].append(x)
    matrix[y, 1].append(z)

print("\n\t\033[01m\033[34mStarted\n\033[00m")

start_time = current_time()
start = time.time()

population_size = 1000000

#* Age Group = 0-4, 5-19, 20-24, 25-60, 60+
ageGroup_list = [[0,4],[5,19],[20,24],[25,60],[60,100]]

interactionRange_list = [[2,20],[50,135],[35,180],[50,140],[5,35]]

populationPct_list = [0.08,0.28,0.1,0.45,0.09]

interaction_level = [1,4,8]
# interaction_level = [0.96,1.96,2.96]

age_list, agePct_list = random_valandpct(ageGroup_list,populationPct_list,[],[])
# print(f"{age_list=}\n{agePct_list=}")

society_age_list = np.random.choice(age_list, size=population_size, p=agePct_list)
# print(f"{society_age_list=}\n{len(society_age_list)}")
# for i,j in ageGroup_list:print(range_count(society_age_list,i,j))

society_interaction_list = make_interactions(society_age_list,ageGroup_list,interactionRange_list)
# print(f"{society_interaction_list=}\n{len(society_interaction_list)}")

matrix = np.empty((population_size, 6), dtype=object)

virus_spread_rate = 0.0008

for i in tqdm(range(population_size),desc="Empty Matrix"):
    matrix[i, 0] = []
    matrix[i, 1] = []

matrix[:, 2] = np.random.choice(society_interaction_list, size=population_size)
matrix[:, 3] = "N"
matrix[:, 4] = 0
matrix[:, 5] = virus_spread_rate

population_alc_list = list(range(0,population_size))

custom_format = '{l_bar}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
custom_format = "\x1b[34m" + custom_format + "\x1b[0m"
print()

for k in tqdm(range(population_size),desc="Interaction Model",bar_format=custom_format):
    while len(matrix[k, 0]) < matrix[k, 2]:

        relation = rm.choice(population_alc_list)
        # interaction = rm.choices(interaction_level, weights=[0.6,0.3,0.1])[0]
        interaction = rm.choices(interaction_level)[0]

        if relation not in matrix[k, 0] and k not in matrix[relation, 0] and k != relation:

            append_matrix(k,relation,interaction)

        elif all(x in matrix[k, 0] for x in population_alc_list[1:]):

            new_row = np.array([[[], [], 0, "N", 0, virus_spread_rate]], dtype=object)
            matrix = np.append(matrix, new_row, axis=0)

            population_alc_list.append(len(matrix)-1)

            append_matrix(k,len(matrix)-1,interaction)

    population_alc_list.remove(k)

np.save(f"matrix_sr{virus_spread_rate}.npy", matrix)
# print(matrix)
# df = pd.DataFrame(matrix)
# df.to_csv('matrix_data.csv', index=False)

end = time.time()
end_time = current_time()

if end-start >= 3600:
    print(f"\n\t\033[90mStarted at : {start_time}\n\tEnd at : {end_time}\n\n\t\033[36m\033[01mTime taken : {(end-start)/3600} hr\033[00m\n")

elif end-start >= 60:
    print(f"\n\t\033[90mStarted at : {start_time}\n\tEnd at : {end_time}\n\n\t\033[36m\033[01mTime taken : {(end-start)/60} min\033[00m\n")
else:
    print(f"\n\t\033[90mStarted at : {start_time}\n\tEnd at : {end_time}\n\n\t\033[36m\033[01mTime taken : {(end-start)} s\033[00m\n")
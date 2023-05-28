#! in this code the imunity of the person is not defined we are just using the virus spread rate and probability of death and recovery as a parameter.
import pickle
import numpy as np
import random as rm
from tqdm import tqdm
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import time
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def append_data():
    global exposed_data 
    global infected_data 
    global recovered_data
    global dead_data
    global activecases_data
    global not_infected_data

    global total_exposed
    global total_infected
    global total_recovered
    global total_dead
    global ActiveCases
    global not_infected

    exposed_data.append(total_exposed)
    infected_data.append(total_infected)
    recovered_data.append(total_recovered)
    dead_data.append(total_dead)
    activecases_data.append(ActiveCases)
    not_infected_data.append(not_infected)

def check_probability(prob):
    ans = np.random.choice([True,False], size=1, p=[prob,1-prob])
    return ans

def spread_virus(neighbour_nodes,interaction_intensity,node):
    global virus_spread_rate
    global interaction_model
    global total_exposed
    global ActiveCases
    global not_infected
    global num
    for neb, ints in zip(neighbour_nodes,interaction_intensity):
        num += 1
        if interaction_model[neb][3] == 'N' and check_probability(interaction_model[node][5]*ints):
            interaction_model[neb][3] = 'E'
            total_exposed += 1
            ActiveCases += 1
            not_infected -= 1

def dead():
    return np.random.choice([True,False], size=1, p=[0.1,0.9])

def jabbed():
    return np.random.choice([True,False], size=1, p=[0.2,0.8])

isRunning = True
runtime = 0
num = 0

while(isRunning):

    exposed_data, infected_data, recovered_data, dead_data ,activecases_data, not_infected_data = [],[],[],[],[],[]
    total_exposed, total_infected, total_recovered, total_dead, ActiveCases, not_infected = 0,0,0,0,0,0

    print(f"\n\tStarted {runtime}\n")
    im = "matrix_sr0.0008"
    interaction_model = np.load(f'{im}.npy', allow_pickle=True)

    total_popultion = len(interaction_model)
    not_infected = total_popultion

    virus_spread_rate = interaction_model[0][5]

    os.mkdir(f"{runtime}_New_IM_vsr_{virus_spread_rate}__im_{im}__{timestamp}")
    print("Folder is Created")
    # time.sleep(5)
    file = open(f"{runtime}_New_IM_vsr_{virus_spread_rate}__im_{im}__{timestamp}/log.txt", 'w')
    file.write("interactionRange_list = [[2,20],[50,135],[35,180],[50,140],[5,35]]\n")
    for i,j in tqdm(enumerate(interaction_model)):
        interaction_model[i][5] = virus_spread_rate

    jabbed_persons = len(np.where(interaction_model[:, 5] == 0.005)[0])
    not_jabbed_persons = len(np.where(interaction_model[:, 5] == virus_spread_rate)[0])

    file.write(f"Total Population : {len(interaction_model)}\n")
    file.write(f"{jabbed_persons=} || {not_jabbed_persons=}\n")

    # print(interaction_model)

    interaction_model[rm.randint(0,len(interaction_model)-1),3] = "E"
    total_exposed += 1
    ActiveCases += 1

    exposed_persons = np.where(interaction_model[:, 3] == "E")

    inLoop = True
    day = 0
    while inLoop:
        print(f"{day} : {ActiveCases=}")
        file.write(f"Day {day} || Active Cases : {ActiveCases} || Exposed : {total_exposed}   Infected : {total_infected}   Recovered : {total_recovered}   Dead : {total_dead}\n")
        append_data()
        day += 1
        for i,j in enumerate(exposed_persons[0]):
            nodeDay = interaction_model[j][4]
            nodeDay += 1
            interaction_model[j][4] = nodeDay

            if nodeDay <= 3:
                spread_virus(interaction_model[j][0],interaction_model[j][1],j)

            elif nodeDay > 3 and interaction_model[j][3] == 'E':
                interaction_model[j][3] = 'I'
                total_infected += 1

        exposed_persons = np.where(interaction_model[:, 3] == "E")
        infected_persons = np.where(interaction_model[:, 3] == "I")

        for m,n in enumerate(infected_persons[0]):
            nodeDay = interaction_model[n][4]
            nodeDay += 1
            interaction_model[n][4] = nodeDay
            
            if nodeDay >= 14:
                if dead():
                    interaction_model[n][3] = 'D'
                    total_dead += 1
                    ActiveCases -= 1
                else:
                    interaction_model[n][3] = 'R'
                    total_recovered += 1
                    ActiveCases -= 1
                
        if ActiveCases == 0: inLoop = False

    runtime += 1

    if day > 100:
      print(f"\n\t\033[01m\033[34mTotal Loop : {num}\n\033[00m")
      fig = make_subplots(rows=5, cols=1)

      numOfDays = list(range(0,len(activecases_data)))

      day_cases = []

      for i,j in enumerate(activecases_data):
          if i > 0:
              day_cases.append(j-activecases_data[i-1])
          elif i == 0:
              day_cases.append(1)

      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=activecases_data,
          mode='lines',
          name='Active Cases'
      ), row=1,col=1)
      fig.append_trace(go.Bar(
          x=numOfDays,
          y=day_cases,
          name='Per-day'
      ), row=2, col=1)
      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=recovered_data,
          mode='lines',
          name='Recovered',
      ), row=3, col=1)
      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=dead_data,
          mode='lines',
          name='Dead',
          marker=dict(color='red')
      ), row=3, col=1)
      fig.append_trace(go.Bar(
          x=["Recovered","Dead"],
          y=[total_recovered,total_dead],
          name='Recovered and Dead'
      )
      , row=4, col=1)
      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=infected_data,
          mode='lines',
          name='Infected',
      ), row=5, col=1)
      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=exposed_data,
          mode='lines',
          name='Exposed',
      ), row=5, col=1)
      fig.append_trace(go.Scatter(
          x=numOfDays,
          y=not_infected_data,
          mode='lines',
          name='Normal',
      ), row=5, col=1)


      fig.update_layout(height=4000)

      fig.show()


      print(f"{jabbed_persons=} || {not_jabbed_persons=}")
      print(f"NOT infected persons : {len(np.where(interaction_model[:, 3] == 'E')[0])}")

      file.write(f"\n\n")
      file.write(f"-----Data-----\n")
      file.write(f"Exposed : {total_exposed}\n")
      file.write(f"Infected : {total_infected}\n")
      file.write(f"Recovered :{total_recovered}\n")
      file.write(f"Dead : {total_dead}\n\n")
      file.write(f"\nExposed : \n{exposed_data}\n")
      file.write(f"\nInfected : \n{infected_data}\n")
      file.write(f"\nRecovered :\n{recovered_data}\n")
      file.write(f"\nDead : \n{dead_data}\n")
      file.write(f"\nActiveCases : \n{activecases_data}\n")
    #   fig.update_layout(width=1500)
    #   fig.write_image(f"{runtime}_New_IM_vsr_{virus_spread_rate}__im_{im}__{timestamp}/plots.svg")
    #   fig.write_image(f"{runtime}_New_IM_vsr_{virus_spread_rate}__im_{im}__{timestamp}/plots.png")
      file.close()
      isRunning = False

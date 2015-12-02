# -*- coding: utf-8 -*-
"""
Fantasy Football Simulations

Created on Tue Dec 01 10:20:50 2015

@author: gnl626
"""

import numpy as np
import random as ran

# Array in alphabetical order
# Updated to include week 12 results
DEXT = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0] # 9-3
JACK = [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1] # 5-7
KATR = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0] # 5-7
MAXM = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] # 2-10 LOL
TOLH = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0] # 6-6
TRIG = [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1] # 9-3

# Dictionary for function
team = {"DEXT": 0, "JACK": 1, "KATR": 2, "MAXM": 3, "TOLH": 4, "TRIG":5}

Comb_score_array = np.row_stack((DEXT, JACK, KATR, MAXM, TOLH, TRIG))

act_wins = []
for row in range(6):
    act_wins.append(sum(Comb_score_array[row,]))
act_wins = np.array(act_wins)

# Define a function to simulate a game of fantasy football
def simulate_game(team1, team2, team1_prob = 0.5):
    num = ran.random()
    if num > team1_prob:
        return team1
    else:
        return team2

playoff_totals = zeros(6)
for n in range(10000):    
    additional_wins = np.zeros(6 ,dtype = np.int)
    # Week 13 Games
    winner = simulate_game("DEXT", "TRIG")
    additional_wins[team[winner]] += 1
    winner = simulate_game("KATR", "JACK")
    additional_wins[team[winner]] += 1
    winner = simulate_game("MAXM", "TOLH")
    additional_wins[team[winner]] += 1
    
    # Week 14 Games
    winner = simulate_game("DEXT", "TOLH")
    additional_wins[team[winner]] += 1
    winner = simulate_game("MAXM", "JACK")
    additional_wins[team[winner]] += 1
    winner = simulate_game("TRIG", "KATR")
    additional_wins[team[winner]] += 1
    
    # Week 15 Games
    winner = simulate_game("DEXT", "MAXM")
    additional_wins[team[winner]] += 1
    winner = simulate_game("KATR", "JACK")
    additional_wins[team[winner]] += 1
    winner = simulate_game("TRIG", "TOLH")
    additional_wins[team[winner]] += 1
    
    # Add the additional wins to the existing wins
    win_vec = act_wins + additional_wins
    
    # Find top three teams
    playoff = zeros(6)
    # Winner of the West
    if win_vec[0] > win_vec[2] and win_vec[0] > win_vec[1]:
        playoff[0] += 1
    elif win_vec[2] > win_vec[1] and win_vec[2] > win_vec[0]:
        playoff[2] += 1
    elif win_vec[1] > win_vec[2] and win_vec[1] > win_vec[0]:
        playoff[1] += 1
     
    
    # Winner of the East
    if win_vec[3] > win_vec[4] and win_vec[3] > win_vec[5]:
        playoff[3] += 1
    elif win_vec[4] > win_vec[5] and win_vec[4] > win_vec[3]:
        playoff[4] += 1
    elif win_vec[5] > win_vec[4] and win_vec[5] > win_vec[3]:
        playoff[5] += 1
    
        
    # At large winner
    at_large_vec = win_vec * (1 - playoff)
    for i in range(6):
        if at_large_vec[i] == max(at_large_vec):
            playoff[i] += 1
            break
    
    playoff_totals += playoff

playoff_prob = playoff_totals/100
import player
from random import uniform, random, randint
from datetime import datetime, timedelta

TURNOVERS = ['pass stolen by', 'drive stripped by', '3 pointer blocked by', \
    'mid-range jumpshot blocked by', 'inside shot blocked by''drive blocked by']
MISSED_SHOTS = ['Layup missed by', 'Dunk missed by', 'Inside shot missed by', \
                'Mid-range jumper missed by', '3 pointer missed by']

def game(t1, t2, pbp=False):
    quarters_played = 0
    t1.points = 0
    t1.possesions = 0
    t1.away = True
    t2.points = 0
    t2.possesions = 0
    t2.home = True

    # Opening tip
    rand_jumpball = random()
    if pbp: print ('FIRST QUARTER')
    if pbp: print ('')
    # Reset all players energy to 100
    for p in (t1.players + t2.players):
        p.energy = 100
    if rand_jumpball < 0.5:
        if pbp: print ('%s won jump ball') % t1.name
        turn = 0
    else:
        if pbp: print ('%s won jump ball') % t2.name
        turn = 1
    q1 = quarter(t1, t2, turn, pbp=pbp)

    # Team who looses tip gets possesion to start 2nd and 3rd
    if turn == 0:
        if pbp: print ('')
        if pbp: print ('SECOND QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        q2 = quarter(t1, t2, 1, pbp=pbp)
        if pbp: print ('')
        if pbp: print ('THIRD QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        # Reset all players energy to 100
        for p in (t1.players + t2.players):
            p.energy = 100
        q3 = quarter(t1, t2, 1, pbp=pbp)
        if pbp: print ('')
        if pbp: print ('FOURTH QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        q4 = quarter(t1, t2, 0, pbp=pbp)
    else:
        if pbp: print ('')
        if pbp: print ('SECOND QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        q2 = quarter(t1, t2, 0, pbp=pbp)
        if pbp: print ('')
        if pbp: print ('THIRD QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        q3 = quarter(t1, t2, 0, pbp=pbp)
        if pbp: print ('')
        if pbp: print ('FOURTH QUARTER')
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        # All players gain 10 energy
        for p in (t1.players + t2.players):
            p.energy += 10
        q4 = quarter(t1, t2, 1, pbp=pbp)

    quarters_played = 4
    # If score tied after 4 quarters, start each overtime with jump ball
    while t1.points == t2.points:
        if pbp: print ('')
        if pbp: print ('OVERTIME %s') % (quarters_played - 3)
        if pbp: print ('%s: %s') % (t1.name, t1.points)
        if pbp: print ('%s: %s') % (t2.name, t2.points)
        if pbp: print ('')
        rand_jumpball = random()
        if rand_jumpball < 0.5:
            turn = 0
        else:
            turn = 1
        ot = quarter(t1, t2, turn, ot=True, pbp=pbp)
        quarters_played += 1

    if t1.points > t2.points:
        t1.wins += 1
        t2.losses += 1
    else:
        t1.losses += 1
        t2.wins += 1
    t1.season_points += t1.points
    t2.season_points += t2.points

    return quarters_played


def quarter(t1, t2, turn, ot=False, pbp=False):
    # Initiate game clock to 12:00 for each quarter (5:00 for OT). After each
    # possesion subtract the time used for that possession until no time left
    if ot:
        game_clock = timedelta(minutes = 5)
    else:
        game_clock = timedelta(minutes = 12)

    # Alternate possesions between teams
    while game_clock > timedelta(0):
        orig_game_clock = game_clock
        if turn % 2 == 0:
            points, possesion_time, reb, result = possesion(t1, t2, \
                                                            game_clock, pbp=pbp)
            t1.points += points
            t1.possesions += 1
        else:
            points, possesion_time, reb, result = possesion(t2, t1, \
                                                            game_clock, pbp=pbp)
            t2.points += points
            t2.possesions += 1
        diff = timedelta(seconds = possesion_time)
        game_clock -= diff

        if game_clock < timedelta(0):
            game_clock = timedelta(0)

        for p in t1.on_floor + t2.on_floor:
            p.time_played += (orig_game_clock - game_clock)

        if reb != None:
            if reb[0] != 'off_rebound':
                if reb[0] == 'def_rebound':
                    result += ', rebound by %s' % reb[1].name
                turn += 1
            else:
                result += ', offesive rebound by %s' % reb[1].name
        else:
            turn += 1

        if pbp: print ('%s  -  %s-%s  -  %s') % (orig_game_clock, t1.points, \
                                               t2.points, result)


def possesion(team, deff_team, game_clock=timedelta(minutes = 12), pbp=False):
    # If less than 24 seconds left in quarter, 'turn off the shot clock'
    if game_clock < timedelta(seconds = 24):
        shot_clock = game_clock.seconds
    else:
        shot_clock = 24

    # Wait 3-6 seconds before initiating a play
    wait_time = randint(3, 6)
    shot_clock -= wait_time

    # PG carries ball past half most times, else SG or SF
    random_cross_half = uniform(0, 100)

    if random_cross_half < 55:
        current_player = team.on_floor[0]
    elif random_cross_half < 80:
        current_player = team.on_floor[1]
    else:
        current_player = team.on_floor[2]

    points, passed_to, off, shot_clock, \
    ass, result, to = play(current_player, deff_team,
                           shot_clock=shot_clock, pbp=pbp, first=True)

    next_player = current_player
    # If player is an exceptional passer ( > 70 ) then give slight boost to the
    # next player's chances if they choose to shoot. Do not penalize bad passers
    # as they are already more likely to turn over the ball
    while shot_clock > 0 and passed_to != None and not to:
        try:
            current_player = off
            open_factor = (100 + current_player.skills['passing'] - 70) / \
                           float(100)
            open_factor = max(1, open_factor)
            next_player = team.on_floor[passed_to]
        except TypeError:
            pass
        points, passed_to, off, \
        shot_clock, ass, result, to = play(team.on_floor[passed_to], \
                                  deff_team, shot_clock=shot_clock, pbp=pbp, \
                                  open_factor=open_factor)

    if points > 0 and current_player != next_player and ass:
        current_player.assists += 1
        result += ', assisted by %s' % current_player.name

    time_used = min(game_clock.seconds, 24) - shot_clock

    reb = None
    for m in MISSED_SHOTS:
        if m in result:
            reb = rebound(team, deff_team)

    update_fatigue(team, deff_team, time_used)
    sub_players(team, deff_team, pbp)

    return points, time_used, reb, result

def play(off, deff, shot_clock=24, pbp=False, first=False, open_factor=1):
    points = 0
    passed_to = None
    result = None

    # Hold ball while making a decision for a period of time depending on clock
    if shot_clock > 12:
        decision_time = randint(1, 6)
    elif shot_clock > 5:
        decision_time = randint(1, 4)
    else:
        decision_time = 0
    shot_clock -= decision_time

    # Decide whether to shoot or pass, always shooting if less than 5 secs left.
    # Players get more likely to shoot as shot clock gets lower. If decision
    # time greater than 4 secs, any basket will be unassisted. If first play
    # of the possesion, more likely to pass to prevent PG's from shooting
    # too often
    assisted = True
    if decision_time > 4:
        assisted = False
    random_sp = random()
    if first:
        urgent = 1
    else:
        urgent = 1 - (24 - shot_clock)/float(25)
    if random_sp < ((off.o_tendencies['shoot_pass'] - 50)/float(300) + urgent) \
    and shot_clock > 5:
        passed_to, result = attempt_pass(off, deff)
        off.passes += 1
    else:
        random_dj = uniform(0, 100)
        if random_dj < off.o_tendencies['drive_jumper']:
            points, result = attempt_jumper(off, deff, open_factor)
        else:
            points, result = attempt_drive(off, deff, open_factor)
    off.points += points

    to = False
    for t in TURNOVERS:
        if t in result:
            to = True
    return points, passed_to, off, shot_clock, assisted, result, to

def attempt_jumper(off, deff, open_factor):
    points = 0
    random_range = uniform(0, 100)
    defender = deff.on_floor[off.position - 1]
    def_block_chance = defender.block_chance
    rand_block = random()

    if random_range < off.shooting_range['close']:
        off.fg2a += 1
        if rand_block < def_block_chance*0.5:
            defender.blocks += 1
            return points, '%s inside shot blocked by %s' \
                            % (off.name, defender.name)
        random_close = random()
        if random_close < max(0.0035, 0.006*off.shooting['close'])*open_factor:
            off.fg2m += 1
            points += 2
            result = '%s made inside shot' % off.name
        else:
            result = 'Inside shot missed by %s' % off.name
    elif random_range < off.shooting_range['mid']:
        off.fg2a += 1
        if rand_block < def_block_chance*0.2:
            defender.blocks += 1
            return points, '%s mid-range jumpshot blocked by %s' \
                            % (off.name, defender.name)
        random_close = random()
        if random_close < max(0.0025, 0.0055*off.shooting['mid'])*open_factor:
            off.fg2m += 1
            points += 2
            result = '%s made mid-range jumpshot' % off.name
        else:
            result = 'Mid-range jumpshot missed by %s' % off.name
    else:
        off.fg3a += 1
        if rand_block < def_block_chance*0.1:
            defender.blocks += 1
            return points, '%s 3 pointer blocked by %s' \
                            % (off.name, defender.name)
        random_close = random()
        if random_close < max(0.0015, 0.0048*off.shooting['long'])*open_factor:
            off.fg3m += 1
            points += 3
            result = '%s made 3 pointer' % off.name
        else:
            result = '3 pointer missed by %s' % off.name

    return points, result

def attempt_drive(off, deff, open_factor):
    points = 0

    # First calculate whether player is stripped of the ball by their defender
    defender = deff.on_floor[off.position - 1]
    protect_ball = 0.92 + (off.protect_drive - defender.steal_pass) / 20
    if protect_ball > 0.97:
        protect_ball = 0.97
    elif protect_ball < 0.87:
        protect_ball = 0.87
    rand_protect = random()
    if rand_protect > protect_ball:
        defender.steals += 1
        off.turnovers += 1
        return points, '%s drive stripped by %s' % (off.name, defender.name)

    # Decide whether attempting a layup or a dunk. Then combine attributes of
    # player's man defender, plus the two post defenders to calculate whether
    # the dunk or layup is blocked
    def_block_chance = defender.block_chance
    pf_block_chance = deff.on_floor[3].block_chance
    c_block_chance = deff.on_floor[4].block_chance

    rand_block_player = random()
    if off.position == 5:
        total_block_chance = 0.70*def_block_chance + 0.30*pf_block_chance
        if rand_block_player < 0.70:
            block_player = defender
        else:
            block_player = deff.on_floor[3]
    elif off.position == 4:
        total_block_chance = 0.60*def_block_chance + 0.40*c_block_chance
        if rand_block_player < 0.60:
            block_player = defender
        else:
            block_player = deff.on_floor[4]
    else:
        total_block_chance = 0.30*def_block_chance + 0.30*pf_block_chance \
                           + 0.40*c_block_chance
        if rand_block_player < 0.40:
            block_player = defender
        elif rand_block_player < 0.60:
            block_player = deff.on_floor[3]
        else:
            block_player = deff.on_floor[4]

    random_drive = uniform(0, 100)
    if random_drive < off.o_tendencies['layup_dunk']:
        off.fg2a += 1
        random_block = random()
        if random_block < total_block_chance:
            block_player.blocks += 1
            return points, '%s layup blocked by %s' \
                            % (off.name, block_player.name)
        random_layup = random()
        if random_layup < max(0.0045, 0.0065*off.driving['layups'])*open_factor:
            off.fg2m += 1
            points += 2
            result = 'Layup made by %s' % off.name
        else:
            result = 'Layup missed by %s' % off.name
    else:
        off.fg2a += 1
        random_block = random()
        if random_block < 0.5*total_block_chance:
            block_player.blocks += 1
            return points, '%s dunk blocked by %s' \
                            % (off.name, block_player.name)
        random_dunk = random()
        if random_dunk < max(0.004, 0.0080*off.driving['dunking'])*open_factor:
            off.fg2m += 1
            points += 2
            result = 'Dunk made by %s' % off.name
        else:
            result = 'Dunk missed by %s' % off.name

    return points, result

def attempt_pass(off, deff):
    # Decide which teammate to attempt a pass to
    rand_pass = uniform(0, 100)
    total = 0

    for p in range(5):
        total += off.passing_choice[p]
        if rand_pass < total and p != off.position -1:
            pass_to = p
            break

    # Give player defending the intended target a 5-25% chance of stealing the
    # pass, depending on attributes
    guarding_pass = deff.on_floor[pass_to ]
    make_pass = 0.96 + (off.complete_pass - guarding_pass.steal_pass) / 50
    if make_pass > 0.98:
        make_pass = 0.98
    elif make_pass < 0.94:
        make_pass = 0.94
    rand_steal = random()
    if rand_steal < make_pass:
        return pass_to, 'made_pass'
    else:
        guarding_pass.steals += 1
        off.turnovers += 1
        return pass_to, '%s pass stolen by %s' % (off.name, guarding_pass.name)

def rebound(off, deff):
    # If attributes are equal, def team will get the rebound ~75% of the time
    deff_rebound_chance = 3*deff.team_rebound_chance()
    off_rebound_chance = off.team_rebound_chance()
    total = deff_rebound_chance + off_rebound_chance
    deff_rebound_chance = deff_rebound_chance / total
    off_rebound_chance = off_rebound_chance / total

    rand_reb_team = random()
    rand_reb_player = random()
    if rand_reb_team < deff_rebound_chance:
        reb_player = deff.player_rebound_chance(rand_reb_player)
        reb_player.def_rebounds += 1
        reb_player.rebounds += 1
        return ['def_rebound', reb_player]
    else:
        reb_player = off.player_rebound_chance(rand_reb_player)
        reb_player.off_rebounds += 1
        reb_player.rebounds += 1
        return ['off_rebound', reb_player]

def update_fatigue(off, deff, time_used):
    # For players on the court decrease energy, resting players increase
    for team in [off, deff]:
        for p in team.on_floor:
            tire_factor = (110 - p.skills['stamina']) / float(275)
            tire_factor = uniform(0.75*tire_factor, 1.25*tire_factor)
            p.energy = max(0, p.energy - time_used * tire_factor)
        for p in team.on_bench:
            rest_factor = 0.25
            p.energy = min(100, p.energy + time_used * rest_factor)

def sub_players(off, deff, pbp=False):
    for team in [off, deff]:
        for p in team.on_floor:
            slot = p.position - 1
            if p in team.starters:
                if p.energy < 30:
                    for b in team.on_bench:
                        if b.position == p.position and b.energy > 95:
                            team.on_floor[slot] = b
                            team.on_bench[slot] = p
                            if pbp: print ('%s subbed out for %s') % (p.name, b.name)
                            break
            else:
                if p.energy < 55:
                    for b in team.on_bench:
                        if b.position == p.position and b.energy > 95:
                            team.on_floor[slot] = b
                            team.on_bench[slot] = p
                            if pbp: print ('%s subbed out for %s') % (p.name, b.name)
                            break

import toks
import random
from datetime import timedelta

POSITIONS = {1: 'PG', 2: 'SG', 3: 'SF', 4: 'PF', 5: 'C'}

class Player():
    name = ''
    position = 0

    # Player skills
    shooting = {'close': 0, 'mid': 0, 'long': 0, 'ft': 0}
    driving = {'layups': 0, 'dunking': 0}
    skills = {'speed': 0, 'dribbling': 0, 'passing': 0, 'stamina': 0}
    defense = {'rebounding': 0, 'defense': 0, 'blocking': 0, 'stealing': 0}

    # Player tendencies
    o_tendencies = {'shoot_pass': 0, 'drive_jumper': 0, 'layup_dunk': 0}
    d_tendencies = {'go_for_steal': 0, 'go_for_block': 0}
    shooting_range = {'close': 0, 'mid': 0, 'long': 0}
    passing_choice = [0, 0, 0, 0, 0]

    # Player offensive chance rolls
    complete_pass = 0
    protect_drive = 0

    # Player defensive chance rolls
    steal_pass = 0
    steal_drive = 0
    block_chance = 0

    # Player stats
    energy = 100
    games = 0
    fga = 0
    fg2a = 0
    fg3a = 0
    fta = 0
    fgm = 0
    fg2m = 0
    fg3m = 0
    ftm = 0
    points = 0
    assists = 0
    rebounds = 0
    def_rebounds = 0
    off_rebounds = 0
    turnovers = 0
    steals = 0
    blocks = 0
    passes = 0
    time_played = timedelta(0)

    def __init__(self, name, position, floor=50, ceiling=100):
        self.name = name
        self.position = position
        self.position_string = POSITIONS[position]

        skills_array = randomize_skills(floor, ceiling)
        self.shooting = skills_array[0]
        self.driving = skills_array[1]
        self.skills = skills_array[2]
        self.defense = skills_array[3]

        tendencies_array = randomize_tendencies(position)
        self.o_tendencies = tendencies_array[0]
        self.d_tendencies = tendencies_array[1]
        self.shooting_range = tendencies_array[2]
        self.passing_choice = tendencies_array[3]

        self.complete_pass = self.skills['passing'] / float(100)
        self.protect_drive = (0.60 * self.skills['dribbling'] + \
                              0.40 * self.skills['speed']) / float(100)

        self.steal_drive = (0.40 * self.defense['defense'] + \
                            0.30 * self.skills['speed'] + \
                            0.30 * self.defense['stealing']) / float(100)
        self.steal_pass = (0.25 * self.defense['defense'] + \
                           0.35 * self.skills['speed'] + \
                           0.40 * self.defense['stealing']) / float(100)
        self.block_chance = (0.80 * self.defense['blocking'] + \
                           0.40 * self.defense['defense']) / float(750)


    def print_player(self):
        print self.name
        print self.position_string
        print self.shooting
        print self.driving
        print self.defense
        print self.skills
        print self.o_tendencies
        print self.d_tendencies
        print self.shooting_range
        print self.passing_choice

def randomize_skills(floor=50, ceiling=100):
    shooting = {}
    driving = {}
    skills = {}
    defense = {}

    for key in toks.DEF_SHOOTING:
        shooting[key] = random.randint(floor, ceiling)
    for key in toks.DEF_DRIVING:
        driving[key] = random.randint(floor, ceiling)
    for key in toks.DEF_SKILLS:
        skills[key] = random.randint(floor, ceiling)
    for key in toks.DEF_DEFENSE:
        defense[key] = random.randint(floor, ceiling)

    return shooting, driving, skills, defense

def randomize_tendencies(position):
    o_tendencies = {}
    d_tendencies = {}
    shooting_range = {}

    for key in toks.DEF_OFFENSIVE:
        o_tendencies[key] = random.randint(40, 60)
    for key in toks.DEF_DEFENSIVE:
        d_tendencies[key] = random.randint(40, 60)

    total = 0
    shot_range = []
    for i in range(3):
        value = random.randint(20, 80)
        total += value
        shot_range.append(value)
    shooting_range['close'] = 100*float(shot_range[0]) / total
    shooting_range['mid'] = 100*float(shot_range[1]) / total
    shooting_range['long'] = 100*float(shot_range[2]) / total

    total = 0
    passing_choice = []
    for i in range(5):
        if i == position - 1:
            value = 0
        else:
            value = random.randint(20, 80)
            total += value
        passing_choice.append(value)
    for i in range(5):
        if i != position - 1:
            passing_choice[i] = 100*float(passing_choice[i]) / total

    return o_tendencies, d_tendencies, shooting_range, passing_choice       

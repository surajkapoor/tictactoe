from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
import os
import pdb
from random import randrange
from collections import Counter

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def tictac():
	return render_template("tictac.html")

def setup_analyze(MOVES):
	s = MOVES["SETUP"]
	setup = []
	for sets in s:
		i = 0
		while i < 3:
			if sets[i] == None:
				setup.append(sets[-1][i])
			i += 1
	return setup

def options_analyze(MOVES):
	o = MOVES["OPTIONS"]
	options = []
	for sets in o:
		i = 0
		while i < 3:
			if sets[i] == None:
				options.append(sets[-1][i])
			i += 1	
	return options						

def optimal_spot(MOVES):
	optimal = None, None
	for each in options_analyze(MOVES):
		s = setup_analyze(MOVES).count(each)
		print each, s
		if s > optimal[1]:
			optimal = each, s
	return optimal[0]		

def filter_setup(MOVES):
	c = Counter(setup_analyze(MOVES))
	largest = None, None
	for each in c:
		if c[each] > largest[0]:
			largest = each, c[each]
	return largest[0]	

def analyze(MOVES, state):
	#picks best move from dictionary
	if "KILL" in MOVES:
		kill = MOVES["KILL"].index(None)
		n = MOVES["KILL"][3][kill]
		state[n] = "O"
		state.append(("COMPUTER WINS", MOVES["KILL"][3]))
	elif "KILL" not in MOVES and "BLOCK" in MOVES:
		block = MOVES["BLOCK"].index(None)
		n = MOVES["BLOCK"][3][block]
		state[n] = "O"
	elif "SETUP" in MOVES and "OPTIONS" in MOVES and "KILL" not in MOVES and "BLOCK" not in MOVES:
		n = optimal_spot(MOVES)
		state[n] = "O"
	elif "SETUP" in MOVES and "OPTIONS" not in MOVES and "KILL" not in MOVES and "BLOCK" not in MOVES:
		n = filter_setup(MOVES)
		state[n] = "O"	
	else:
		print MOVES, state
	print MOVES, state	
	return state	
			
def move(state):
	#analyzes all possible winning combinations and creates a dictionary of next moves
	MOVES = {}
	top_horiz = [state[0], state[1], state[2], (0,1,2)]
	middle_horiz = [state[3], state[4], state[5], (3,4,5)]
	bottom_horiz = [state[6], state[7], state[8], (6,7,8)]
	left_vertical = [state[0], state[3], state[6], (0,3,6)]
	middle_vertical = [state[1], state[4], state[7], (1,4,7)]
	right_vertical = [state[2], state[5], state[8], (2,5,8)]
	diag_bleft_tright = [state[6], state[4], state[2], (6,4,2)]
	diag_tleft_bright = [state[0], state[4], state[8], (0,4,8)]
	options = [top_horiz, middle_horiz, bottom_horiz, left_vertical, middle_vertical, right_vertical, diag_tleft_bright, diag_bleft_tright]
	for each in options:
		o = each.count("O")
		x = each.count("X")
		n = each.count(None)
		if x == 3:
			state.append(("YOU WIN", each[3]))
			return state
		elif o == 2 and n == 1:
			MOVES["KILL"] = each
		elif x == 2 and n == 1:
			MOVES["BLOCK"] = each
		elif o == 1 and n == 2 and "OPTIONS" not in MOVES:
			MOVES["OPTIONS"] = [each]
		elif o == 1 and n == 2 and "OPTIONS" in MOVES:
			MOVES["OPTIONS"].append(each)
		elif x == 1 and n == 2 and "SETUP" not in MOVES:
			MOVES["SETUP"] = [each]
		elif x == 1 and n == 2 and "SETUP" in MOVES:
			MOVES["SETUP"].append(each)	
		'''	
		elif x == 1 and o == 1 and n == 1 and "NEUTRAL" not in MOVES:
			MOVES["NEUTRAL"] = [each]
		elif x == 1 and o == 1 and n == 1 and "NEUTRAL" in MOVES:
			MOVES["NEUTRAL"].append(each)		
		'''	
	return analyze(MOVES, state)		

def first_move(state):
	place = state.index("X")
	new_spot = None
	while True:
		new_spot = randrange(9)
		if new_spot != place:
			break				
	state[new_spot] = "O"
	return state
	
@app.route('/score')
def score():
	top_left = request.args.get("top_left", "top_left", type=str)
	top_middle = request.args.get("top_middle", "top_middle", type=str)
	top_right = request.args.get("top_right", "top_right", type=str)
	middle_left = request.args.get("middle_left", "middle_left", type=str)
	middle_middle = request.args.get("middle_middle", "middle_middle", type=str)
	middle_right = request.args.get("middle_right", "middle_right", type=str)
	bottom_left = request.args.get("bottom_left", "bottom_left", type=str)
	bottom_middle = request.args.get("bottom_middle", "bottom_middle", type=str)
	bottom_right = request.args.get("bottom_right", "bottom_right", type=str)
	result = [top_left, top_middle, top_right, middle_left, middle_middle, middle_right, bottom_left, bottom_middle, bottom_right]
	result = [None if i == "" else i for i in result]
	if result.count("X") == 1:
		first_move(result)
	else:
		move(result)
	return jsonify(result = result)

if __name__ == "__main__":
	app.debug = True
	app.run()    
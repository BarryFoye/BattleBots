"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from FlaskServer import app
from GeneticAlgorithm import GeneticAlgorithm as ga
import json
genetic_algs = []

#@app.route('/')
#@app.route('/home')
#def home():
#    """Renders the home page."""
#    return render_template(
#        'index.html',
#        title='Home Page',
#        year=datetime.now().year,
#    )

@app.route('/generate_random_generation', methods=['POST'])
def get_generation():
    """Gets a random generation from the selected GA"""
    ga_id = int(request.args['ga_id'])
    genetic_algs[ga_id].GenerateRandomGeneration()
    return json.dumps(genetic_algs[ga_id].current_generation)

@app.route('/init_ga', methods=['POST'])
def init_ga():
    """sets up a new GA and returns the id of that GA for the client
     takes in a comma-delimited string of genome_length,generation_size,mutation_percent"""
    genome_length = request.args['genome_length']
    generation_size = request.args['generation_size']
    mutation_percent = request.args['mutation_percent']
    new_ga = ga(genome_length,2,generation_size,mutation_percent)
    genetic_algs.append(new_ga)
    return str(len(genetic_algs))

@app.route('/record_candidate_score', methods=['POST'])
def record_candidate_score():
    """records the score of a candidate"""
    ga_id = request.args['ga_id']
    candidate_id = request.args['candidate_id']
    score = request.args['score']
    genetic_algs[ga_id].RecordCandidateScore(candidate_id,score)
    return str(0)

@app.route('/get_next_generation', methods=['POST'])
def get_next_generation():
    """once all candidates have been scored this method runs the roulette wheel
    and the mutation and then gives you a new generation"""
    ga_id = request.args['ga_id']
    genetic_algs[ga_id].GetNextGeneration()
    return json.dumps(genetic_algs[ga_id].current_generation)
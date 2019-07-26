"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from FlaskServer import app
from GeneticAlgorithm import GeneticAlgorithm as ga
from bson.objectid import ObjectId
import json
#import pymongo
from pymongo import MongoClient


genetic_alg = []
ThisMongoCollectionObject = [ ]

@app.route('/init_ga', methods=['POST'])
def init_ga():
    GetMongoCollection()
    """sets up a new GA and returns the id of that GA for the client
     takes in a comma-delimited string of genome_length,generation_size,mutation_percent"""
    genome_length = int(request.args['genome_length'])
    generation_size = int(request.args['generation_size'])
    mutation_percent = int(request.args['mutation_percent'])
    num_possible_options = int(request.args['num_possible_options'])
    ga_id = ga.new_ga(genome_length,2,generation_size,mutation_percent,ThisMongoCollectionObject[0])
    return str(ga_id)

@app.route('/generate_random_generation', methods=['POST'])
def get_rnd_generation():
    """Gets a random generation from the selected GA. Wipes all other generations, effectively starts from scratch"""
    GetMongoCollection()
    ga_id = ObjectId(request.args['ga_id'])
    inital_generation = ga.GenerateRandomGeneration(ga_id,ThisMongoCollectionObject[0])
    return json.dumps(inital_generation)

@app.route('/record_candidate_score', methods=['POST'])
def record_candidate_score():
    """records the score of a candidate"""
    GetMongoCollection()
    ga_id = ObjectId(request.args['ga_id'])
    candidate_id = int(request.args['candidate_id'])
    score = int(request.args['score'])
    ga.RecordCandidateScore(ga_id,candidate_id,score,ThisMongoCollectionObject[0])
    return str(0)

@app.route('/get_next_generation', methods=['POST'])
def get_next_generation():
    """once all candidates have been scored this method runs the roulette wheel
    and the mutation and then gives you a new generation"""
    GetMongoCollection()
    ga_id = ObjectId(request.args['ga_id'])
    next_gen = ga.GetNextGeneration(ga_id,ThisMongoCollectionObject[0])
    return json.dumps(next_gen)
    #return json.dumps(genetic_algs[ga_id].current_generation)

def GetMongoCollection():
    if len(ThisMongoCollectionObject) == 0:
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client['ga_data']
        ThisMongoCollectionObject.append(db.get_collection("GeneticAlgorithmCollection"))
    pass

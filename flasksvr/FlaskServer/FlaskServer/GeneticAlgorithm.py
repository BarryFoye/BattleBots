import random
import logging
import pymongo
from pymongo import MongoClient

class GeneticAlgorithm(object):
    """Class to encapsulate the genetic algorithm in python"""

    #Generate a random genome
    def GenerateRandomGenome(genome_length, genome_numpossibleoptions):
        genome_data = list()
        for i in range(genome_length):
            genome_data.append(random.randint(0,genome_numpossibleoptions-1))
            pass
        return genome_data

    #Generate an initial generation consisting entirely of random genomes`
    def GenerateRandomGeneration(ga_id,ThisMongoCollectionObject):
        ga = ThisMongoCollectionObject.find_one({'_id': ga_id})
        generations = list();
        initial_generation = list();
        for i in range(ga['generation_size']):
            initial_generation.append(GeneticAlgorithm.GenerateRandomGenome(ga['genome_length'], ga['genome_numpossibleoptions']))
        generations.append(initial_generation)
        ThisMongoCollectionObject.find_one_and_update({"_id": ga_id}, {"$set": {"generations": generations}})
        return initial_generation

    #Run a roulette wheel algorithm and build the next generation
    def GetNextGeneration(ga_id, ThisMongoCollectionObject):
        #get scores from db
        ga = ThisMongoCollectionObject.find_one({'_id': ga_id})
        generation_id = len(ga['generations'])-1#
        #If the next line gives a typeerror, not all candidates have been scored.
        candidate_scores = ga['generations'][generation_id]
        scores = [x['score'] for x in candidate_scores]
        #Build roulette wheel
        total_score = sum(scores)
        percentages = [(x['score']/total_score * 100) for x in candidate_scores]
        cumulative_percentage = 0
        cumulative_percentages = [ ]
        for percentage in percentages:
            cumulative_percentage = cumulative_percentage + percentage
            cumulative_percentages.append(cumulative_percentage)
        next_generation = list()        
        while len(next_generation) < len(scores):
            #run roulette - stronger candidates have a higher chance of selection
            selection_1 = random.random() * 100
            selection_2 = random.random() * 100
            #get both parents and mate them
            for i in range(len(cumulative_percentages)):
                if selection_1 < cumulative_percentages[i]:
                    parent_1 = candidate_scores[i]['candidate']
                    break
            for i in range(len(cumulative_percentages)):
                if selection_2 < cumulative_percentages[i]:
                    parent_2 = candidate_scores[i]['candidate']
                    break
            #We don't want both parents to be the same, so if they are, randomise one of them
            #while parent_1 == parent_2:
            #    i = random.randint(0,len(scores))-1
            #    parent_2 = candidate_scores[i]['candidate']
            #mate the parents
            next_generation.extend(GeneticAlgorithm.Mate(parent_1,parent_2))
        GeneticAlgorithm.Mutate(next_generation, ga['genome_numpossibleoptions'], ga['mutation_percent'])
        ThisMongoCollectionObject.find_one_and_update({'_id': ga_id}, {'$push': {'generations': next_generation}})
        return next_generation

    #Randomly mutate the genome as per the mutation percentage set
    def Mutate(generation, genome_numpossibleoptions, mutation_percent):
        for i in range(len(generation)):
            for j in range(len(generation[i])):
                rand = random.random() * 100
                if rand < mutation_percent:
                    generation[i][j] = random.randint(0,genome_numpossibleoptions - 1)
                    pass
                pass
            pass
        pass

    #Mate two candidates and produce two new ones
    #uses a double crossover algorithm
    def Mate(gene1, gene2):
        crossover_points = [random.randint(0,len(gene1)), random.randint(0,len(gene1))]
        CrossoverPoint_1 = min(crossover_points)
        CrossoverPoint_2 = max(crossover_points)
        child1 = gene1[0:CrossoverPoint_1]
        child1.extend(gene2[CrossoverPoint_1:CrossoverPoint_2])
        child1.extend(gene2[CrossoverPoint_2:len(gene2)])
        child2 = gene2[0:CrossoverPoint_1]
        child2.extend(gene1[CrossoverPoint_1:CrossoverPoint_2])
        child2.extend(gene1[CrossoverPoint_2:len(gene1)])
        #ga_logger.debug("---")
        #ga_logger.debug("Mated " + str(gene1) + " with " + str(gene2) + "")
        #ga_logger.debug("xover points " + str(CrossoverPoint_1) + " with " + str(CrossoverPoint_2) + "")
        #ga_logger.debug("child " + str(child1) + " with " + str(child2) + "")
        return [child1, child2]

    #We score the candidate indexes with their scores, so the candidates can be scored and processed in parallel in the future
    def RecordCandidateScore(ga_id, CandidateIndex, Score, ThisMongoCollectionObject):
        ga = ThisMongoCollectionObject.find_one({'_id': ga_id})
        generation_id = len(ga['generations'])-1
        this_candidate = ga['generations'][generation_id][CandidateIndex]
        candidate_data = {"candidate": this_candidate, "score" : Score}
        ThisMongoCollectionObject.find_one_and_update(
            { "_id": ga_id },
            { "$set": { 'generations.'+str(generation_id)+'.'+str(CandidateIndex) : candidate_data}}
        )
        #TODO: Default all candidates to -1 to start with so you can see which have been scored already and which havent.


    #Constructor
    def new_ga(GenomeLength, GenomeNumPossibleOptions, GenerationSize, MutationPercent, ThisMongoCollectionObject):
        genome_length = GenomeLength
        genome_numpossibleoptions = GenomeNumPossibleOptions
        generation_size = GenerationSize
        mutation_percent = MutationPercent
        db_collection = ThisMongoCollectionObject
        post_data = {
           'genome_length': GenomeLength,
           'genome_numpossibleoptions': GenomeNumPossibleOptions,
           'generation_size': GenerationSize,
           'mutation_percent': MutationPercent
        }
        result = ThisMongoCollectionObject.insert_one(post_data)
        return result.inserted_id

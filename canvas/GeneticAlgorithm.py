import random
import logging

class GeneticAlgorithm(object):
    """Class to encapsulate the genetic algorithm in python"""

    ga_logger = [ ]

    genome_length = 1;
    genome_numpossibleoptions = 1;
    generation_size = 50;
    mutation_percent = 1;

    candidate_scores = [ ];
    current_generation = [ ];

    #Generate a random genome
    def GenerateRandomGenome(self):
        genome_data = list()
        for i in range(self.genome_length):
            genome_data.append(random.random(0, 1))
            pass
        return genome_data

    #Generate an initial generation consisting entirely of random genomes`
    def GenerateRandomGeneration(self):
        generation = list();
        for i in range(self.generation_size):
            generation.append(self.GenerateRandomGenome())
        self.current_generation = generation

    #Run a roulette wheel algorithm and build the next generation
    def GetNextGeneration(self):
        #Build roulette wheel
        scores = [x[1] for x in self.candidate_scores]
        total_score = sum(scores)
        percentages = [(x[1]/total_score * 100) for x in self.candidate_scores]
        cumulative_percentage = 0
        cumulative_percentages = [ ]
        for percentage in percentages:
            cumulative_percentage = cumulative_percentage + percentage
            cumulative_percentages.append(cumulative_percentage)
        next_generation = list()
        while len(next_generation) < len(self.current_generation):
            #run roulette - stronger candidates have a higher chance of selection
            selection_1 = random.random() * 100
            selection_2 = random.random() * 100
            #get both parents and mate them
            for i in range(len(cumulative_percentages)):
                if selection_1 < cumulative_percentages[i]:
                    parent_1 = self.current_generation[i]
                    break
            for i in range(len(cumulative_percentages)):
                if selection_2 < cumulative_percentages[i]:
                    parent_2 = self.current_generation[i]
                    break
            #We don't want both parents to be the same, so if they are, randomise one of them
            while parent_1 == parent_2:
                i = random.randint(0,len(self.current_generation))-1
                parent_2 = self.current_generation[i]
            #mate the parents
            next_generation.extend(self.Mate(parent_1,parent_2))
        self.current_generation = [ ]
        self.candidate_scores = [ ]
        self.current_generation = next_generation
        self.Mutate()

    #Randomly mutate the genome as per the mutation percentage set
    def Mutate(self):
        for i in range(len(self.current_generation)):
            for j in range(len(self.current_generation[i])):
                rand = random.random() * 100
                if rand < self.mutation_percent:
                    self.current_generation[i][j] = random.random(0, 1)
                    pass
                pass
            pass
        pass

    #Mate two candidates and produce two new ones
    #uses a double crossover algorithm
    def Mate(self, gene1, gene2):
        crossover_points = [random.randint(0,len(gene1)), random.randint(0,len(gene1))]
        CrossoverPoint_1 = min(crossover_points)
        CrossoverPoint_2 = max(crossover_points)
        child1 = gene1[0:CrossoverPoint_1]
        child1.extend(gene2[CrossoverPoint_1:CrossoverPoint_2])
        child1.extend(gene2[CrossoverPoint_2:len(gene2)])
        child2 = gene2[0:CrossoverPoint_1]
        child2.extend(gene1[CrossoverPoint_1:CrossoverPoint_2])
        child2.extend(gene1[CrossoverPoint_2:len(gene1)])
        self.ga_logger.debug("---")
        self.ga_logger.debug("Mated " + str(gene1) + " with " + str(gene2) + "")
        self.ga_logger.debug("xover points " + str(CrossoverPoint_1) + " with " + str(CrossoverPoint_2) + "")
        self.ga_logger.debug("child " + str(child1) + " with " + str(child2) + "")
        return [child1, child2]

    #We score the candidate indexes with their scores, so the candidates can be scored and processed in parallel in the future
    def RecordCandidateScore(self, CandidateIndex, Score):
        thisCandidateScore = [CandidateIndex, Score]
        self.candidate_scores.append(thisCandidateScore)

    #Constructor
    def __init__(self,GenomeLength, GenerationSize, MutationPercent):
        self.genome_length = GenomeLength
        self.generation_size = GenerationSize
        self.mutation_percent = MutationPercent
        self.ga_logger = logging.getLogger("GeneticAlgorithm")

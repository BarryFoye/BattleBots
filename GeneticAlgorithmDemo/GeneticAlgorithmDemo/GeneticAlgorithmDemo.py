# This demo will use all functions of the GeneticAlgorithm API
#it will generate random strings and eventually 'evolve' to the target string inputted by the user
#It is effectively a reimplementation of the demo shown in this video: https://www.youtube.com/watch?v=9zfeTw-uFCw

import requests
import json

print("Enter a target string. use only lowercase a-z characters:")
target=input()

#Set up API connection
url = "http://localhost:5555"

#Endpoints are defined below
url_Create_Genetic_Algorithm = url + "/init_ga?genome_length={}&generation_size={}&mutation_percent={}&num_possible_options={}"
url_Create_Random_Generation = url + "/generate_random_generation?ga_id={}"
url_Record_Candidate_Score   = url + "/record_candidate_score?ga_id={}&candidate_id={}&score={}"
url_Get_Next_Generation      = url + "/get_next_generation?ga_id={}"
url_Test_Connection          = url + "/test"

def clean_response_string(r) : return str(r.content).replace("b\'","").replace("\'","")

#Test the connection to the API
print("If the connection to the API is working, a random sentence from the origin of species will appear below:")
print("")
r = requests.post(url = url_Test_Connection)
print(r.content.decode("utf-8"))
print("")

#Start off by initialising a GA. The API returns an id that uniquely identifies our GA. 
#We need to store the unique ID as it is required for further API calls.
target_length = len(target)
generation_size = 150
mutation_percent = 10
num_possible_options = 26 #26 lowercase characters to choose from
r = requests.post(url = url_Create_Genetic_Algorithm.format(target_length,generation_size,mutation_percent,num_possible_options))

ga_id = clean_response_string(r)
print ("Successfully created Genetic Algorithm with id " + ga_id)

#The GA works in numbers but our string is letters so we define some simple functions to convert between the two
def char_to_num(char): return ord(char)-97
def num_to_char(num): return chr(num+97)
def nums_to_string(nums):
    string = list()
    for n in nums:
        string.append(num_to_char(n))
    return str(string)

#Work out the target sequence
target_num = list()
for c in target:
    target_num.append(char_to_num(c))

print("Your target string as a series of numbers is " + str(target_num))

#Set up the scoring function
#This function 'scores' the candidate - higher score = better candidate

#def scoring_function(this_candidate,target) :
#    scores = list()
#    idx = 0
#    for val in this_candidate:       
#        scores.append(26 - abs(val - target[idx]))
#        idx += 1
#        pass
#    return sum(scores)

def scoring_function(this_candidate,target) :
    score = 0
    idx = 0
    for val in this_candidate:
        if val == target[idx]:
            score +=1
        idx += 1
    return score * score


#Next step is to generate the initial, random generation. This step is only done once.
request_url = url_Create_Random_Generation.format(ga_id)
r = requests.post(url = request_url)
generation = json.loads(clean_response_string(r))

generation_count = 0
target_found = False

print("")
print("Starting Algorithm...")
print("")

#Loop through each candidate and score them
while (1):
    candidate_id = 0
    for c in generation:
        candidate_score = scoring_function(c['candidate'],target_num)
        #Tell the GA how this candidate scored
        requests.post(url = url_Record_Candidate_Score.format(ga_id,candidate_id,candidate_score))
        print("Recorded Gen {} Candidate {} Score {} - {}".format(generation_count,candidate_id,candidate_score,nums_to_string(c['candidate'])))
        #There must be some condition to end the algorithm. Here, we know the maximum score we're looking for so break on that.
        if(candidate_score == (len(target)) * len(target)):
            target_found = True
            print ("Target found!")
        candidate_id += 1
    #After all candidates have been evaluated, get next generation
    if target_found:
        break
    else:
        print ("")
        r = requests.post(url=url_Get_Next_Generation.format(ga_id))
        generation = json.loads(clean_response_string(r))
        generation_count += 1
    pass


#We found the target!
print("")
print("")
generation_count += 1
print ("Target found! Yay! It took " + str(generation_count) + " generations.")
print ("{} attempts were scored.".format(generation_count * generation_size))
print ("Brute-forcing this would be expected to take {} attempts".format(26 ** len(target)))
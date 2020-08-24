# Set up library imports.
import random
from collections import Counter
from itertools import chain

# install bitstring 
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("bitstring")

# import bitstring
from bitstring import *

########################################################
'''
    - This module assumes you first read the Jupyter notebook. 
    - You are free to add other members functions in class GeneticAlgorithm
      as long as you do not modify the code already written. If you have justified
      reasons for making modifications in code, come talk to us. 
    - Our implementation uses recursive solutions and some flavor of 
      functional programming (maps/lambdas); You're not required to do so.
      Just Write clean code. 
'''
########################################################

class GeneticAlgorithm(object):

    def __init__(self, POPULATION_SIZE, CHROMOSOME_LENGTH, verbose):
        self.wall_bit_string_raw = "01010101011001101101010111011001100101010101100101010101"
        self.wall_bit_string = ConstBitStream(bin = self.wall_bit_string_raw)
        self.population_size = POPULATION_SIZE
        self.chromosome_length = CHROMOSOME_LENGTH # this is the length of self.wall_bit_string
        self.terminate = False
        self.verbose = verbose # In verbose mode, fitness of each individual is shown. 

    def run_genetic_alg(self):
        '''  
        The pseudo you saw in slides of Genetic Algorithm is implemented here. 
        Here, You'll get a flavor of functional 
        programming in Python- Those who attempted ungraded optional tasks in tutorial
        have seen something similar there as well. 
        Those with experience in functional programming (Haskell etc)
        should have no trouble understanding the code below. Otherwise, take our word that
        this is more or less similar to the generic pseudocode in Jupyter Notebook.

        '''
        "You may not make any changes to this function."

        # Creation of Population
        solutions = self.generate_candidate_sols(self.population_size) # arg passed for recursive implementation.

        # Evaluation of individuals
        parents = self.evaluate_candidates(solutions)

        while(not self.terminate):
            # Make pairs
            pairs_of_parents = self.select_parents(parents)

            # Recombination of pairs.
            recombinded_parents = list(chain(*map(lambda pair: \
                self.recombine_pairs_of_parents(pair[0], pair[1]), \
                    pairs_of_parents))) 

            # Mutation of each individual
            mutated_offspring = list(map(lambda offspring: \
                self.mutate_offspring(offspring), recombinded_parents))

            # Evaluation of individuals
            parents = self.evaluate_candidates(mutated_offspring) # new parents (offspring)
            if self.verbose and not self.terminate:
                self.print_fitness_of_each_indiviudal(parents)

######################################################################
###### These two functions print fitness of each individual ##########

# *** "Warning" ***: In this function, if an individual with 100% fitness is discovered, algorithm stops. 
# You should implement a stopping condition elsewhere. This codition, for example,
# won't stop your algorithm if mode is not verbose.
    def print_fitness_of_one_individual(self, _candidate_sol):
        _WallBitString = self.wall_bit_string
        _WallBitString.pos = 0
        _candidate_sol.pos = 0
        
        matching_bit_pairs = 0
        try:
            if not self.terminate:
                while (_WallBitString.read(2).bin == _candidate_sol.read(2).bin):
                    matching_bit_pairs = matching_bit_pairs + 1
                print('Individual Fitness: ', round((matching_bit_pairs)/28*100, 2), '%')
        except: # When all bits matched. 
            pass
            return

    def print_fitness_of_each_indiviudal(self, parents):
        if parents:
            for _parent in parents:
                self.print_fitness_of_one_individual(_parent)

###### These two functions print fitness of each individual ##########
######################################################################

    def select_parents(self, parents):
        '''
        args: parents (list) => list of bitstrings (ConstbitStream)
        returns: pairs of parents (tuple) => consecutive pairs.
        '''
        ptuple = []
        num = int(self.population_size/2)
        for i in range(0,num):
            rand_num = random.randint(0,len(parents)-3)
            ptuple.append((parents[rand_num],parents[rand_num+1]))
            
        return ptuple
        

    # A helper function that you may find useful for `generate_candidate_sols()`
    def random_num(self):
        random.seed()
        return random.randrange(2**14) ## for fitting in 14 bits.

    def generate_candidate_sols(self, n): 
        '''
        args: n (int) => Number of cadidates solutions to generate. 
        retruns: (list of n random 56 bit ConstBitStreams) 
                 In other words, a list of individuals: Population.

        Each cadidates solution is a 56 bit string (ConstBitStreams object). 

        One clean way is to first get four 14 bit random strings then concatenate
        them to get the desired 56 bit candidate. Repeat this for n candidates.
        '''
        sol_list = []
        for i in range(0,n):
            sol = ''
            for i in range(0,56):
                # Generate 0 or 1 (56times)
                num = random.randint(0,1)
                # Concatenate them 
                string = str(num)
                sol = sol + string
            sol = ConstBitStream(bin=sol)
            sol_list.append(sol)
            
        return sol_list

    def recombine_pairs_of_parents(self, p1, p2):
        """
        args: p1, and p2  (ConstBitStream)
        returns: p1, and p2 (ConstBitStream)

        split at .6-.9 of 56 bits (CHROMOSOME_LENGTH). i.e. between 31-50 bits
        """
    
        p1 = p1.bin
        p1 = str(p1)[2:]
        
        p2 = p2.bin
        p2 = str(p2)[2:]

        randn = random.randint(31,50)
        s1 = p1[:randn]
        s2 = p1[randn:]
        s3 = p2[:randn]
        s4 = p2[randn:]
        
        ret1 = s1 + s4
        ret2 = s3 + s2
    
        ret1 = ConstBitStream(bin = ret1)
        ret2 = ConstBitStream(bin = ret2)
        return ret1,ret2

    def mutate_offspring(self, p):
        ''' 
            args: individual (ConstBitStream)
            returns: individual (ConstBitStream)
        '''
        p = p.bin
        p = p.zfill(56)
        p1 = p
        for i in range(0,len(p)):
            prob1 = random.randint(1,100)
            prob2 = random.randint(1,10)
            prob2 = 10*prob2
            if (p[i] == '1'):
                add = '0'
            else:
                add = '1'
                
            if (prob1 > prob2):
                p1 = p1[:i]+add+p1[i+1:]
              
        p = ConstBitStream(bin = p1)  
        return p
    
    def third_val(self,val): 
        return val[1]

    def evaluate_candidates(self, candidates): 
        '''
        args: candidate solutions (list) => each element is a bitstring (ConstBitStream)
        
        returns: parents (list of ConstBitStream) => each element is a bitstring (ConstBitStream) 
                    but elements are not unique. Fittest candidates will have multiple copies.
                    Size of 'parents' must be equal to population size.  
        '''
        
        total_match = 0
        fitness_list = []
        for i in range(0,len(candidates)):
            counter = 0
            candidate = candidates[i]
            candidate = candidate.bin
            candidate = str(candidate)[2:]
            j = 0
            while True:
                if (j >= len(self.wall_bit_string_raw)):
                    break
                if (candidate[j:j+2] == self.wall_bit_string_raw[j:j+2]):
                    counter = counter + 1
                j = j + 2
            fitness = counter
            fitness_list.append((candidates[i],fitness,0))
        
        tfitness = 0
        for bitstring,fit,x in fitness_list:
            tfitness = tfitness + fit
        
        avg_fitness =  (tfitness/28)/ len(candidates)
        
        for bitstring,fit,gen in fitness_list:
            next_gen = fit / avg_fitness
            next_gen = round(next_gen)
            gen = next_gen
        
        print("Fitness:", fitness_list)
        fitness_list.sort(key = self.third_val, reverse = True) 
           
        length = 0
        s = ''
        for bit,x,t in fitness_list:
            s = s + bit
        
        # Apply Roullete Wheel Formula
        ret = []
        pick = random.uniform(0, 1)
        current = 0
        while (len(ret) < self.population_size):
            for bit,fit,d in fitness_list:
                current += fit
                if current > pick:
                    ret.append(bit)
                if len(ret) == self.population_size:
                    break
            if len(ret) == self.population_size:
                    break
        return ret
        
        
       
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import random
import math

INITIAL_POPULATION = 100 # Initial Population of Boards at beginning.
MAX_TEST_CYCLES = 1500 # Maximum number of test cycles.
MATING_PROBABILITY = 0.85 # Probability of two parents mating.
MUTATION_RATE = 0.002 # Mutation Rate. 
MIN_SELECT = 15 # Minimum parents allowed for selection process.
MAX_SELECT = 40 # Maximum parents allowed for selection process. 
CHILD_PER_GENERATION = 25 # New children created per generation. 
MIN_SHUFFLES = 15 # For shuffling genes/positions in the Board
MAX_SHUFFLES = 30

MAX_LENGTH = 8 # Dimension of chess board.

class Board : #Class containing details and properties about a board (child / parent)

    fitness = 0.0
    conflicts = 0
    maxlength = 0
    selection_probability = 0.0
    selected = False

    def __init__ (self , maxlength) :
      self.maxlength = maxlength
      self.position_data = [0] * maxlength
      for i in range(self.maxlength) :
        self.position_data[i] = i
      self.fitness = 0.0
      self.conflicts = 0
      self.maxlength = 0
      self.selection_probability = 0.0
      self.selected = False
      return


    def calculate_num_conflicts(self , width) :     # Returns number of conflicts (pairs) between the queens in O(N) time complexity and O(N) space complexity
      freq_row = [0] * width            # Frequency of Queens in Horizontal Rows
      freq_mdiag = [0] * (2*width)      # Frequency of Queens in Main Diagonals
      freq_sdiag = [0] * (2*width)      # Frequency of Queens in Secondary Duagonals

      n = width  #Dimension of Board
      
      for i in range(n):
        freq_row.append(0)

      for i in range(n+n):
        freq_mdiag.append(0)
      
      for i in range(n+n):
        freq_sdiag.append(0)

      for i in range(n) :
        val = self.position_data[i]
        freq_row[val]+=1
        freq_mdiag[val+i]+=1
        freq_sdiag[n-val+1+i]+=1
      
      num_conflicts = 0

      for i in range (n+n):
        x,y,z = 0,0,0
        if (i<n):
          x = freq_row[i]
        y = freq_mdiag[i]
        z = freq_sdiag[i]
        num_conflicts += (x*(x-1))/2    # Number of conflicts in Horizontal Rows
        num_conflicts += (y*(y-1))/2    # Number of conflicts in Main Diagonals
        num_conflicts += (z*(z-1))/2    # Number of conflicts in Secondary Diagonals

      self.conflicts = num_conflicts    # Total Number of conflicts (pairs)
      return

    def get_Fitness(self):
      return self.fitness
    
    def get_Conflicts(self):
      return self.conflicts

    def get_Board(self):
      return self.position_data

    def get_Data_at_index(self , index):
      return self.position_data[index]

    def set_Data_at_index(self , data , index):
      self.position_data[index] = data
      return

    def set_Fitness(self , score):
      self.fitness = score
      return
    
    def set_selection_probability(self , sprob):
      self.selection_probability = sprob
      return

    def get_selection_probability(self):
      return self.selection_probability

    def set_selected(self , val):
      self.selected = val
      return

    def get_selected(self):
      return self.selected 

#End of Board Class       

class NQueens :

  def __init__(self , INITIAL_POPULATION , MAX_LENGTH , MIN_SHUFFLES , MAX_SHUFFLES , MAX_TEST_CYCLES , CHILD_PER_GENERATION , MIN_SELECT , MAX_SELECT , MATING_PROBABILITY , MUTATION_RATE):
    self.start_size = INITIAL_POPULATION
    self.maxLength = MAX_LENGTH
    self.min_Shuffles = MIN_SHUFFLES
    self.max_Shuffles = MAX_SHUFFLES
    self.maxTestCycles = MAX_TEST_CYCLES
    self.min_select = MIN_SELECT
    self.max_select = MAX_SELECT
    self.child_per_gen = CHILD_PER_GENERATION
    self.MatingProbability = MATING_PROBABILITY
    self.MutationRate = MUTATION_RATE
    
    self.population = []
    self.test_cycles = 0
    self.childCount = 0
    self.next_mutation = 0      # Schedulling Mutaton purposes.
    self.num_mutations = 0
    return

  def initialize_Population(self):    # Function to generate initial population.
    shuffles = 0
    boardIndex = 0

    for i in range(self.start_size):
      newBoard = Board(self.maxLength)
      self.population.append(newBoard)
      newBoardIndex = self.population.index(newBoard)

      shuffles = random.randrange(self.min_Shuffles, self.max_Shuffles)

      self.mutation(newBoardIndex , shuffles)
      newBoard = self.population[newBoardIndex]
      newBoard.calculate_num_conflicts(self.maxLength)
    return
  
  def mutation(self , boardIndex , shuffles):   # Function to perform mutation in genes / position data of the board.
    tempData = 0
    i = 0
    gene1 = 0
    gene2 = 0
    done = False

    thisBoard = self.population[boardIndex]

    while not done :
      gene1 = random.randrange(0 , self.maxLength)
      gene2 = self.getRandomNumber_Except(self.maxLength, gene1)

      tempData = thisBoard.get_Data_at_index(gene1)
      thisBoard.set_Data_at_index(gene1 , thisBoard.get_Data_at_index(gene2))
      thisBoard.set_Data_at_index(gene2 , tempData)

      if i == shuffles :
        done = True
      
      i+=1
    
    self.num_mutations += 1
    return


  def getRandomNumber(self , low , high):
    return random.randint(low, high)

  def getRandomNumber_Except(self , high , numberA):    # Generate a random number except numberA
    numberB = 0
    done = False

    while not done:
      numberB = random.randrange(0, high)
      if numberB != numberA:
        done = True
    
    return numberB


  def get_Fitness_Score(self):        # Function to score / calculate the fitness of the population
    popSize = len(self.population)
    thisBoard = Board(self.maxLength)
    bestScore = 0
    worstScore = 0

    thisBoard = self.population[self.get_maximum_conflicts()]
    worstScore = thisBoard.get_Conflicts()
    # Convert to a weighted percentage.
    thisBoard = self.population[self.get_minimum_conflicts()]
    bestScore = worstScore - thisBoard.get_Conflicts()

    for i in range(popSize):
      thisBoard = self.population[i]
      thisBoard.set_Fitness((worstScore - thisBoard.get_Conflicts()) * 100.0 / bestScore)
    return


  def get_maximum_conflicts(self):  # Function to find the Board with maximum number of conflicting (pairs of) Queens
    popSize = 0
    maximum = 0
    foundNewMax = False
    done = False

    while not done:
      foundNewMax = False
      popSize = len(self.population)
      for i in range(popSize):
          if i != maximum: # Avoiding self comparision
              board_A = self.population[i]
              board_B = self.population[maximum]
              # The maximum has to be in relation to the Target.
              if math.fabs(board_A.get_Conflicts() > board_B.get_Conflicts()):
                  maximum = i
                  foundNewMax = True

      if foundNewMax == False:
          done = True

    return maximum

  def get_minimum_conflicts(self):   # Function to find the Board with minimum number of conflicting (pairs of) Queens
    popSize = 0
    minimum = 0
    foundNewMin = False
    done = False

    while not done:
        foundNewMin = False
        popSize = len(self.population)
        for i in range(popSize):
            if i != minimum:
                board_A = self.population[i]
                board_B = self.population[minimum]
                # The minimum has to be in relation to the Target.
                if math.fabs(board_A.get_Conflicts() < board_B.get_Conflicts()):
                    minimum = i
                    foundNewMin = True

        if foundNewMin == False:
            done = True

    return minimum

  def board_selection(self): # Function to select board based on fitness (Roulette Selection)
    boardIndex = 0
    popSize = 0
    total_fitness = 0.0
    selTotal = 0.0
    rouletteSpin = 0.0
    done = False
    num_selection = random.randrange(self.min_select , self.max_select)
    thisBoard = Board(self.maxLength)
    thatBoard = Board(self.maxLength)

    popSize = len(self.population)
    for i in range(popSize):
        thisBoard = self.population[i]
        total_fitness += thisBoard.get_Fitness()

    total_fitness *= 0.01

    for i in range(popSize):
      thisBoard = self.population[i]
      thisBoard.set_selection_probability(thisBoard.get_Fitness() / total_fitness)

    for i in range(num_selection):
      rouletteSpin = random.randrange(0, 99)
      boardIndex = 0
      selTotal = 0
      done = False
      while not done:
         thisBoard = self.population[boardIndex]
         selTotal += thisBoard.get_selection_probability()
         if selTotal >= rouletteSpin:
            if boardIndex == 0:
                thatBoard = self.population[boardIndex]
            elif boardIndex >= popSize - 1:
                thatBoard = self.population[popSize - 1]
            else:
                thatBoard = self.population[boardIndex - 1]

            thatBoard.set_selected(True)
            done = True
         else:
            boardIndex += 1
    return
  
  def mating_pool(self):  # Function for mating of selected gene pool
    getRandProb = 0
    parent_board_A = 0
    parent_board_B = 0
    newIndex1 = 0
    newIndex2 = 0

    for i in range(self.child_per_gen):
       parent_board_A = self.choose_first_parent_board()
       # Testing probability of mating.
       getRandProb = random.randrange(0, 100)

       if getRandProb <= self.MatingProbability * 100:
            parent_board_B = self.choose_second_parent(parent_board_A)
            new_Child_Board_1 = Board(self.maxLength)
            new_Child_Board_2 = Board(self.maxLength)
            self.population.append(new_Child_Board_1)
            newIndex1 = len(self.population) - 1
            self.population.append(new_Child_Board_2)
            newIndex2 = len(self.population) - 1

            self.crossover(parent_board_A, parent_board_B, newIndex1, newIndex2)

            if self.childCount - 1 == self.next_mutation:
                self.mutation(newIndex1, 1)
            elif self.childCount == self.next_mutation:
                self.mutation(newIndex2, 1)

            new_Child_Board_1 = self.population[newIndex1]
            new_Child_Board_1.calculate_num_conflicts(self.maxLength)
            new_Child_Board_2 = self.population[newIndex2]
            new_Child_Board_2.calculate_num_conflicts(self.maxLength)  

            self.childCount += 2

            if math.fmod(self.childCount, self.round_up(1.0 / self.MutationRate)) == 0:
                self.next_mutation = self.childCount + random.randrange(0, self.round_up(1.0 / self.MutationRate))
    return


  def choose_first_parent_board(self):
    parent_board_index = 0
    done = False

    while not done :
      parent_board_index = self.getRandomNumber(0 , len(self.population) - 1)
      thisBoard = self.population[parent_board_index]

      if thisBoard.get_selected() == True:
        done = True
    return parent_board_index
  
  def choose_second_parent(self , first_parent_board):
    second_parent_index = 0
    done = False

    while not done :
      second_parent_index = random.randrange(0, len(self.population) - 1)
      if second_parent_index != first_parent_board :   # Avoiding to choose the same parent (ie. first parent)
        thisBoard = self.population[second_parent_index]
        if thisBoard.get_selected() == True :
          done = True
    return second_parent_index

  def crossover(self, parent_board_A, parent_board_B, newIndex1, newIndex2):  # Function of CROSSOVER for the selected gene pool
        parent_A = Board(self.maxLength)
        parent_A = self.population[parent_board_A]
        parent_B = Board(self.maxLength)
        parent_B = self.population[parent_board_B]
        new_child_1 = Board(self.maxLength)
        new_child_1 = self.population[newIndex1]
        new_child_2 = Board(self.maxLength)
        new_child_2 = self.population[newIndex2]

        crossPoint1 = random.randrange(0, self.maxLength)
        crossPoint2 = self.getRandomNumber_Except(self.maxLength, crossPoint1)
        if crossPoint2 < crossPoint1: # Swapping two cross points
            swap = crossPoint1
            crossPoint1 = crossPoint2
            crossPoint2 = swap

        # Copying parent genes / position data to child board.
        for i in range(self.maxLength):
            new_child_1.set_Data_at_index(parent_A.get_Data_at_index(i) , i)
            new_child_2.set_Data_at_index(parent_B.get_Data_at_index(i) , i)

        for i in range(crossPoint1, crossPoint2 + 1):
            gene1 = parent_A.get_Data_at_index(i)
            gene2 = parent_B.get_Data_at_index(i)
            pos1 = 0
            pos2 = 0
            for j in range(self.maxLength):
                if new_child_1.get_Data_at_index(j) == gene1:
                    pos1 = j
                elif new_child_1.get_Data_at_index(j) == gene2:
                    pos2 = j
            if gene1 != gene2:
                new_child_1.set_Data_at_index(gene2, pos1)
                new_child_1.set_Data_at_index(gene1, pos2)
            for j in range(self.maxLength):
                if new_child_2.get_Data_at_index(j) == gene2:
                    pos1 = j
                elif new_child_2.get_Data_at_index(j) == gene1:
                    pos2 = j
            if gene1 != gene2:
                new_child_2.set_Data_at_index(gene1 ,pos1)
                new_child_2.set_Data_at_index(gene2 ,pos2)
        return

  def prep_next_test_cycle(self):  # Function to prepare for initiating the next test cycle.
    popSize = len(self.population)

    for i in range(popSize):
      thisBoard = self.population[i]
      thisBoard.set_selected(False)
    
    return
  
  def round_up(self, val): # Utility Function for rounding up floating point values.
    rval = 0
    if math.modf(val)[0] >= 0.5:
        rval = math.ceil(val)
    else:
        rval = math.floor(val)
    return rval

  def population_status(self): # Utility function to get the status of population (ie. Fitness , whether selected ?)
    popSize = len(self.population)

    for i in range(popSize) :
      thisBoard = self.population[i]
      print(thisBoard.get_selected())
      print(thisBoard.get_Fitness())
    
    return

  def main(self):   # Main Function to identify the right sequence.
    population_size = 0
    done = False

    self.initialize_Population()

    self.num_mutations = 0
    self.next_mutation = random.randint(0, self.round_up(1.0 / self.MutationRate))

    while not done :

      population_size = len(self.population)
      for i in range(population_size):
        thisBoard = self.population[i]
        if thisBoard.get_Conflicts() == 0 or self.test_cycles ==  self.maxTestCycles:
          done  = True
      
      self.get_Fitness_Score()
      self.board_selection()
      self.mating_pool()
      self.prep_next_test_cycle()

      self.test_cycles += 1
    

    if self.test_cycles !=  self.maxTestCycles:
      popSize = len(self.population)
      for boardIndex in range(popSize):
        thisBoard = self.population[boardIndex]
        if thisBoard.get_Conflicts() == 0:
          for i in range(self.maxLength):
            if i != self.maxLength-1 :
              print(thisBoard.get_Data_at_index(i) , end = ' ')
            else :
              print(thisBoard.get_Data_at_index(i))
    
    return

if __name__ == "__main__":
    nqueens = NQueens(INITIAL_POPULATION , MAX_LENGTH , MIN_SHUFFLES , MAX_SHUFFLES , MAX_TEST_CYCLES , CHILD_PER_GENERATION , MIN_SELECT , MAX_SELECT , MATING_PROBABILITY , MUTATION_RATE)
    nqueens.main()


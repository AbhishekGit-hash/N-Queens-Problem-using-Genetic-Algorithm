# N Queens Problem using Genetic Algorithm

This notebook illustrates the concept of Genetic Computing through an example (of generating a text "winner takes it all") based approach.

The genetic algorithm is a method for solving both constrained and unconstrained optimization problems that is based on natural selection, the process that drives biological evolution. Ref : Genetic Computing

The objective is to be able to generate the text "winner takes it all". This can be attempted using a conventional probabilistic approach but doing so will take years to get to the solution of the problem. The probability of choosing "w" the first character is 1/27 which includes the blank space. Similalry for generating the "i" the second character is 1/27 and the same goes for every other character in the text. Now doing the calculation of the probability of generating the given text is very low hence this requires a different method to solve the problem.

In the context of Genetic Computing the following are the key elements

-Defining a solution space by generating an initial population
-The solution space consists of potential configurations
-Defining a fitness function to evaluate the solutions in the solution space
-Once the initial population and fitness score is done, new configurations are created in the solution space through crossover and mutation.
-The following figure shows how the crossover and mutation works

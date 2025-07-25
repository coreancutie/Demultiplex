#!/usr/bin/env python

#need this import to use argparse variables
import argparse

def get_args():
	'''this has 1 arguement: file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-f", help="Filename", type=str, required=True)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.filename as f
f:str = args.f


def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''

    #loops 101 times!
    for i in range(101):
        #appends the value, in no value given appends 0.0
        lst.append(value if value else 0.0) 

    #returns the final lst
    return lst

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    
    #uses ord to get the phred value
    #subtract 33 to get actual phred score
    return ord(letter) - 33

def populate_list(file: str) -> tuple[list, int]:
    """takes a file and returns a tuple of the list of quality scores and total number of lines 
    the quality score for each reccord is summed at the loaction in the list
    (the quality score of the first nucleotide of every read is summed together in position 0 of the list)
    """
    
    #making an empy list
    my_list: list = []
    
    #calling the init_list function (list is fill of 0.0)
    my_list = init_list(my_list)

    with open(file, "r") as f:
        
        #initalizing line count to get qual score lines
        line_count = 0
    
        #for each line in f (file)
        for line in f:
            #add the line count
            line_count += 1
            
            #getting rid of newline
            line = line.strip('\n')
            
            #getting the quality score line (line no. 4)
            if line_count%4 == 0:
                #getting the score and it's poisiton in the line
                for j, score in enumerate(line):
                    my_list[j] += convert_phred(score)

    #returns the list of quality score sums and total lines in the file
    return my_list, line_count

def calc_median(lst: list) -> float:
    '''takes a one-dimensional list that is already sorted and calculates and return the median as a float'''

    #for list with even number of values
    if len(lst)%2 == 0:
        #getting the first middle value
        middle_1 = len(lst) // 2
        #getting the second middle value
        middle_2 = middle_1 - 1
        #getting the mean of the 2 middle values
        median = (lst[middle_1] + lst[middle_2]) / 2
    
    #for list with odd number of values
    else:
        #getting value at the middle value index
        median = lst[len(lst) // 2]

    #returning the median value
    return median 



#calling the populate list to get the phred scores for every letter in the file
my_list, num_lines = populate_list(f)

print("Done with populating the list!")

score_lines = num_lines / 4

#looping through the
for i, score in enumerate(my_list):
    #calculating the mean and storing it back into my_list
    my_list[i] = score / score_lines

print("Done getting the averages!")

#plotting the scores!
import matplotlib.pyplot as plt

#making figure size
plt.figure(figsize=(12, 5))

#adding gridlines
plt.grid()

#plotting the mean quality scores as dots in pink
plt.plot(my_list, 'o', color="pink")

#adding lables
plt.xlabel("Base Position")
plt.ylabel("Mean Quality Score")
plt.title(f"Plot of Mean Quality Score of {f[14:16]} FASTQ file for Each Base Position in a Sequence")

#saving the figure
plt.savefig(f"{f[:-9]}.png")
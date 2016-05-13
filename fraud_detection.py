#Jessica Neves CSC 201 5/13/16
import csv
import matplotlib.pyplot as plt
import random

#reads csv file and appends the values from the specified columns into a list
def extract_election_vote_counts(filename, column_names):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        vote_counts = []
        for row in reader:
            for count in range(0, len(column_names)):
                data = row[column_names[count]]
                data = data.replace(",", "")#removes punctuation
                try:
                    vote_counts.append(int(data))#clean str changed to int
                except ValueError:#if cell in spreadsheet is empty
                    pass
    csvfile.close()#closes file
    return vote_counts

#makes a histogram from a list of numbers
def ones_and_tens_digit_histogram(numbers):
    occurring_digits = []#list of each ones and tens place digit
    num_occurrances = []
    histogram_data = []
    ones_and_tens_places = len(numbers) * 2#total ones and tens places
    for number in numbers:#depending on the size of the number
        if number > 99:#more than 2 digit number
            ones_place = number % 10#find ones place
            number = (number - ones_place) / 10#removes ones place
            tens_place = number % 10#finds tens place
            occurring_digits.append(ones_place)#append ones place digit
            occurring_digits.append(tens_place)#append tens place digit
        elif 99 >= number >= 10:#two digit number
            ones_place = number % 10#finds ones place
            number = number - ones_place#removes ones place
            tens_place = number / 10#finds tens place
            occurring_digits.append(ones_place)
            occurring_digits.append(tens_place)
        elif 10 > number > 0:#single digit number
            ones_place = number % 10#finds ones place
            tens_place = 0#tens place is 0
            occurring_digits.append(ones_place)
            occurring_digits.append(tens_place)
        elif number == 0:
            ones_place = 0
            tens_place = 0
            occurring_digits.append(ones_place)
            occurring_digits.append(tens_place)
    for number in range(0, 10):
        #for each number 0-9, append the count from occurring_digits
        occur_count = occurring_digits.count(number)
        num_occurrances.append(occur_count)
    for value in num_occurrances:
        #for each element in the list, adds to a histogram
        histogram_point = value / ones_and_tens_places
        histogram_data.append(histogram_point)
    return histogram_data      
         
def plot_iranian_least_digits_histogram(histogram):
    #plots ideal against iran histogram
    ideal_histogram = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    plt.clf()#clears the current figure
    plt.plot(ideal_histogram, label = 'Ideal')
    plt.plot(histogram, label = 'Iran')
    plt.ylabel('Frequency')
    plt.xlabel('Digit')
    plt.legend()
    plt.savefig('iran-digits.png')
    #plt.show()

def random_sample_histogram(number):
    #creates a random histogram
    sample = []
    for i in range(0, number):
        sample.append(random.randint(0, 99))
    sample_histogram = ones_and_tens_digit_histogram(sample)
    return sample_histogram
    
def plot_distribution_by_sample_size():
    #plots 5 random histograms of varying size
    ten_numbers = random_sample_histogram(10)
    fifty_numbers = random_sample_histogram(50)
    one_hundred_numbers = random_sample_histogram(100)
    one_thousand_numbers = random_sample_histogram(1000)
    ten_thousand_numbers = random_sample_histogram(10000)
    ideal_histogram = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    plt.clf()
    plt.plot(ideal_histogram, label = 'Ideal')
    plt.plot(ten_numbers, label = '10 random numbers')
    plt.plot(fifty_numbers, label = '50 random numbers')
    plt.plot(one_hundred_numbers, label = '100 random numbers')
    plt.plot(one_thousand_numbers, label = '1000 random numbers')
    plt.plot(ten_thousand_numbers, label = '10000 random numbers')
    plt.ylabel('Frequency')
    plt.xlabel('Digit')
    plt.legend()
    plt.savefig('random-digits.png')
    #plt.show()
    
def mean_squared_error(numbers1, numbers2):
    #calculates a mean squared error
    MSE = 0
    for i in range(0, len(numbers1)):
        difference = (numbers1[i] - numbers2[i])**2
        MSE += difference
    MSE = MSE / len(numbers1)
    return MSE

def calculate_mse_with_uniform(histogram):
    #calculates a mean squared error agains the ideal histogram
    uniform_data_set = []
    for value in range(0, len(histogram)):
        uniform_data_set.append(0.1)
    return mean_squared_error(histogram, uniform_data_set)

def compare_mse_to_samples(mse_value, number_of_samples):
    #compares a calculated MSE to sample MSEs
    MSE_larger_than = 0
    MSE_less_than = 0
    
    for group in range(0, 10000):
        histogram = random_sample_histogram(number_of_samples)
        sample_mse = calculate_mse_with_uniform(histogram)
        if sample_mse >= mse_value:
            MSE_larger_than += 1
        if sample_mse < mse_value:
            MSE_less_than += 1
    p_value = MSE_larger_than/10000
    return MSE_larger_than, MSE_less_than, p_value
    #returns all values in a tuple

def compare_iranian_mse_to_samples(iranian_mse, number_of_iranian_samples):
    #takes in iranian mse and the number of iranian data points
    values = compare_mse_to_samples(iranian_mse, number_of_iranian_samples)
    #values is a tuple returned from compare_mse_to_samples
    print("2009 Iranian election MSE: " + str(iranian_mse) +
          "\nQuantity of MSEs larger than or equal to the 2009 Iranian election"
          " MSE: " + str(values[0]) +#uses indexing to call from tuple
          "\nQuantity of MSE's smaller than the 2009 Iranian election MSE: " +
          str(values[1]) +
          "\n2009 Iranian election null hypothesis rejection level p: " +
          str(values[2]))
def compare_us_mse_to_samples(us_mse, number_of_us_samples):
    #takes in us mse and the numberof us data points
    values = compare_mse_to_samples(us_mse, number_of_us_samples)
    #values is a tuple returned from compare_mse_to_samples
    print("2008 United States election MSE: " + str(us_mse) +
          "\nQuantity of MSEs larger than or equal to the 2008 United States "
          "election MSE: " + str(values[0]) +
          "\nQuantity of MSEs smaller than the 2008 United States election "
          "MSE: " + str(values[1]) +
          "\n2008 United States election null hypothesis rejection level p: "
          + str(values[2]))
#The code in this function is executed when this file is run as a Python program
def main():
    filename = 'election-iran-2009.csv'
    column_name = ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"]
    numbers = extract_election_vote_counts(filename, column_name)
    histogram = ones_and_tens_digit_histogram(numbers)
    plot_iranian_least_digits_histogram(histogram)
    iranian_mse = calculate_mse_with_uniform(histogram)
    number_of_iranian_samples = len(numbers)
    compare_iranian_mse_to_samples(iranian_mse, number_of_iranian_samples)
    print('')
    us_2008_candidates = (["Obama", "McCain", "Nader", "Barr", "Baldwin",
                           "McKinney"])
    filename = 'election-us-2008.csv'
    numbers = extract_election_vote_counts(filename, us_2008_candidates)
    histogram = ones_and_tens_digit_histogram(numbers)
    us_mse = calculate_mse_with_uniform(histogram)
    number_of_us_samples = len(numbers)
    compare_us_mse_to_samples(us_mse, number_of_us_samples)
    
    
if __name__ == "__main__":
    main()

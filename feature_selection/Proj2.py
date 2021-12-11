import time
import numpy as np
from copy import deepcopy
import copy
import math

#found in Dr Keogh's slides
def forward_selection(data, current_set, accuracy, numfeatures):
    best_feature_set = copy.deepcopy(current_set)
    best_accuracy = accuracy
    
    current_features_set = []
    numlines = len(data)
    # numfeatures = len(data[0].strip().split())
    # idk why it doesn't work so im just calling the numfeatures
    
    for i in range(1, numfeatures):
        feature_to_add = 0
        best_in_search = 0   
        #k is a feature
 
        for k in range(1, numfeatures):
             #if it is not in the set, add
            if not k in current_features_set: 
                accuracy = leave_one_out_cross_validation(data,current_features_set,k, numlines, numfeatures)
                if accuracy > best_in_search : 
                    best_in_search = accuracy
                    feature_to_add = k                   
        current_features_set.append(feature_to_add)

        if best_in_search > best_accuracy:
            best_accuracy = best_in_search
            best_set = copy.deepcopy(current_features_set)

        elif best_in_search < best_accuracy:
            print("(Warning, accuracy has decreased! Go back!)")
        print(f'\n\nFeature set {current_features_set} was the best, accuracy is ',end='')
        print("{:2.2%}".format(best_in_search))
        
    return  (best_set, best_accuracy)


#found in Dr Keogh's slides
#https://www.analyticsvidhya.com/blog/2021/04/backward-feature-elimination-and-its-implementation/
def backward_selection(data, current_set, accuracy, numfeatures):
    best_feature_set = copy.deepcopy(current_set)
    best_accuracy = accuracy

    # current_features_set = [] #i can't be doing this bc we going backwards
    current_features_set = set(range(1,numfeatures+1))
    numlines = len(data)

    for i in range(1, numfeatures):
        feature_to_remove = 0
        best_in_search = 0
        #k is a feature
        for k in range(1, numfeatures+1):
            #if it is in the set, remove
            if k in current_features_set: 
                accuracy = leave_one_out_cross_validation(data,current_features_set,(-1*k),numlines,numfeatures)
                if accuracy > best_in_search:
                    best_in_search = accuracy
                    feature_to_remove = k
        #removing said feature
        current_features_set.remove(feature_to_remove)

        if best_accuracy < best_in_search:
            best_accuracy = best_in_search
            best_set = copy.deepcopy(current_features_set)
        #if the accuracy lowered
        elif best_accuracy >best_in_search:
            print("Warning, accuracy has decreased! Go back!")
        print(f'\n\nFeature set { current_features_set } was the best, accuracy is ',end='')
        print("{:2.2%}".format(best_in_search))
        
    # completing search to return best set and accuracy
    return  (best_set, best_accuracy)

def leave_one_out_cross_validation(data, current_set,feature_to_add, numlines, numfeatures):
    #basically nearest neighbor
    cross_check = deepcopy(list(current_set))
    #if feature is positive
    if feature_to_add > 0:
        cross_check.append(feature_to_add)

    #if feature is negative
    elif feature_to_add < 0:
        cross_check.remove(abs(feature_to_add))

    elif len(cross_check) == 0:
        return 0

    #set all the unnecessary features to 0
    cross_data = deepcopy(data)
    for i in range(0, numlines):
        for k in range(1, numfeatures):
            if k not in cross_check:
                # print(type(cross_data[i][k]))
                cross_data[i][k] = 0

    number_correctly_classified = 0 #counter for the numerator for k-fold

    # Calculating the nearest neighbor distance and classifying each instance
    # then using the correctly classified values to calculate accuracy
    for i in range(0, numlines):
        object_to_classify = cross_data[i][1:]
        label_object_to_classify = cross_data[i][0]

        nearest_neighbor_distance = float('inf')
        nearest_neighbor_location = float('inf') #numlines + 1 #float('inf') #why not working?

        for k in range(0, numlines):
            if k != i:
                distance = np.sqrt(sum([(a - b) * (a - b) for a, b in zip(object_to_classify, cross_data[k][1:])]))

                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_location = k
                    nearest_neighbor_label = cross_data[nearest_neighbor_location][0]

        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified = number_correctly_classified + 1

    accuracy = number_correctly_classified / len(cross_data) #len(cross_data) the number of instances in dataset

    print('The current accuracy is for using feature(s) {', end = '') 
    print(f'{cross_check}',end = '} ') #feature subset
    print("{:2.2%}".format(accuracy)) #calculates the percentage
    # https://www.geeksforgeeks.org/how-to-convert-fraction-to-percent-in-python/
    return accuracy


def read_file(filename):
    file_data = []
    f = open(filename, 'r')
    
    data_set = f.readline()
    numfeatures = len(data_set.split()) - 1 
    # print( str(data))

    f.seek(0, 0)
    numlines = len(f.readlines())
    #https://www.tutorialspoint.com/python/file_seek.htm
    
    f.seek(0, 0)
    data = [[] for i in range(numlines)]

    print(f'\nThe data has %d features (not including the class attribute), with %d instances\n' % (numfeatures, len(data) ))
    for i in range(numlines):
        data[i] = [float(j) for j in f.readline().split()]
    print("Finished processing data")
    return data, numfeatures

#not necessary, i am tired for typing in the data set names
def menu():
    option1 = "Small_data__90.txt"
    option2 = "LARGE_data__91.txt"
    option3 = "Small_data__86.txt"
    preselect = input("Do you want...\n\t 1)options of data sets \n\t 2)your own dataset.\nChoose 1 or 2.\n")
    if(preselect == '1'):
        optionfile = input("Here are your options: \n\t1) " + option1 + "\n\t2) " + option2 + "\n\t3) " + option3 + " (this is to check)\n")
        if(optionfile == '1'):
            filename = option1
            return filename
        elif(optionfile =='2'):
            filename = option2
            return filename
        elif(optionfile =='3'):
            filename = option3
            return filename
    elif(preselect == '2'):
        filename = input("Insert the name of the file\n")
        return filename

def main():
    #process the data
    print("This is Tiffany's Feature selection algorithm")
    filename = menu()
    data,numfeatures = read_file(filename)
    #My data sets
        #Small_data__90.txt
        #LARGE_data__91.txt

    #The following is seen in Dr. Keogh's debriefing slides    
    #remember numfeatures is -1 cause not including class attribute
    current_set = list(range(1, numfeatures +1))
    feature_to_add = 0

    accuracy = leave_one_out_cross_validation(data,current_set,feature_to_add, len(data), numfeatures+1)
    choice = input("Which algorithm would you like to run?\n\t Type (1) for forward selection. \n\t Type (2) for backward selection.\n")

    #i need to time it
    #https://www.udacity.com/blog/2021/09/create-a-timer-in-python-step-by-step-guide.html
    start = time.time()
    if choice == '1':
        best_set, best_accuracy = forward_selection(data, current_set, accuracy, numfeatures)
    elif choice == '2':
        best_set, best_accuracy = backward_selection(data, current_set, accuracy, numfeatures)

    end = time.time()
    total_time = end - start
    
    print(f'Finished Search!! The best feature subset is {best_set}, which has an accuracy of ')
    print("{:2.2%}".format(best_accuracy))
    print("The total amount of time it took to run algorithm: " + str(total_time) + " seconds.")

if __name__ == '__main__':
    main()





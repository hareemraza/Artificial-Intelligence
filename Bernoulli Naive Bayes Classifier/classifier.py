import numpy as np
import sys

def load_data(fileName, datasize):
    """ this function takes filepath as an argument and loads data inside a list"""
    f= open(fileName)
    data= []
    for i in range(datasize):
        line= f.readline()
        line= np.fromstring(line, dtype= 'int', sep=',')
        data.append(line)
    data= np.array(data)
    f.close()
    return data

def calculate_priors(class_occ):
    ones= class_occ.sum()
    prob_1= ones/ class_occ.shape[0]
    prob_0= 1- prob_1
    return prob_0, prob_1

def calculate_conditionals(data_normal, data_abnormal, p_n, p_ab):
    testpass_normal= data_normal.sum(axis=0)/data_normal.shape[0]
    testfail_normal= 1- testpass_normal
    testpass_normal= testpass_normal*p_n
    testfail_normal= testfail_normal*p_n 
    testpass_abnormal= data_abnormal.sum(axis=0)/data_abnormal.shape[0]
    testfail_abnormal= 1- testpass_abnormal
    testpass_abnormal= testpass_abnormal*p_ab
    testfail_abnormal= testfail_abnormal*p_ab    

    return testpass_normal,testfail_normal, testpass_abnormal, testfail_abnormal

def test(test_data, testpass_normal,testfail_normal, testpass_abnormal, testfail_abnormal):
    labels= []
    for i in range(test_data.shape[0]):
        a=np.prod((test_data[i]*testpass_normal)+((1-test_data[i])*testfail_normal))    
        b=np.prod((test_data[i]*testpass_abnormal)+((1-test_data[i])*testfail_abnormal))
        if a<b:
            labels.append(0)
        else:
            labels.append(1)
    return labels


def accuracy(y_pred, y_true):
    correct = np.sum(y_pred==y_true)
    accuracy= correct/len(y_pred)
    return accuracy

def main():
     #load train and test files
     train_file= sys.argv[1]
     test_file = sys.argv[2]
     train_data= load_data(train_file, 80)
     test_data = load_data(test_file, 187)

     #caculate priors ie probabilty of normal and abnormal
     p_ab, p_n= calculate_priors(train_data[:,0])
     print("\nStarting to train on 80 data points .....")
     #calculate conditional probabililities for each test
     testpass_normal,testfail_normal, testpass_abnormal, testfail_abnormal= calculate_conditionals(train_data[:40,1:],train_data[40:,1:],p_n , p_ab)
     print("Training Complete")
     print("-------------------------------------------")
     print("Testing on 187 data points")
     labels= test(test_data[:,1:], testpass_normal,testfail_normal, testpass_abnormal, testfail_abnormal)

     acc= accuracy(labels, test_data[:,0])
     print("Total Accuracy= " + str(acc*100) + " %")     


main()        

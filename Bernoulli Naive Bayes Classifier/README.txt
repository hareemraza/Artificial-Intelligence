#Naïve Bayes Classifier

The goal of this assignment is to implement Naïve Bayes Classifier. You will use the Bernoulli
naïve Bayes model for the classification task. Bernoulli model requires that all attributes value
is binary as a result the dataset of SPECT, provided to you, contains only binary values.

#Explanation of dataset:

Each patient is classified into two categories: Normal and Abnormal, depending on the number
of medical tests he/she passes. The database contains 267 patients’ data, every person
underwent 22 medical tests and each test was either pass or fail. As a result, for each patient
22 binary values were extracted.

You have been provided with two files, Spect_train and Spect_test. Spect_train has a total 80
data points and Spect_test has 187 data points.
You will use Spect_train patient data to train your naïve Bayes classifier and Spect_test to test
it.

A single patient in the dataset is described as a single line of the file. So, each line has 23
values, the first value of each line describes whether the person was described as normal (value
of 1) or abnormal (value of 0). All other 22 values define which test number the patient failed
and which he/she passed.

#Tasks

You have to implement the Bernoulli naïve Bayes classifier for the above set such that given
22 medical test reports of a person, your classifier predicts whether the person is normal or
abnormal. You will test your classifier using Spect_test file.

You also have to write a short report on the process, and you will be marked on the quantity of
the content, so write anything you feel deserves credit. (Should not be more than a page). Take
both Spect_test and Spect_train files as input from command line as mentioned in the
instructions. Both your training and testing code will be in the same file (classifier.py), you can
divide it in classes or functions as appropriate.

#Sample Output:

You should correctly show your output on the screen.
##########
Starting to Train on 80 data points . . .
Training Complete
Testing on 187 data point . . .
Total Accuracy: = 90%
##########

#Command Line Arguments

To run the program, give the following command line arguments
python3 classifier.py Spect_train Spect_test

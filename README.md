# Sickle-Cell-Image
This project presents a system for detecting sickle cell disease
 (SCD) using a Convolutional Neural Network (CNN) model, designed
 to improve early diagnosis through automated analysis of microscopic
 blood smear images. The system begins with the input of microscopic
 blood cell images, which undergo preprocessing steps such as normal
ization, resizing, and data augmentation. The preprocessed images
 are divided into training and testing sets, with the CNN model be
ing trained on the former to recognize features associated with sickle
shaped red blood cells. The model is then evaluated for accuracy using
 the testing set. Key stages in the system include data preprocessing,
 feature extraction through convolutional and pooling layers, and clas
 sification using fully connected layers. The output layer of the CNN
 uses softmax or sigmoid activation functions to categorize the images
 as either containing sickle cells or normal cells. The system’s perfor
mance is evaluated based on metrics such as accuracy, precision, recall,
 and specificity

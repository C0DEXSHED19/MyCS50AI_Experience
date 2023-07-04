https://cs50.harvard.edu/ai/2020/projects/5/traffic/
As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, you’ll use TensorFlow to build a neural network to classify road signs based on an image of those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the German Traffic Sign Recognition Benchmark (GTSRB) dataset http://benchmark.ini.rub.de/?section=gtsrb&subsection=news(To test the code, please download the dataset), which contains thousands of images of 43 different kinds of road signs.

Those are the steps that I took to maximize the AI's efficiency and accuracy:

First of all, I tried a model without adding any convolutional, pooling and hidden layers and the model was 80% accurate and was pretty fast. 

Adding a 16 filter of size 3x3 convolutional layer increases the accuracy to 89% but creates an overfitting problem as training data shows an accuracy of 97% as opposed to 89% on testing data.

Overfitting problem was solved by adding droupout.

Accuracy wa increased to 90% after adding 2x2 max pooling layers and using 32 filter 3x3 convolutional layers.

Adding hidden layers of 512 units increased accuracy to 94% and reduced variance but it costed more time.

Adding another 64 filter 3x3 convolutional layer increased accuracy to 96%.

After trying many models the one that I chose was the one with two convolutional layers (one 32 , 3x3 and the other 64, 3x3) both layers were followed by max pooling layers (2x2) after which a 512 units hidden layers were used in addition to droupout. This model was accurate (95%) and did not cause overfitting problems and has similar training and testing loss.

Link to my youtube video where I demonstrate my code:
https://youtu.be/meGqSv9YKtA


# Kopernikus

Solution to the take home code assignment

Answer to the assignment questions:



Question: What did you learn after looking on our dataset?

The following observations were deduced from the dataset:

    1. The dataset contains 1080 png files
    2. The images are of varying resolutions and sizes
    3. There is a corrupt png file c21_2021_03_27__10_36_36.png which we are unable to read into our code.
    4. The images have been taken by 4 different cameras namely c10, c20, c21 and c23
    5. All images appear to be taken in the same parking facility.
    6. Images have been taken at different times of days.
    7. There is a significant change in images due to lightning exposure at different times of day. Making it harder to eliminate redundant images.
    8. The images are taken at time lapse. It appears that they are arranged in the order of time they were taken.



Question: How does you program work?

The details of the working of the programm are explained in the solution.ipynb notebook in the repo. 
The code has been developed iteratively to solve various problems apart from the main task which is reading the directory files and deleting the similar images. 

In brief the solution calculates change score of 2 consecutive images after preprocessing them using the already provided functions. The code then deletes them if the score is less than 300. On executing the solution.py file, the user is asked to input the directory path containing the png images(currently designed to handle only png). It also checks for errors while reading and deleting the images to prevent the code from being interrupted.



Question: What values did you decide to use for input parameters and how did you find these values?

The following values were selected

    1. gaussian_blur_radius_list: 
    It was set to 9 after iterating for various values. Higher blur value may result in 
    blurring the key features of the images and lower value results to be computationally 
    expensive. To retain the balance of features and computation we arrived at the value of 9.
    More details providedd in solution.ipynb in Trial 5.

    2. min_contour_area: 
    This was set to 25 to allow the code to detect objects which are small due to being at
    a farther distance fromt he camera. refer Trial 5 in Solutions.ipynb where a car could 
    not be detected with a higher value of contour area. 

    3. threshold for change_score:
    This was set at 300 after the results of Trial 7(solution.ipynb)



Question: What you would suggest to implement to improve data collection of unique cases in future?

To improve data collection we could focus on:

    1.  Including a wide range of environmental conditions, lighting conditions, and variations 
    in object appearances.
    
    2. Add synthetic lightning / orientation effects on existing images to create a wider level
    of variation in the dataset.
    
    3. Most of the cases in this dataset has very few objects. A more crowded space can be used
    to identify more challenging situatuions.



Question: Any other comments about your solution?

The task was a great learning experience.

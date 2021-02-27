# How Do We Design a Good Online Course for Business Analytics?

## Table of Contents
1. [Introduction](#introduction)
2. [File Structure](#filestructure)
3. [Instructions](#instructions)
4. [Pipeline](#pipeline)
5. [Exploring Variables](#variables)
6. [Regression](#regression)

![intro figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/udemy.png?raw=true)

<a name="instroduction"></a>
## Introduction
Websites for a massive open online course (MOOC), such as Udacity, Udemy, and Coursera, provide learners a low-cost, highly efficient way to acquire knowledge. Business analytics, which relies mainly on computer coding, is a popular topic in MOOC websites. 

In this project, we aim to discover the secrete of designing an excellent online course for business analytics. 

<a name="filestructure"></a>
## File Structure:
    data
    | - raw                         # A folder contains the raw data from webscrapping.
    ETL
    |- ETL_nonText.ipynb            # notebook for process non-text information.
    |- ETL_Text.ipynb               # notebook for process text information.
    |- text_mining.py               # functions for text mining. 
    model
    |- Analysis.ipynb               # notebook for analysis the dataset. 
    webscrap
    |- get_course_list.py           # python scripts for getting course list.
    |- get_course_data.py           # python scripts for getting course data. 
    README.md

<a name="instructions"></a>
## Instructions:
* Install dependencies, including NumPy, SciPy, Pandas, Sciki-Learn, Gensim, Selenium, and statsmodels.
* Run the following commands to set up your data and model.
    - to run "get_course_list.py" and then "get_course_data.py" in the "webscrap" folder to perform web scrapping. 
    - To run "ETL_nonText.ipynb" in "ETL" folder to cleans non-text data.
    - To run "ETL_Text.ipynb" in "ETL" folder to process text data.
    - To run "Analysis.ipynb" in "model" folder to analyze the final dataset.

<a name="pipeline"></a>
## Pipeline
We use the package Selenium with Python to perform web scraping on the Udemy website.  The list of 1005 courses is obtained from Udemy's webpage for Business Analytics & Intelligence Courses. We use Gensim to perform topic modeling on the course description and the instruction introduction.  

![pipe figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/pipe.png?raw=true)

<a name="variables"></a>
## Exploring Variables
we set the enrollment number as the target variable.

![enrollment figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/enrollment.png?raw=true)

We plot the word clouds of topics in course description and instructor information. 
![description figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/lda_description.png?raw=true)
![instruction figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/lda_instructor.png?raw=true)

<a name="regression"></a>
## Regression
Use ordinary least squares (OLS) model to check the impacts of independent variables on the dependent variable (enrollment number). 

![regression figure](https://github.com/leizhipeng/analyze_mooc_course_data/blob/main/figures/OLS.png?raw=true)



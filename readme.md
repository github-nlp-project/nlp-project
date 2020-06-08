# GitHub NLP Project

For this project, we scraped data from GitHub repository README files using GitHub's API. 

![example readme language breakdown](example_readme.gif)

## Data Dictionary

**language**: Programming language used for repository project

**category**: The category within the energy sector

**repo**: The specific repo referenced with that observation

**readme_contents**: Description of each repository containing keywords used to make predictions

**clean_tokes**: README content normalized removing any uppercased characters, special characters, non-alpha characters, and alpha strings with 2 or less characters

**clean_stemmed**: README content reducing each word to its root stem and then removes any stopwords

**clean_lemmatized**: README content reducing each word to its root word and then removes any stopwords

**word_count**: The total word count for that observation

## Goal

The primary goal for this project was to build an NLP model that can predict the primary language of REPO using the text in the README file.

As a secondary goal, we decided to pull repos from a specific sector, or topic, to see if an industry we were interested is utilizing a program language we're familiar with.

Due to the first and second goals, this repo can be used as a means to research an potenial industry you might be interested in entering, and knowing what programming language you'll need to have familiarity with.

## Deliverables

> A well-documented jupyter notebook that contains your analysis.

[Check out the notebook here](https://github.com/github-nlp-project/nlp-project/blob/master/github_nlp_notebook.ipynb "Final Notebook")

> Three to four slide deck suitable for a general audience that summarize your findings - including well-labelled visualizations

[Here' the deck](https://www.canva.com/design/DAD-LM8dJPk/6-UD1UppB0-u5LeA9fjB2g/view?utm_content=DAD-LM8dJPk&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink "Presentation Link")

## Exploration

Some of the questions answered in either the notebook or deck:

1. What are the most common words in READMEs?

2. What does the distribution of IDFs look like for the most common words?

3. Does the length of the README vary by programming language?

4. Do different programming languages use a different number of unique words?

## Model

How top performing model used the top 4 languages in the corpus, a TF-IDF Vectorizor, and a Random Forest Classifier. The results were 92.31% accuracy on the train dataset and 60.47% accuracy on the test dataset.

## *Technical Skills used*

* Python
* Jupyter Notebook
* VS Code
* Various Data Science libraries (Pandas, Numpy, Matplotlib, Seaborn, Sklearn, etc.)
* BeautifulSoup
* nltk
* Stats (Hypothesis testing, correlation tests)
* Classification Models (Decision Tree, Random Forest, KNN)

## SUMMARY

Github READMEs can be good predictors of the programming languages of the repos. With NLP models language is important, so it isn't a surprise that the longer and more in-depth a README is, the better we can get at predicting the primary language. 

Whenever possible, words that are unique to a particular programming language, including the name of that language, make for key identifiers of a language. 

As with most data work, NLP modeling is no different, imbalances in your data affect everything, most importantly model performance. To improve our models, we'd want to ensure a better language distribution throughout the corpus, and gathering more observations generally speaking will also possitively impact model performace.

## Want to use our code?

You can use our python files to recreate the work done in our notebook. You'll also need to get create an env.py file that includes your GitHub username and GitHub token.

***Be sure to include a .gitignore file that includes that env.py***
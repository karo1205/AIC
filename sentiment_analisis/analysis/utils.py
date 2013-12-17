""" This module contains helper functions needed for preccessing data coming from
the crowdsorucing platform

Docstring

"""
import json
import nltk

#from analysis.models import Feed, Task


def transform_task_to_data(task):

    """This function generates a JSON Structure out of the properties of the
    specific task

    """

    data={}
    data['header'] = "Identify Product and Company Names"
    data['question'] = """
    Plaese read this text carefully, filter out product and
    company names and put them into the textfields below.
    """
    data['additional_header'] = "Instructions"
    #data['additional_input']={}
    #for i in range(1,6):
    #    data['additional_input']['keyword' + str(i)] = ""
    data['additional_input'] = "Please identifiy product and company names out of the given text and put the names into the 'keywords' collumn. Further put either a 'C' for company or a 'P' for product in to the second collumn"
    data['headers'] = ("Keyword", "Product or Company?")
    data['input'] = nltk.clean_html(task.feed.content)
    data['keyword_count'] = 5
    return data


def process_task_answers():

    """This funcion  goes trough all unprocessed tasks and add news
    keywords,sentiments, workes and relations

    Docstring

    """

    pass

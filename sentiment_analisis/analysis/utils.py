""" This module contains helper functions needed for preccessing data coming from
the crowdsorucing platform

Docstring

"""
import json

#from analysis.models import Feed, Task


def transform_task_to_data(task):

    """This function generates a JSON Structure out of the properties of the
    specific task

    """

    data={}
    data['header'] = "Identify Product and Company Names"
    data['question'] = """
    Plaese read this text carefully, filter out product and
    company names and put them into the textfields below
    """
    data['additional_header'] = ""
    data['additional_input']={}
    for i in range(1,6):
        data['additional_input']['keyword' + str(i)] = ""
    data['headers'] = ("Keyword", "Rating")
    data['input'] = task.feed.content
    return data


def process_task_answers():

    """This funcion  goes trough all unprocessed tasks and add news
    keywords,sentiments, workes and relations

    Docstring

    """

    pass

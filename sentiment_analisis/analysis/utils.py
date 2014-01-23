""" This module contains helper functions needed for preccessing data coming from
the crowdsorucing platform
"""
import json
import nltk
import logging
from analysis.models import Task, Keyword

logger = logging.getLogger(__name__)


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
    data['headers'] = [{"text":"Keyword","values":[]}, {"text":"Product or Company?","values":["P","C"]}]
    data['input'] = nltk.clean_html(task.feed.content)
    data['keyword_count'] = 5
    return data


def process_task_answers():

    """
    This funcion  goes trough all unprocessed tasks and add news
    keywords,sentiments, workes and relations

    """

    logger.info("start processing keywords")

    """
    Process Task Type 1

    """

    opentasks = Task.objects.filter(status='D')  # get all started tasks
    logger.info('Getting done tasks from DB. ' + str(opentasks.count()) + ' elements found')
    for t in opentasks:
        logger.info("Processing Task " + str(t.id))
        try:
            answer = json.loads(t.answer)
            #answer = t.answer
        except ValueError:
            logger.error("the answer field of task " + str(t.id) + " does not contain a valid JSON Format. Skipping.")
            continue    # if there is not valid JSON there is no pint of considerung this answer
                        # TODO: Implement quality control and pot task
                        # again

        for kw in answer['keywords'].keys():
            try:
                keyword = Keyword.objects.get(text = kw, category = answer['keywords'][kw])
                logger.info('Keyword "' + kw + '" already in DB')
                t.keywords.add(keyword)
                logger.info('Keyword "' + kw + '" assigned to Task' + str(t.id))
                # TODO debug here
                keyword_inverse = Keyword.objects.filter(text=kw).exclude(category=answer['keywords'][kw])
                if len(keyword_inverse) == 0:
                    continue
                elif keyword.task_set.count() / (keyword_inverse.task_set.count() + keyword.task_set.count()) >= 1:
                    t.worker.score -= 1
                    t.worker.save()
                    logger.info('Keyword "' + kw + '" has wrong catgory set.' + str(t.worker.id)+ ' was degraded')
            except Keyword.DoesNotExist:
                if t.feed.content.find(kw) == -1:  #if keyword is not found in text of the feed
                    t.worker.score -= 1
                    t.worker.save()
                    logger.info('Keyword "' + kw + '" was not found in feed. worker ' + str(t.worker.id)+ ' was degraded')
                else:
                    newkeyword=Keyword(text=str(kw), category=answer['keywords'][kw])
                    newkeyword.save()
                    t.keywords.add(newkeyword)
                    logger.info('new keyword "' + kw + '" created and assigned to Task' + str(t.id))

        t.status='P'  # set status to processed
        t.save()

    pass

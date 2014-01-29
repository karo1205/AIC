#README:

##Description
This Project contains of two django web applications:

1.) A Sentiment Analysis app, which collects feed from Yahoo finance and posts them to a Crowssoucring application

2.) A Crowdsourcing simulator which provides a rudimentary GUI for Task completion and pushes the answers back via callback function to the sentiment analysis application

Both Application are connection via a REST API.


##Installation


    cd DIRECTORY_WHERE_IT_SHOULD_BE
    sudo apt-get install python-setuptools
    sudo easy_install virtualenv
#### create virtuel environment:

    virtualenv --no-site-packages django

#### enter the virtual environment
    
    source django/bin/activate
    cd django/

#### install django (without sudo becasue already in the virtualenv):

    easy_install django==1.5

    git clone https://github.com/karo1205/AIC.git

    cd AIC

    cp -r * ../

    cd ..

    pip install south
    pip install django-tastypie
    pip install django-cron
    pip install requests
    pip install nltk 
    pip install feedparser 
    pip install django-chart-tools
    
#### Inititialize the database
    cd sentiment_analisis
    python manage.py syncdb

Choose "yes" and choose a Username and Password

    cd ../crowdsource_sim
    python manage.py syncdb

Choose "yes" and choose a Username and Password


Add some initial data to the database
    python manage.py sqlcustom polls | ./manage.py dbshell

#### start crowdsourcing platform simulator
    python manage.py runserver 8002
NOTE: the crowdsourcing plattform always hav to run on the port 8002
Don't mix the ports up!!

#### Run new terminal(Second Terminal): 
(on every terminal you have to "source django/bin/activate")

    cd django/sentiment_analisis/

#### start sentiment analysis
    python manage.py runserver

#### Run new terminal(Third Terminal): 
(on every terminal you have to "source django/bin/activate")

    cd django/sentiment_analisis/

    python manage.py syncdb --all

start feed parser crons
    python manage.py runcrons    

This Downloads Feeds from Source page and generates Task1s  Do this as often as you like

## Do Things with App: 
### Important Urls: 

#### Crowdsourcing_sim:
choose an open Task from all open Tasks 
e.g.: http://127.0.0.1:8002/polls/ 	
get Task with <task-id>
e.g.: http://127.0.0.1:8002/polls/5/

#####Interacting with the API

Inspect API of the crowdsourcing simulator

http://127.0.0.1:8002/api/v1/?format=json

Getting the Task List

http://127.0.0.1:8002/api/v1/task/?format=json

Getting an individual Task

http://127.0.0.1:8002/api/v1/task/2/?format=json

#### Sentiment_analisis:
make new Order for sentimentanalysis

e.g.: http://127.0.0.1:8000/makeorder/ 

get Results of Order with <order-id>

e.g.: http://127.0.0.1:8000/makeorder/1/ 

#####Interacting with the API

Inspect API of sentiment analysis

http://127.0.0.1:8000/api/v1/?format=json

Getting a task list

http://127.0.0.1:8000/api/v1/task/?format=json

Get an individual task

http://127.0.0.1:8000/api/v1/task/30/?format=json

#### leave virtualenv
deactivate 

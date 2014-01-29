### Basic UsageOS: Ubuntu

Instructions:

cd DIRECTORY_WHERE_IT_SHOULD_BE
sudo apt-get install python-setuptools

sudo easy_install virtualenv

### create virtual environment:

virtualenv --no-site-packages django

### enter the virtual environment
source django/bin/activate

cd django/

### install django (without sudo becasue already in the virtualenv):

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

cd sentiment_analisis
python manage.py syncdb

### Choose "yes" and choose a Username and Password

cd ../crowdsource_sim
python manage.py syncdb

### Choose "yes" and choose a Username and Password


### Add some initial data to the database
python manage.py sqlcustom polls | ./manage.py dbshell

### start crowdsourcing platform simulator
python manage.py runserver 8002

### Run new terminal: (on every terminal you have to "source django/bin/activate")

### Second Terminal:


cd django/sentiment_analisis/

### start sentiment analysis
python manage.py runserver

### Run new terminal: (on every terminal you have to "source django/bin/activate")

### Third Terminal:

cd django/sentiment_analisis/

python manage.py syncdb --all

### start feed parser crons
python manage.py runcrons    

### This Downloads Feeds from Source page and generates Task1s  Do this as often as you like

### Do Things with App: 
### Important Urls: 

### Crowdsourcing_sim:

127.0.0.1:8002/polls/ 			# --> choose an open Task from all open Tasks 
127.0.0.1:8002/polls/<task-id>/ # --> get Task with <task-id>

### Sentiment_analisis:

127.0.0.1:8000/makeorder 			# --> make new Order for sentimentanalysis
127.0.0.1:8000/makeorder/<order-id>/ 	# --> get Results of Order with <order-id>
 
### leave virtualenv
deactivate 

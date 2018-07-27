# RH Leaves - Leaves managements

### A simple HR web application inspired to bamboo hr

## How To Setup The App Locally

## Prerequisites
- [python3](https://www.python.org/) click this for installing python
- [pip3](https://pypi.python.org/pypi/pip) clikc this for installing pip3
- [virtualenv](https://virtualenv.pypa.io/en/latest/) click this for installing virtualenv
- [postgresql](http://www.postgresql.org/) click this for installing postgresql

## Once all the Prerequisites are installed Initialize the Project
#### 1. Create and Activate a virtualenv
```bash
virtualenv env_name
source env_name/bin/activate Or in windows scrips env_name/bin/activate
```

#### 2. While in the virtualenv Clone the Repository
```
git clone https://github.com/dntech17/hr_soum.git
```

#### 3. cd into the Repo and install dependencies
```
pip install -r requirements.txt
```

#### 4. Create the Postgres User and Database
```
sudo -i -u postgres
createuser --interactive -P
user=hr_soum
password=hr_soum@dntech!@#$

createdb hr_soum_db
```

#### 4. Migrate the Database and Create a Superuser
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 5. Run the Developement Server
```
python manage.py runserver
```

#### 5. Run the Developement Server
if you want to catch the email in your localhost
install [MailDev](http://danfarrelly.nyc/MailDev/)

```
npm install -g maildev
```

and run in your another terminal

```
maildev
```

navigate to `localhost:1080` to see your mail server

## Translate The Application

#### 1. Make sure all HTML strings are wrapped around *{% trans "string" %}*
```
python manage.py makemessages -l fr
```

#### 2. Cd Into locale/fr/LC_MESSAGES
#### 3. Open the django.po file and add your French Translations and Compile
```
python manage.py compilemessages -l fr
```

## Load Initial Data
There are some fixtures files which contain some basic data
one super admin user with email : admin@admin.com with
the default password 1234. <br/>

### Load Fixtures data

| Commands                                              |  Data loaded                                           |
| ------------------------------------------------------|:------------------------------------------------------:|
| `./scripts/data.sh loadtest`                          | this will load test data (fake dafs, fake agencies...) |
| `./scripts/data.sh loadprod`                          | Only load production data (agencies, daf...)           |
| `./scripts/data.sh flush`                             | This command will properly clean the database          |

#### Fake Daf only for test:

| Emails                     |  Passwords       |
| ---------------------------|:----------------:|
| admin@admin.com            | 1234             |
| hr@hr.com                  | 1234             |
| manager@manager.com        | 1234             |
| employe@employe.com        | 1234             |


## Setting cron job to send email
In order to calculate automatically the employe leaves at the end of the month.
set a cron job wich gonna run at the end of every month

`
* * 27-31 * * /scripts/calculate_leave.sh
`
Follow the instruction bellow to set this up in your server :

### 1. Python and Django

make sure your django installation global, if not install it outside of your virtual environment in case you have one.
And make sure you have python3 installer as well

```
python -V
```
if you have something like python 3.6.1 that's great then keep going if not you can upate your python version if you want but this is not mandatory. you just need to have on of the python 3 versions.

### 2. Give execution privillege on the scrip
Give execution privillege to all user by running 
```
sudo chmod +x send_mail.sh
```

### 2. Setting up the cronjob
This process should work on all unix based systems (ubuntu, mac...)

#### 2.1 Edit your crontab
```
crontab -e
```
#### 2.2 Put your command to cronjobs
```
*/02 * * * * cd /Users/UserName/Desktop/Project/Biyassi/script && ./send_mail.sh
```
the path to you project should be global.
then save it and exit crontab.

#### 2.3 test if everything is working
To test if it's working on your system, add a mission and wait 2 minute to get emails in your mail box.

if you don't get any email after 2 minutes, you should try to execute the command directly in your terminal.

Go in `scripts` directory in your project and run this script:

```
./send_mail
```
You can also redirect the output in a log file by running:

```
./send_mail > log.txt
```

Then open the log.txt to see if there is something

##Deployements

Our deployment server is an ubuntu 14.04 (LTS)
the deployment is done with gunicorn and nginx
so if you want to deploy the app in another ubuntu server fisrt of all try to install the required software and dependencies

### install dependancies
1. python3
2. postgres 
3. nginx : `sudo apt-get install nginx`
4. gunicorn : `pip3 install gunicorn`
5. git 


NOTE: if you want to use a virtualenv in your server this one should be done after installing and activating the virtualenv

### setup the server 

In the project folder there is bash file  /scripts/gunicorn.sh which is starting gunicorn in background on the  10.13.15.16:80
you will need to edit this file in order to make it work on your server.


#### Put django DEBUGING to false

Edit your .bashrc file and put the following line at the end of the file

```
export DJANGO_SETTINGS_MODULE=config.prod_settings
``` 

This file /config/prod_setting.py is specially made for production, so change all the variables you want to change from developpement to your production environement.

#### Automatically lunch the app on server startup

if you want the app to be lunched on startup of the server, you should edit the crontab with sudo privilege like this 

```
sudo crontab -e
```

then put inside the following line

```
@reboot kill $(sudo lsof -t -i:80)
@reboot cd /home/smsi/Biyassi/scripts && bash ./gunicorn.sh
```

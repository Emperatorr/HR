#!/bin/sh 
clear

load_initial(){
    python3 manage.py loaddata initial_data.json
}

load_test(){
    python3 manage.py loaddata test_data.json
}
flush_data(){
    python3 manage.py flush --noinput
}
load_production_users(){
    python3 manage.py loaddata production-users.json
}

# defining default param
if [ -z "$1" ]; then
    echo "default action"
	action="loadtest"
else 
    action=$1
fi

# the main part
if [ $action = "flush" ]; then
    echo
    echo "Cleaning the database"
    python3 manage.py flush
elif [ $action = "loadtest" ]; then
    echo
    echo "Clean database and Load Test data into it"
    flush_data &&
    load_initial &&
    load_test
elif [ $action = "loadprod" ]; then
    echo
    echo "Clean database and Load production data into it"
    flush_data &&
    load_initial &&
    load_production_users 
    # this will load admin@admin.com
    # with the password !@#smsi123

#elif [ $action = "loadall" ]; then
#    echo
#    echo "Loading all fixtures data into database"
#    flush_data &&
#    load_test &&
#    load_production_users
fi


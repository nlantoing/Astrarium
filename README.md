# Open solarsystem database #


After many personal projects which involved the solar system and having to get all the different datas I needed by hand I decided to create this project.


The goal is simply to build an SQLite database with a bunch of script to export it in differents formats (mongoDB, XML etc)


### Work in progress ###


### INSTALL ###


Initialize the database :


> python database.py db init
> python database.py db upgrade


### UPGRADE ###


Apply database patches:


> python database.py db upgrade
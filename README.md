# SongCatalog
This is the Item Catalog Application project for the Udacity Full Stack Nanodegree Course.
## About
This project is a RESTfull web application that catalogs songs into categories. The categories can be genres or any other category that a logged in user wants to define. The application allows logged in visters to add, edit, and delete their own categories and songs. Visiters can log in if they have a google+ or facebook account. 

The server side of the application is written in python and uses the flask library. It utilizes Oauth2 to handle secure user logins. It stores the data in a sqlite database using the SQLAlchemy ORM and implements full CRUD operations. The application also has JSON api endpoints for the categories and songs.
## Installing
Install Vagrant http://vagrantup.com and VirtualBox http://www.virtualbox.org.

Clone the fsnd repository from Udacity at GitHub https://github.com/udacity/fullstack-nanodegree-vm.

Go to the FSND-Virtual-Machine/vagrant/catalog directory and clone this repo or download and place zip here.

## Running
From a terminal go to the FSND-Virutual-Machine directory and run - vagrant up; vagrant ssh.

In the vagrant shell go to the vagrant/catalog directory and run - python project.py.

Open a browser window and open a link to http://localhost:8000/categories.
## Accessing JSON endpoints
Adding /JSON to the url for categories or any song link in that category will resturn JSON ouput.

Going to http://localhost:8000/JSON will return output for all categories and songs.

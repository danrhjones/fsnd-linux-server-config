# Item Catalog
Udacity Full Stack - Project 3 (Item Catalog)

## Project Specification

Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. 
Registered users will have the ability to post, edit and delete their own items.

## Prerequisites 

The latest [vagrant](https://github.com/udacity/fullstack-nanodegree-vm.git) build for the Udacity item catalog project. 

## Instructions

1. Start Vagrant
  1. Open Terminal or cmd and browse to the vagrant folder
  2. Type `vagrant up` to started the virtual machine
2. SSH in to the vagrant VM
  1. In the same terminal type `vagrant ssh` to ssh in to the virtual machine
3. Change to the correct folder
  1. Type `cd /vagrant/catalog_app`
4. In order to sign in with a google account, you will need to create a project in https://console.developers.google.com/
  1. Once a project is created you need to generate OAuth ClientId in creditentials. 
  2. Click on ``` download json ``` to download the json file, call it client_secrets.json and store it in your project 
  or paste contents in to existing client_secrets.json
5. in login.html change the client id to:
  `data-clientid = "YOUR_CLIENT_ID"`
6. Run the application
  1. run `catalog_webserver.py`

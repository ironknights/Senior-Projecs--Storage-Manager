# SOLO Storage Manager

Python storage facility utility and database

# Getting Started

## Installation and Running

1. Clone repository and install all dependencies.

2. Install virtualenv if not already installed: `pip install virtualenv`

3. Start virtualenv: `virtualenv venv path/to/repository/venv`

4. Run main module from root of repository: `../Storage-Manager> python main.py`

## Initial Setup and Operation

1. At the login page, click "New" to create a new database (or select "Change" to use an existing one from the repository).

2. Put in the default username and password: User Name: `admin`, Password: `password`. Alternatively you may use the "Default Login" button to enter these two values automatically (note that if you delete or change the default user this button will not let you log in).

3. If you created a new database you will be logged in with no data. To start adding units and/or tenants, use the debug menu to add them.

4. Map creation must be done manually; to test, install a sqlite database browser, such as DB Browser, and add values to database.

# Functionality

The operations that currently work and can be tested are as follows:

## General/Debug

* Login
* Add Unit
* Add Tenant
* Add User
* Add Transaction
* Add History
* Wipe Database (Erases database and builds a new one with default values)

## Operations Tab

* View Unit List
* View Tenant List
* Move In
* Save image to disk
* Make Payment

## Reports Tab

* Load Report
* Export Report

## Tools Tab

### Settings Tab

* Change Default Tab (per user)
* Save Website

### Edit Reports

* Create New Report
* Edit Report

### Edit Rules

* Modify values and save changes
* Locked out of user does not have edit rules permission

## Maps

* Draws Units
* Draws Lines

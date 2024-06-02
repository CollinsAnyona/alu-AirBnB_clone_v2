#AirBnB clone - MySQL
Welcome to the AirBnB Clone project! This project is a simplified version of the popular AirBnB service, implemented with a MySQL database. This README file will guide you through the setup, usage, and structure of the project.

#Description
This project is part of the Holberton School curriculum and serves as an introduction to back-end development with MySQL. The goal is to build a web application similar to AirBnB, which allows users to perform various operations such as creating and managing user accounts, listings, reservations, and reviews.

#Features

*User authentication and management
*CRUD operations for listings, reservations, and reviews
*Search functionality for listings
*Integration with a MySQL database
*RESTful API

#Requirements

*Python 3.8+
*MySQL 8.0+
*Flask
*SQLAlchemy
*Flask-RESTful

#Configure the MySQL database:

*Create a new MySQL Database
CREATE DATABASE airbnb_clone;

#Usage
Once the Flask application is running, you can access the API at http://localhost:5000. Here are some example endpoints:

*User registration:
POST /users
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}

#Contributing
We welcome contributions to this project! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (git checkout -b feature-branch)
3. Make your changes
4. Commit your changes (git commit -m 'Add some feature')
5. Push to the branch (git push origin feature-branch)
6. Open a pull request

#AUTHORS

* BElinda Belange Larose
* Otieno Junior Collins


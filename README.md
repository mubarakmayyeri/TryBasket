# **TryBasket** - eCommerce Platform
This is an eCommerce web application created with Python Django. This website uses PostgreSQL as database and have both user side and admin side functionalities. Users can register, login, view products, manage their profile, checkout and do payments with options like COD, razorpay and paypal. In admin side, there are functionalities like user management, order management, category, subcategory and product management, offer management, dashboard for sales overview and a sales report section for analyzing all sales data.


## Live Demonstration

The E-commerce demo can be viewed online here: https://www.trybasket.shop



## Getting started
To get started you can simply clone this project repository and install the dependencies.

Clone the TryBasket repository using git:
```python
git clone https://github.com/mubarakmayyeri/TryBasket.git
cd TryBasket
```
Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:
```python
(env)$ pip install -r requirement.txt
```
Note the ```(env)``` in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once ```pip``` has finished downloading the dependencies:
```python
(env)$ cd TryBasket
(env)$ python3 manage.py runserver
```
And navigate to ```http://127.0.0.1:8000/```

### Note:
 You will have to create an .env file in the project folder and setup all the environment variables.  
 A sample file (.env-sample) is provided in this repository.


## Tech Stack
* Python
  
* Django
  
* PostgreSQL
  
* Bootstrap

* Ajax
  
* Javascript


<br />
<p align="center">

  <h3 align="center">Cars REST API application</h3>

[![V7.9.3 Python](https://img.shields.io/badge/python-v7.9.3-green)]()  ![](https://img.shields.io/badge/Django-2.1.3-green) [![](https://img.shields.io/badge/postgresql-12-red)]() ![](https://img.shields.io/badge/docker-blue)

This project is made by: <br>
Dominic <strong>Catana</strong><br />
<strong>catanadominic@gmail.com</strong><br>
<strong>+40 723 142 712</strong><br />

#### Prerequisites
0. Install postgresql 12, python 7.9

```
$ git clone https://github.com/Dominiq97/cars-rest-api.git
$ cd cars-rest-api
```
2.a Create python virtual environment and activate it (Windows)
```
$ python -m venv env
$ env\Scripts\activate
```
2.b (Linux, Mac)
```
virtualenv -p python ~/env
source ~/env/bin/activate
```
3. Install the packages
```
pip install -r requirements.txt
```
4. Migrate the database
```
$ (env) python cars-rest-api/manage.py migrate
```
5. Run the server and launch the app on https://127.0.0.1:8000
```
$ (env) python cars-rest-api/manage.py runserver
```

Project Link: [https://github.com/Dominiq97/cars-rest-api](https://github.com/Dominiq97/cars-rest-api)







 

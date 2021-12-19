# README

## Setup

### Requirements
* Python3
* Pandas (for init_db.py)
* Docker

### Create data base
In order to recreate the database from scratch, you must populate a directory called `data` in the root directory of this repo, with the contents of the data directory at https://www.kaggle.com/berkayalan/retail-sales-data

From the root directory, run the init_db.py script:

```$ python init_db.py```


### Steps to run docker rest_app on localhost
Build the docker image by setting your currect directory to the root of this directory (e.g. the location of this README file). Run the following command in your terminal to create the docker
```
docker build --tag rest_app:latest .
```

To run the container you have just created run the following command:
```
docker run -d -p 5000:5000 rest_app
```
This will run your container detached so that you can access the API in your host
browser. You may change the port as you wish.

## Accessing the rest_app

From a browser visit `http://127.0.0.1:5000`

In order to make queries, the get rest endpoint to use is

```
http://127.0.0.1:5000/query/<json-query>
```

e.g.

```
127.0.0.1:5000/query/{"product_id":"P0001","start_date":"2017-01-05","end_date":"2017-02-12"}
```

In order to access the public holiday revenue request, replace `product_id` above with `holidays`

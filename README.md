## User Guide

### How to run

* Build a the docker container image `make build`
* Start the docker container built in the previous step `make start`

The api can be used as follows 

`curl 'http://localhost:8000/ask?q=which%20is%20the%20most%populated%20city%20in%20United%20States'`

or `curl 'http://localhost:8000/ask?q=idontknowanythingaboutit'` which will return 404 and will trigger a model update in the next update interval.

The `score` indicates how relevant a question is to the question provided in the query.

## Dev Guide:

### How it works

* The app is based on the following concepts/algorithms:
    * Tokenizing
    * Bag of words
    * Tf-Idf weighting
    * Self-similarity search using cosine distance
* The main service uses pickled models to start fast and the model is updated every 30 seconds if required.
    * This works with batches of questions. All new questions added between now and the next model update will be inserted into the model.
* The questions dataset used as a baseline was derived from the Stanford Question Answering Dataset (https://rajpurkar.github.io/SQuAD-explorer/)

### Testing

* Run unit tests as follows `make test`

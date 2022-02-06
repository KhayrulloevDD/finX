Given following abc with a method named `query` which accepts keyword arguments for filtering and returns results in a following data structure

[{"first_name": "John", "last_name": "Doe", "email": "john.doe@gmail.com"}]

from abc import ABC, abstractmethod


    class DataSource(ABC):
        @abstractmethod
        def query(self, **kwargs):
            ...

        @property
        @abstractmethod
        def name(self):
            ...

Do the following:

1. Setup a simple Django project using latest LTS version of Django (don't forget to add a custom user model) with multiple databases (you can use sqlite as backend, just define multiple `DATABASES` in settings)
2. Implement a data source based on abc above that performs filtering against django user model in a given database
3. Perform a call using data source against all databases in parallel (up to you how you do it, just add comments explaining why you choose that method, async/multiprocessing/threading/celery (but it may be an overkill))
4. combine results into single data structure that has a data source name in it (and make it read only)


========================================================

Deployment instructions:

* clone https://github.com/KhayrulloevDD/finX.git repository;
* create virtual environment and activate it(optional);
* install dependencies from the requirements.txt file (pip install -r requirements.txt);
* run the server (python manage.py runserver).

Usage instructions:

  * make GET request to {server_domen}/parallel_calls_to_databases?first_name=Melissa&last_name=Doe&email=johndoe@gmail.com&db=db2;

The result of request above will be filtered data from all databases. All parameters are optional. If no parameters passed, result will be all data from all databases.
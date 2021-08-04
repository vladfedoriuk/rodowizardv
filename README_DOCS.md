# rodowizardv

Rodo Wizard 

- ### Set up with pyenv:

    - `pyenv virtualenv 3.9.1 rodowizardv`
    - `pyenv local rodowizardv`
    - `pip install -r requirements.txt`
    - To proceed with running a project using a virtual environment created with the commands above, one will need to create and set up a PostgreSQL database as required by the project's `settings.py` file or change the database configuration in a mentioned file, so it will work with an already created database.
    - `python manage.py migrate`
    - `python manage.py runserver`

- ### Set up with docker-compose:

    - Just perform a `docker-compose up` command in the directory which contains a `docker-compose.yml` file and move forward :)
    - the solution will be available via `127.0.0.1:9071`
    - To access a comand line of the web service: `docker exec -it <container_id> /bin/bash`

- To create a superuser: `python manage.py createsuperuser` (default one is `admin/pass4admin`)
- To run the tests: `python manage.py test`

## Documentation
- After successful logging in to the admin panel and selecting a corresponding Training record, the user will be redirected to a Training editing page, where they can find a button "View on site", which allows to access a RODO form.
- A link that identifies in a unique way a RODO form for a specific training has a template: `/training/<int: year>/<int: month>/<int: day>/<slug: training_slug>`, where *year*, *month*, and *day* stand for the date the training starts and the *training_slug* is predefined by training title, when created via admin panel or needs to be defined manually.
- Having filled the form correctly, the user is shown a dedicated message. In the message the user is asked to check their mail in order to proceed with authentication of the email. On pressing an "OK" button, the User is redirected to the beginning of the form.
- On confirming a mail via pressing a button "here", the user is getting redirected to the page with a message that confirms the successfull confirmation of an email. The confirmation link is unique for every data preserved in the database and it follows this pattern: `confirm/<int:data_id>/`, where *data_id* is an id of the record.

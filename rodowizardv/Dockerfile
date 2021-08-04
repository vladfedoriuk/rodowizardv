# The first instruction is what image we want to base our container on
FROM python:3.9.1

RUN adduser --disabled-password --gecos '' rodowizardv

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# development
ENV DEBUG 1

# environment variables to ensure the database access
ENV PSQL_DATABASE: rodowizardv
ENV PSQL_USER: rodowizardv
ENV PSQL_PASSWORD: pass4rodowizardv
ENV PSQL_HOST database
ENV PSQL_PORT 5432

# update and get the dependencies
RUN apt update
RUN sh -c '/bin/echo -e Y |  apt install gettext'
# create root directory for our project in the container
RUN mkdir /code

# Copy the current directory contents into the container at /code
COPY . /code
RUN chown -R rodowizardv /code

# Copy the entrypoint and grant the user required rights.
COPY ./compose/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown rodowizardv /entrypoint.sh

USER rodowizardv
# Set the working directory to /code
WORKDIR /code

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]

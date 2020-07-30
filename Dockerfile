# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code/src

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y tmux

# command to run on container start
CMD [ "python", "./serverDashboard.py" ] 

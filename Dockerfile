FROM python:3.8-bullseye

RUN pip3 install --no-cache --upgrade pip 

RUN apt-get update && apt-get install -y netcat


COPY Pipfile .
COPY Pipfile.lock .

WORKDIR /app


COPY . /app


RUN pip3 install pipenv

RUN pipenv install --system



# ENTRYPOINT ["entrypoint.sh"]
# CMD ["flask", "run"]
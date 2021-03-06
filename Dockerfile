#FROM heroku/miniconda
FROM continuumio/miniconda3

# Grab requirements.txt.
ADD ./app/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./app /opt/app/
WORKDIR /opt/app

RUN conda install -c estnltk -c conda-forge estnltk

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
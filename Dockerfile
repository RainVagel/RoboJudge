FROM heroku/miniconda

# Grab requirements.txt.
ADD ./app/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./app /opt/app/
WORKDIR /opt/webapp

RUN conda install sqlite

RUN conda create -n tmp python=2.7 enum34=3

RUN conda install python=3.5

RUN conda install -c estnltk -c conda-forge estnltk

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
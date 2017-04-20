FROM gcr.io/google_appengine/python

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt-get install -y curl

# You may later want to change this download as the Cloud SDK version is updated.
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-149.0.0-linux-x86_64.tar.gz | tar xvz
RUN ./google-cloud-sdk/install.sh -q
RUN ./google-cloud-sdk/bin/gcloud components install beta

ADD . /app/
RUN pip install -r requirements.txt
ENV PATH /home/vmagent/app/google-cloud-sdk/bin:$PATH
# CHANGE THIS: Edit the following 3 lines to use your settings.
ENV PROJECT tvlk-recsys-platform
ENV BUCKET tvlk-recsys-storage

EXPOSE 8080
WORKDIR /app

CMD gunicorn -b :$PORT main:app

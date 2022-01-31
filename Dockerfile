
FROM python:3.8
RUN mkdir /projet_data_engeeniring
COPY requirements.txt /projet_data_engeeniring/
RUN pip3 install -r /projet_data_engeeniring/requirements.txt

WORKDIR /projet_data_engeeniring
#COPY . .

ENV FLASK_APP=app
ENV FLASK_DEBUG=1
CMD  ["flask", "run", "--host", "0.0.0.0", "--port", "5000"] 
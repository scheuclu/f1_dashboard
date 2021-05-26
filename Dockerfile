FROM python:3.9
ENV DASH_DEBUG_MODE True # False
LABEL maintainer="scheuclu <scheuclu@gmail.com>"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["python", "./app.py"]
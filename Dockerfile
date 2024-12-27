FROM python:3.10

COPY requirements.txt /app/
RUN pip install -r app/requirements.txt

COPY . /app
WORKDIR app

RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
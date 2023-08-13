FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN useradd --create-home appuser
USER appuser
ENV PORT=8080
CMD ./manage.py migrate &&  gunicorn --workers 3 --bind 0.0.0.0:$PORT centric_app.wsgi

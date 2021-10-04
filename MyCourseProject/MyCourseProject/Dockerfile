FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /MyCourseProject
RUN pip install --upgrade pip
COPY requirements.txt /MyCourseProject/
RUN pip install -r requirements.txt
COPY . /MyCourseProject/
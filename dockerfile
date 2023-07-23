FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /usr/src/simple_blog

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD ["bash", "runserver.sh"]
FROM baseimage

ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /home/app
ADD . /home/app

RUN touch /home/app/logs/access.log
RUN touch /home/app/logs/error.log

EXPOSE 80

CMD ["sh", "cmd.sh"]

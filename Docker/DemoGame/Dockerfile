FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5003
COPY ./DemoGame.py .
CMD [ "python", "./DemoGame.py" ]
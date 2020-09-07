FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5004
COPY ./Stocks.py .
CMD [ "python", "./Stocks.py" ]
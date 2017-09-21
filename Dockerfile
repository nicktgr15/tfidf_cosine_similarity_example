FROM python:3.6

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY pickled_models/* /tmp/

RUN python -c "import nltk; nltk.download('punkt')"

COPY src /src

ENTRYPOINT ["python","/src/api_server.py"]
FROM intermedia/loopbackip

RUN pip install pytest ipython pydevd-pycharm
ADD . /tests

CMD ["pytest", "/tests/"]
From python:3.7.4-slim
RUN pip install flask==1.1.1 redis==3.3.8
WORKDIR /app
COPY ./myapp.py /app
ENTRYPOINT ["python", "myapp.py"]
From python:3.7.5-slim
RUN pip install pytest==5.2.0 requests==2.22.0 selenium==3.141.0
WORKDIR /src
COPY ./test_static.py /src/test_static.py
COPY ./test_selenium.py /src/test_selenium.py
ENV SELENIUM_HUB_HOST 127.0.0.1
ENV SELENIUM_HUB_PORT 4444
ENV WEB_HOST 127.0.0.1
ENV WEB_PORT 80
CMD ["tail", "-f", "/dev/null"]
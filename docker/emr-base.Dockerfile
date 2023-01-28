# reference: https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-docker.html
FROM amazoncorretto:8

ENV PYTHONUNBUFFERED=1
# stop writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN yum -y update; \
    yum -y install yum-utils; \
    yum -y groupinstall development; \
    yum list python3*; \
    yum -y install python3 python3-dev python3-pip python3-virtualenv; \
    pip3 install --upgrade pip; \
    pip3 install numpy pandas; \
    yum -y clean all && rm -rf /var/cache

# RUN python -V
# RUN python3 -V

ENV PYSPARK_DRIVER_PYTHON python3

ENV PYSPARK_PYTHON python3
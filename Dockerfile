FROM amazonlinux:1-with-sources

RUN yum -y install zip gcc gcc-c++ python36 python36-pip python36-virtualenv && yum clean all

RUN python3 -m pip install --upgrade pip && python3 -m pip install boto3


# pdf-lambda-example
A example of how to use camelot-py & pymupdf to parse a pdf file on AWS lambda.

This repo describes how to bundle up and deploy a lambda function which parses
pdf files using python.  This is mainly to serve as a proof of concept for 
packaging up required python dependencies into a layer for use with lambda
functions.

## Architecture

The system comprises:

1. An S3 bucket into which pdf files can be placed as input
2. An Event to trigger the lambda function when a pdf file is created in the S3 bucket.
3. A Lambda function which invokes a python function to parse the pdf
4. A DynamoDB table into which the lambda function can write results.

## Deployment process

### Building the Layer

To deploy a python function with dependencies, they must be bundled up in a 
deployment package;  essentially a zip file containing all the required 
libraries.  This can either be done including the python script to run (as
a full deployment package), or just containing the required libraries (for
use as a layer).

The easiest way to create one of these is to use either an EC2 instance or a 
docker container of the appropriate version, and install the packages in there
before zipping them up.

AWS Lambda functions are deployed on an amazonlinux image; version 1 for python 
versions up to 3.7, version 2 for python versions 3.8 and up.

The Dockerfile in this repo sets up an amazonlinux-1 container with python 3.6.
The create_layer.sh script can then be run in it to install all the required 
packages and creates the zip to use to create a layer.

Run:
`docker build -t lambda1 .`
`docker run -v ${PWD}:/io -it lambda1 /io/create_layer.sh`

### Setup the infrastructure

TODO: describe:

1. Creating up an S3 bucket
2. Creating a DynamoDB table
3. Creating a Lambda layer
4. Creating a Lambda Function
5. Setting up the trigger event.

## TODO

- Add the section on infrastructure setup.
- Rewrite the readme to be more coherant.
- Doodle up an architecture diagram.
- Explain about the 250mb layer limit, and the importance of cleaning it up.

# S3 Immediate Archiver

[![GitHub](https://img.shields.io/github/license/martin-dominguez/immediate-archive-to-s3-ia)](https://github.com/martin-dominguez/immediate-archive-to-s3-ia/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/martin-dominguez/immediate-archive-to-s3-ia)](https://github.com/martin-dominguez/immediate-archive-to-s3-ia/issues)
[![GitHub stars](https://img.shields.io/github/stars/martin-dominguez/immediate-archive-to-s3-ia)](https://github.com/martin-dominguez/immediate-archive-to-s3-ia/stargazers)

This repository contains an AWS Lambda function that allows you to move objects from Amazon S3 Standard storage to the S3 Intelligent-Tiering (S3 IA) storage class without waiting for the 30-day period required by S3 Lifecycle Management.

## Overview

The S3 Lifecycle Management feature allows you to transition objects to different storage classes based on predefined rules. However, when transitioning objects from S3 Standard to S3 IA, there is a minimum 30-day storage period requirement before the transition can occur.

This Lambda function provides a workaround for this limitation by directly copying objects from S3 Standard to S3 IA, bypassing the 30-day waiting period. It can be triggered manually or set up to run on a schedule using AWS CloudWatch Events.

## Prerequisites

- An AWS account with permissions to create and manage Lambda functions, S3 buckets, and CloudWatch Events (if scheduling is required).
- Python 3.7 or later (if you need to modify the Lambda function code).
- (Optional) AWS CLI to deploy CloudFormation template.

## Installation
1. Clone this repository
2. Deploy CloudFormation template in `template.yaml.
   ```bash
   aws cloudformation deploy --stack-name myteststack \
      --template template.yaml
   ```
3. Alternatively, you can use [Application Composer](https://aws.amazon.com/application-composer/).

# Configuration
The Lambda function requires the following parameters in the event that triggers the function:

`bucket_name`: The name of the S3 bucket containing the objects you want to transition to S3 IA.

`prefix` (optional): If the scope of the action is limited to a prefix, this parameter can be used to specify it.

It also requires permissions to get and copy files, so a policy like the following must be added to function's role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>",
                "arn:aws:s3:::<bucket_name>/*"
            ]
        }
    ]
}
```

# Usage
You can invoke the Lambda function manually through the AWS Management Console, AWS CLI, or by triggering it with a CloudWatch Event rule (if scheduled).

The function will copy all objects from the `bucket_name` but storing them in the S3 IA storage class.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

# License
This project is licensed under the Apache v2.0 License.

# video-maker: Serverless Video Maker Service

## Introduction

The `video-maker` service is a serverless application that utilizes AWS Step Functions, Lambda, AWS Bedrock, and AWS S3 to create videos. This guide provides a step-by-step introduction to setting up and deploying the service.

## Prerequisites

- AWS account
- AWS CLI configured with proper credentials
- Serverless Framework installed
- Docker (for packaging Python dependencies)

## Development Guide

1. **Install Dependencies**
   Ensure you have the necessary dependencies installed by running:

   ```sh
   pip install -r requirements.txt
   ```

2. **Create Handler Functions**
   Implement the logic for the functions in the `src` directory:

   - `create_script.py`: Uses AWS Bedrock to generate a script.
   - `create_image.py`: Generates images using AI models and stores them in S3.
   - `create_video.py`: Creates a video from the generated script and images and stores it in S3.

3. **Run Local Tests**
   Test your functions locally before deployment using the Serverless Framework's `invoke local` command:
   ```sh
   serverless invoke local --function createScript
   serverless invoke local --function createImage
   serverless invoke local --function createVideo
   ```

## Deployment Guide

1. **Deploy the Service**
   Deploy your service to AWS using the Serverless Framework:

   ```sh
   serverless deploy --stage dev
   ```

2. **Verify Deployment**
   Verify that the functions and state machine are correctly deployed:

   - Check the AWS Lambda console for the deployed functions.
   - Check the AWS Step Functions console for the state machine.

3. **Invoke State Machine**
   Trigger the state machine execution:
   ```sh
   aws stepfunctions start-execution --state-machine-arn arn:aws:states:<region>:<account-id>:stateMachine:<state-machine-name>
   ```

## Conclusion

This `video-maker` service provides a serverless solution for creating videos using AWS Step Functions, Lambda, AWS Bedrock, and S3. Follow the development and deployment guides to set up and run the service.

For further customization and optimization, refer to the official documentation of the Serverless Framework and AWS services.

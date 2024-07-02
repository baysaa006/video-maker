import json
import boto3
import base64
import logging


s3 = boto3.client('s3')

class ImageError(Exception):
    "Custom exception for errors returned by Amazon Titan Image Generator G1"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_script_handler(event, context):
    images = event.get('images', [])
    audio_file = event.get('audio_file', '')
    text_overlay = event.get('text_overlay', '')
    duration_per_image = event.get('duration_per_image', 3)

    script = f"Script generated from description:\n\n"
    script += f"Text Overlay: {text_overlay}\n\n"
    script += f"Duration per image: {duration_per_image} seconds\n\n"
    script += f"Images:\n"
    for i, image_path in enumerate(images, start=1):
        script += f"{i}. {image_path}\n"

    return {
        "statusCode": 200,
        "script": script
    }

def create_script(event, context):
    print('Event in script::',event)
    # Call the appropriate handler based on the task
    task = event.get('task', '')
    if task == 'create_script':
        return create_script_handler(event, context)
    # Add more handlers for other tasks if needed
    else:
        return {
            "statusCode": 400,
            "error": "Invalid task"
        }

def create_image(event, context):
    print('Event in image::',event)
    model_id = event.get('model_id', '')
    prompt = """A photograph of a cup of coffee from the side."""

    body = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": 0
        }
    })


    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    base64_image = response_body.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Image generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated image with Amazon Titan Image Generator G1 model %s", model_id)


    dynamodb = boto3.resource('dynamodb')

    script =response_body
    table = dynamodb.Table('your_table_name') 
    table.put_item(Item={'script_id': 'your_script_id', 'script': script})

 
    return {
     "statusCode": 200,
     "error": "Invalid task"
    }
    

def create_video(event, context):
    images = event.get('images', [])
    audio_file = event.get('audio_file', '')
    text_overlay = event.get('text_overlay', '')
    duration_per_image = event.get('duration_per_image', 3)

    script = f"Script generated from description:\n\n"
    script += f"Text Overlay: {text_overlay}\n\n"
    script += f"Duration per image: {duration_per_image} seconds\n\n"
    script += f"Images:\n"
    for i, image_path in enumerate(images, start=1):
        script += f"{i}. {image_path}\n"

    dynamodb = boto3.resource('dynamodb')


    table = dynamodb.Table('your_table_name')  
    table.put_item(Item={'script_id': 'your_script_id', 'script': script})

    return {
        "statusCode": 200,
        "script": script
    }
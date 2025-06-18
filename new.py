
# AWS lambda code 

import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    polly = boto3.client('polly')

    # Extract file info from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read the uploaded text file
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = file_obj['Body'].read().decode('utf-8')

    # Convert text to speech using Polly
    response = polly.synthesize_speech(
        Text=file_content,
        OutputFormat='mp3',
        VoiceId='Joanna'  # change if needed
    )

    # Save MP3 back to S3 in the 'audio/' folder
    output_key = f'audio/{key.split('/')[-1].replace('.txt', '.mp3')}"
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=response['AudioStream'].read()
    )

    return {
        'statusCode': 200,
        'body': f'Successfully converted {key} to {output_key}'
    }

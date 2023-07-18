import json
import os

def lambda_handler(event, context):
    # Get the post-deployment script from GitHub.
    post_deployment_script = os.path.join(
        os.path.dirname(__file__), 'post-deploymentscript.sql'
    )

    # Run the post-deployment script.
    with open(post_deployment_script, 'r') as f:
        post_deployment_data = json.load(f)

    for command in post_deployment_data['commands']:
        os.system(command)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Post-deployment script ran successfully'}),
    }
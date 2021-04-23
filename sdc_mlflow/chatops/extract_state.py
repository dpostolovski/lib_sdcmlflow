from googleapiclient import discovery
from googleapiclient import errors
import os
from requests.auth import HTTPBasicAuth
import requests


class Extract_Run:
    def state(self, job_id):
        # Store your full project ID in a variable in the format the API needs.
        project_id = os.environ['GOOGLE_PROJECT_ID']
        # Build a representation of the Cloud ML API.
        ml = discovery.build('ml', 'v1')

        request = ml.projects().jobs().get(name=f'projects/{project_id}/jobs/{job_id}')

        try:
            response = request.execute()
            return response
        except errors.HttpError as err:
            # Something went wrong, print out some information.
            print('There was an error creating the model. Check the details:')
            print(err._get_reason())

    def tracking_run(self, run_id):
        response = requests.get(url=f"{os.environ['MLFLOW_TRACKING_URI']}/api/2.0/mlflow/runs/get",
                                params={'run_id':run_id},
                                auth=HTTPBasicAuth(os.environ['MLFLOW_TRACKING_USERNAME'],
                                                   os.environ['MLFLOW_TRACKING_PASSWORD']))
        json = response.json()

        return {"run_id": run_id,
                "url": f"={os.environ['TRACKING_SERVER_UI']}/#/experiments/{json['run']['info']['experiment_id']}/runs/{run_id}",
                "metrics": json['run']['data']['metrics'],
                "params": json['run']['data']['params']}

import os
from mlflow.tracking import MlflowClient
from mlflow.exceptions import MlflowException, RESOURCE_ALREADY_EXISTS
if __name__ == '__main__':

    client = MlflowClient(tracking_uri=os.environ['MLFLOW_TRACKING_URI'])

    name = "training/sample-model/"
    try:
        experiment_id = client.create_experiment(name)
    except MlflowException as exc:

        if exc.error_code == 'RESOURCE_ALREADY_EXISTS':
            experiment = client.get_experiment_by_name(name)
            experiment_id = experiment.experiment_id

    print(experiment_id)

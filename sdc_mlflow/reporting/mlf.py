import logging

import mlflow
import os
import requests
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient

_MLFLOW_DISABLE_REPORTING = 'MLFLOW_DISABLE_REPORTING'
_MLFLOW_DISABLE_CALLBACK = 'MLFLOW_DISABLE_CALLBACK'
_GITHUB_HEADER_ACCEPT = 'application/vnd.github.v3+json'


def _is_true(env_variable_name):
    return env_variable_name in os.environ and os.environ[env_variable_name] == 'true'

def _get_token():
    pass

def get_secret():
    pass

def callback(uri, data):
    print(f"Callback to: {uri}")
    body = {'inputs': {'google_job_id': '1',
                       'mlflow_job_id': data['mlflow_job_id'],
                       'issue_id': data['issue_id']
                       },
            'ref': data['ref']}

    return requests.post(uri, json=body, headers={'accept': _GITHUB_HEADER_ACCEPT,
                                                  'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'})



def mlflow_disabled_reporting(args):
    return _is_true(_MLFLOW_DISABLE_REPORTING) or args.disable_reporting


def is_callback_disabled():
    return _is_true(_MLFLOW_DISABLE_CALLBACK)


def arguments_processor(parser):
    parser.add_argument(
        '--disable-reporting',
        type=bool,
        default=False),
    if not is_callback_disabled():
        parser.add_argument(
            '--callback-uri',
            type=str,
            default=None),
        parser.add_argument(
            '--ref',
            type=str,
            default=None),
        parser.add_argument(
            '--issue-id',
            type=str,
            default=None)
        parser.add_argument(
            '--job-id',
            type=str,
            default=None
        )
        parser.add_argument(
            '--experiment-name',
            type=str,
            default='0'
        )
    return parser

def _get_exp_id_from_name(name):
    client = MlflowClient(tracking_uri=os.environ['MLFLOW_TRACKING_URI'])

    try:
        experiment_id = client.create_experiment(name)
    except MlflowException as exc:
        if exc.error_code == 'RESOURCE_ALREADY_EXISTS':
            experiment = client.get_experiment_by_name(name)
            experiment_id = experiment.experiment_id

    return experiment_id



class start_run:
    def __init__(self, args):
        self.args = args
        self.run = None
        self.active = None

    def log_metrics(self,metrics):
        for metric, value in metrics.items():
            self.log_metric(metric, value)

    def __getattr__(self,name: str):
        def dummy_method(*args, **kwargs):
            return None

        if name == 'log_metric' or name == 'log_param':
            if not mlflow_disabled_reporting(self.args):
                return getattr(mlflow, name)
            else:
                return dummy_method

    def __enter__(self):
        if mlflow_disabled_reporting(self.args):
            logging.warning("MLFLOW REPORTING DISABLED")
            return self
        else:
            experiment_id = _get_exp_id_from_name(self.args.experiment_name)

            self.active = mlflow.start_run(experiment_id=experiment_id)
            self.active.__enter__()

            self.run = mlflow.active_run()
            print("Active run_id: {}".format(self.run.info.run_id))
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if mlflow_disabled_reporting(self.args):
            return False
        self.active.__exit__(exc_type, exc_val, exc_tb)
        print('after exit')
        if not is_callback_disabled():
            data = {'mlflow_job_id': self.run.info.run_id,
                    'issue_id': self.args.issue_id,
                    'google_job_id': '',
                    'ref': self.args.ref
            }
            print('callback')
            callback(self.args.callback_uri,data)

        return False


def __getattr__(name: str):
    def dummy_method(*args, **kwargs):
        return None

    if name == 'log_metric' or name == 'log_param':
        if not mlflow_disabled_reporting():
            return getattr(mlflow, name)
        else:
            return dummy_method

if __name__ == '__main__':
    client = MlflowClient()


    # Examine the deleted experiment details.
    experiment = client.get_experiment(4)
    print("--")
    print(experiment)

    # Restore the experiment and fetch its info
    client.restore_experiment(2)

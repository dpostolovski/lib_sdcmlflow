from ..chatops.extract_state import Extract_Run
from ..chatops.github import Github
from ..chatops.report_text import Report
import os

if __name__ == '__main__':
    google_job_id = os.environ['GOOGLE_JOB_ID']
    mlflow_job_id = os.environ['MLFLOW_JOB_ID']
    pr = os.environ['PR_ISSUE_ID']

    print(f'PR_ISSUE_ID:{pr}')
    print(f'MLFLOW_JOB_ID:{mlflow_job_id}')
    print(f'MLFLOW_TRACKING_USERNAME:{os.environ["MLFLOW_TRACKING_USERNAME"]}')

    extractor = Extract_Run()
    state = extractor.state(google_job_id)
    run = extractor.tracking_run(mlflow_job_id)
    print(f"text: {run}")


    text = Report().job_run(state, run)
    print(f"text: {text}")

    response = Github().add_comment_in_pr(pr,text)
    print(response.status_code)
    print(response.content)
    assert response.status_code == 201
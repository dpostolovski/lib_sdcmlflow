class Report:
    def job_run(self, state,run, logs=None):
        parameters_text = ""
        metrics_text = ""


        for parameter in run['params']:
            parameters_text+=f"{parameter['key']}: {parameter['value']} \n"

        for metric in run['metrics']:
            metrics_text+=f"{metric['key']}: {metric['value']} \n"

        comment_text = f"JOB ID: [{run['run_id']}]({run['url']}) \n" \
            f"PARAMETERS: \n" \
            f"{parameters_text} \n" \
            f"METRICS: \n" \
            f"{metrics_text} \n"
        return comment_text


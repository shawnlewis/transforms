from wandb.sdk.launch.launch_add import launch_add


class LaunchJob(object):
    def __init__(self, launch_job):
        self._launch_job = launch_job

    def get_result(self):
        self._launch_job.wait_until_running()
        run = self._launch_job.run
        run.wait_until_finished()
        run.load(force=True)
        return run


def launch(uri, run_config):
    return LaunchJob(launch_add(
        uri, {
            "overrides": {
                "args": run_config,
                "run_config": run_config
            }
        }))

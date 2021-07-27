import argparse
import wandb
from wandb.sdk.launch.launch_add import launch_add
import sys


parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact to a given type'

parser.add_argument('--input', type=str, required=True)
parser.add_argument('--target_type', type=str, required=True)


class Transforms(object):
    def __init__(self, api, entity_project):
        # TODO: filter later
        runs = api.runs(entity_project)
        result = []
        for run in runs:
            input_artifact = None
            if run.state != 'finished':
                continue
            if len(run.config) == 1 and 'input' in run.config:
                input_artifact_name = run.config['input']
                for artifact in run.used_artifacts():
                    if artifact.name == input_artifact_name:
                        input_artifact = artifact
            output_artifact = None
            if 'output' in run.summary:
                output_artifact_name = run.summary['output']
                for artifact in run.logged_artifacts():
                    if artifact.name == output_artifact_name:
                        output_artifact = artifact
            if input_artifact is not None and output_artifact is not None:
                result.append((
                    input_artifact.type, output_artifact.type,
                    input_artifact.name, output_artifact.name,
                    run.created_at, run.id))
        self._transforms = result

    def get_equivalent_transforms(self, artifact_name):
        first_order_equivs = [
            t for t in self._transforms if t[2] == artifact_name]
        result = first_order_equivs
        for trans in first_order_equivs:
            for sub in self.get_equivalent_transforms(trans[3]):
                result.append(sub)
        return result

    def get_equivalent_artifacts_of_type(self, artifact_name, target_type):
        equivs = self.get_equivalent_transforms(artifact_name)
        return [t[3] for t in equivs if t[1] == target_type]

    def possible_transforms(self):
        possible = {}
        for transform in self._transforms:
            in_type = transform[0]
            out_type = transform[1]
            run_start = transform[4]
            run_id = transform[5]
            if in_type not in possible:
                possible[in_type] = {}
            in_possible = possible[in_type]
            if out_type not in in_possible:
                in_possible[out_type] = (run_start, run_id)
            out_possible = in_possible[out_type]
            if run_start > out_possible[0]:
                in_possible[out_type] = (run_start, run_id)
        return possible

    def get_type_paths(self, input_type):
        possible = self.possible_transforms()

        def get_paths(path):
            from_type = path[-1]
            if from_type not in possible:
                return []
            to_paths = possible[from_type]
            result = []
            for to_type, (run_start, run_id) in to_paths.items():
                result.append([(from_type, to_type, run_id)])
            for to_type, (run_start, run_id) in to_paths.items():
                if to_type not in path:
                    sub_paths = get_paths(path + [to_type])
                    for sub_path in sub_paths:
                        result.append(
                            [[from_type, to_type, run_id]] + sub_path)
            return result

        return get_paths([input_type])


def print_path(transform_path):
    print(transform_path[0][0], end='')
    for sub_path in transform_path:
        print(' -> [%s] %s' % (sub_path[2], sub_path[1]), end='')
    print()


PROJECT = 'shawn/launch-test2'


def main():
    args = parser.parse_args()
    api = wandb.Api()

    artifact = api.artifact(args.input)
    input_type = artifact.type

    transforms = Transforms(api, PROJECT)
    print('HERE')
    print(transforms._transforms)
    equivalents = transforms.get_equivalent_artifacts_of_type(
        args.input, args.target_type)
    if equivalents:
        print('Equivalent artifact available: %s' % equivalents[0])
        sys.exit(0)

    paths = transforms.get_type_paths(input_type)
    paths_to_target = sorted(paths, key=lambda x: len(x))
    paths_to_target = [p for p in paths if p[-1][1] == args.target_type]
    if paths_to_target:
        # TODO: do transform
        print('Found %s paths to target' % len(paths_to_target))
        for path in paths_to_target:
            print_path(path)
        shortest_path = paths_to_target[0]
        print('Executing:')
        print_path(shortest_path)
        input = args.input
        for transform_run in shortest_path:
            input_type, output_type, run_id = transform_run
            queued_job = launch_add(
                'https://wandb.ai/%s/runs/%s' % (PROJECT, run_id), {
                    "overrides": {
                        "run_config": {
                            "input": input
                        }
                    }
                })
            queued_job.wait_until_running()
            run = queued_job.run
            run.wait_until_finished()
            input = input.split(':')[0] + '-' + output_type

    else:
        available_types = [input_type] + list(set(p[-1][1] for p in paths))
        print('No paths to target type found')
        print('Available paths:')
        for path in paths:
            print_path(path)
        print()
        print('Please create and run a transform from one these types: %s' %
              available_types)
        print('  to the target type: %s' % args.target_type)


if __name__ == '__main__':
    main()

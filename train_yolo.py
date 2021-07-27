import argparse
import random
import os
import tempfile
import wandb


parser = argparse.ArgumentParser()
parser.description = 'Train a model on a dataset'
parser.add_argument('--input_dataset', type=str, required=True)
parser.add_argument('--sweep_id', type=str)
parser.add_argument('--input_model', type=str)
parser.add_argument('--learning_rate', type=float, required=True)
parser.add_argument('--momentum', type=float, required=True)

INPUT_DATASET_TYPE = 'yolo-dataset'


def main():
    args = parser.parse_args()
    with wandb.init(config=args, job_type='train-yolo') as run:
        artifact = run.use_artifact(run.config.input_dataset)
        if artifact.type != INPUT_DATASET_TYPE:
            raise 'input_artifact type must be: %s' % INPUT_DATASET_TYPE
        if args.input_model:
            run.use_artifact(args.input_model)
        # input_dir = artifact.download()
        with tempfile.TemporaryDirectory() as output_dir:
            open(os.path.join(output_dir, 'file.txt'),
                 'w').write('%s' % random.random())
            output_artifact = wandb.Artifact(
                name=run.id + '-' + 'model', type='model')
            output_artifact.add_dir(output_dir)
            server_artifact = run.log_artifact(output_artifact)
            server_artifact.wait()
            run.summary['output'] = server_artifact.name
            run.log({'acc': random.random()})


if __name__ == '__main__':
    main()

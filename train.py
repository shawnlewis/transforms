import argparse
import random
import os
import tempfile
import wandb


parser = argparse.ArgumentParser()
parser.description = 'Train a model on a dataset'
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--learning_rate', type=float, required=True)
parser.add_argument('--momentum', type=float, required=True)


def main():
    args = parser.parse_args()
    with wandb.init(config=args, job_type='train') as run:
        artifact = run.use_artifact(run.config.input)
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
            run.summary['acc'] = random.random()


if __name__ == '__main__':
    main()

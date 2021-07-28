import argparse
import random
import os
import tempfile
import wandb


parser = argparse.ArgumentParser()
parser.description = 'Train a model on a dataset'
# parser.add_argument('--input_dataset', type=str, required=True)
parser.add_argument('--input_model', type=str, required=True)

INPUT_DATASET_TYPE = 'yolo-dataset'


def main():
    args = parser.parse_args()
    with wandb.init(config=args, job_type='eval-yolo') as run:
        if args.input_model:
            run.use_artifact(args.input_model)
        run.summary['output'] = random.random()


if __name__ == '__main__':
    main()

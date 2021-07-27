import argparse
import random
import wandb
from launch import launch


parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact to a given type'

parser.add_argument('--template_uri', type=str, required=True)
parser.add_argument('--input_dataset', type=str, required=True)


PROJECT = 'shawn/launch-test2'
NUM_GENS = 3
JOBS_PER_GEN = 2


def main():
    args = parser.parse_args()

    input_model = None
    for gen in range(NUM_GENS):
        # launch a generation and wait for results
        run_config = {
            'input_dataset': args.input_dataset,
            'learning_rate': random.random(),
            'momentum': random.random()
        }
        if input_model:
            run_config['input_model'] = input_model
        jobs = [launch(args.template_uri, run_config)
                for j in range(JOBS_PER_GEN)]
        results = [j.get_result() for j in jobs]

        # use the best model from this gen as input to
        # next gen
        best_acc = -1
        best_run = None
        for run in results:
            if run['acc'] > best_acc:
                best_run = run
        input_model = best_run['output']


if __name__ == '__main__':
    main()

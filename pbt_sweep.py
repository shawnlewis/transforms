import argparse
import random
import wandb
from launch import launch


parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact to a given type'

parser.add_argument('--template_uri', type=str, required=True)
parser.add_argument('--input_dataset', type=str, required=True)


NUM_GENS = 5
JOBS_PER_GEN = 3
BEST_N_MODELS = 3


def best_n_runs(runs, n):
    return sorted(runs, key=lambda x: x['acc'])[-n]


def main():
    args = parser.parse_args()

    all_runs = []
    for gen in range(NUM_GENS):
        best_n_runs = sorted(
            all_runs, key=lambda r: r.summary['acc'])[-BEST_N_MODELS:]
        # launch a generation and wait for results
        jobs = []
        for j in range(JOBS_PER_GEN):
            run_config = {
                'input_dataset': args.input_dataset,
                'learning_rate': random.random(),
                'momentum': random.random()
            }
            if best_n_runs:
                run_config['input_model'] = random.choice(
                    best_n_runs).summary['output']
            jobs.append(launch(args.template_uri, run_config))
        all_runs += [j.get_result() for j in jobs]


if __name__ == '__main__':
    main()

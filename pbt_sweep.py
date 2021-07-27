import argparse
import string
import random
import wandb
from launch import launch


parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact to a given type'

parser.add_argument('--template_uri', type=str, required=True)
parser.add_argument('--input_dataset', type=str, required=True)
parser.add_argument('--num_gens', type=int, default=5, required=True)
parser.add_argument('--jobs_per_gen', type=int, default=3, required=True)
parser.add_argument('--best_n_models', type=int, default=3, required=True)


def best_n_runs(runs, n):
    return sorted(runs, key=lambda x: x['acc'])[-n]


def main():
    args = parser.parse_args()
    run = wandb.init(config=args, job_type='pbt_sweep')
    sweep_id = ''.join(random.choice(string.ascii_lowercase)
                       for i in range(9))
    print('sweep_id:', sweep_id)

    all_runs = []
    n = 0
    for gen in range(run.config.num_gens):
        print('Generation', gen)
        best_n_runs = sorted(
            all_runs, key=lambda r: r.summary['acc'])[-run.config.best_n_models:]
        # launch a generation
        jobs = []
        for j in range(run.config.jobs_per_gen):
            n += 1
            run_config = {
                'sweep_id': sweep_id,
                'input_dataset': args.input_dataset,
                'learning_rate': random.random(),
                'momentum': random.random()
            }
            if best_n_runs:
                run_config['input_model'] = random.choice(
                    best_n_runs).summary['output']
            jobs.append(launch(args.template_uri, run_config))
        # wait for results
        all_runs += [j.get_result() for j in jobs]
        # log status
        wandb.log({'generation': gen, 'total_jobs': n,
                  'best_acc': max(r.summary['acc'] for r in all_runs)})

    top_run = sorted(
        all_runs, key=lambda r: r.summary['acc'])[-1]
    run['output'] = top_run
    run['sweep_id'] = sweep_id


if __name__ == '__main__':
    main()

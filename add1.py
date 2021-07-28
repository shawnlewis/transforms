import argparse
import wandb

parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact'
parser.add_argument('--input', type=float, required=True)

args = parser.parse_args()
with wandb.init(job_type='add1', config=args) as run:
    run.summary['output'] = run.config['input'] + 1

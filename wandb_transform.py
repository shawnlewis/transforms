import argparse
import os
import tempfile
import wandb


parser = argparse.ArgumentParser()
parser.description = 'Transform an artifact'
parser.add_argument('--input', type=str, required=True)


def transform(input_dir, output_dir):
    in_file = open(os.path.join(input_dir, 'file.txt'))
    val = int(in_file.read().strip())
    out_file = open(os.path.join(output_dir, 'file.txt'), 'w')
    out_file.write('%s' % (val + 2))


def transform_files_main(input_type, output_type, files_transform_callback):
    args = parser.parse_args()
    with wandb.init(config=args, job_type='transform-%s-to-%s' % (input_type, output_type)) as run:
        artifact = run.use_artifact(run.config.input)
        if artifact.type != input_type:
            raise 'input_artifact type must be: %s' % input_type
        input_dir = artifact.download()
        with tempfile.TemporaryDirectory() as output_dir:
            files_transform_callback(input_dir, output_dir)
            output_artifact = wandb.Artifact(
                type=output_type, name=artifact.name.split(':')[0] + '-' + output_type)
            output_artifact.add_dir(output_dir)
            server_artifact = run.log_artifact(output_artifact)
            server_artifact.wait()
            run.summary['output'] = server_artifact.name

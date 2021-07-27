import os
import wandb_transform


def transform(input_dir, output_dir):
    in_file = open(os.path.join(input_dir, 'file.txt'))
    val = int(in_file.read().strip())
    out_file = open(os.path.join(output_dir, 'file.txt'), 'w')
    out_file.write('%s' % (val * 11))


if __name__ == '__main__':
    wandb_transform.transform_files_main('x', 'y', transform)

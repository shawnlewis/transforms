import os
import wandb_transform


def transform(input_dir, output_dir):
    f = open(os.path.join(input_dir, 'file.txt'))
    num = int(f.read().strip())
    open(os.path.join(output_dir, 'file.txt'), 'w').write('%s' % (num + 2))


if __name__ == '__main__':
    wandb_transform.transform_files_main(
        'coco-dataset', 'wandb-dataset', transform)

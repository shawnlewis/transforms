import wandb_transform


def transform(input_dir, output_dir):
    # your transform code here
    pass


if __name__ == '__main__':
    wandb_transform.transform_files_main(
        '%%INPUT_TYPE%%', '%%OUTPUT_TYPE%%', transform)

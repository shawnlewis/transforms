Generic initialization for demo

```
sh init_project.sh
```

Custom initializations. Update template_uri and input_model specifically for
your new project.

```
python pbt_sweep.py \
  --template_uri=https://wandb.ai/shawn/launch-demo7/runs/3aeeywbw \
  --input_dataset=yolo-dataset1:v0 \
  --num_gens=1 \
  --jobs_per_gen=1 \
  --best_n_models=1
python eval_yolo.py --input_model=1wp25rsj-model:v0
```

Run three launch-agents for your project:

```
wandb launch-agent <project_name>
```

First, try to transform data into yolo format

launch spec in UI:

```
{
  "overrides": {
    "args": {
      "input": "coco-dataset2:v0",
      "target_type": "yolo-dataset"
    }
  }
}
```

This will fail, we need a valid transform.

Run this on local machine:
python transform-wandb-to-yolo.py --input=coco-dataset1-wandb-dataset:v0

Then run the above transform again. Great

Then launch a sweep (replace template_uri here):

launch spec in UI:

```
{
  "overrides": {
    "args": {
      "template_uri": "https://wandb.ai/shawn/launch-demo7/runs/3aeeywbw",
      "input_dataset": "coco-dataset2-wandb-dataset-yolo-dataset:v0",
      "num_gens": "5",
      "jobs_per_gen": "3",
      "best_n_models": "3"
    }
  }
}
```

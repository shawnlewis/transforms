```
sh init_project.sh
python pbt_sweep.py \
  --template_uri=https://wandb.ai/shawn/launch-test4/runs/wfpru048  \
  --input_dataset=yolo-dataset1:v0 \
  --num_gens=1 \
  --jobs_per_gen=1 \
  --best_n_models=1
```

ENTITY=$1
PROJECT=$2
wandb init -e $1 -p $2

cd test_artifacts
wandb artifact put -t coco-dataset -n $2/coco-dataset1 coco-dataset1
wandb artifact put -t coco-dataset -n $2/coco-dataset2 coco-dataset2
wandb artifact put -t coco-dataset -n $2/coco-dataset3 coco-dataset3
wandb artifact put -t yolo-dataset -n $2/yolo-dataset1 yolo-dataset1
cd ..

python transform-coco-to-wandb.py --input=coco-dataset1:v0
python transform.py --input=coco-dataset1:v1 --target_type=wandb

python train.py --input_dataset=yolo-dataset1 --learning_rate=0.1 --momentum=0.9
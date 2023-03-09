# Speaker-Verification-task3

## How to launch 
1. Docker container
```
cd Speaker-Verification/task3
docker build . -t speaker_verification:0.0
docker run -d --cpuset-cpus 128-255 --gpus '"device=4,5,6,7"' -v /raid/madina_abdrakhmanova/datasets/sf_pv:/workdir/sf_pv --name sv_task3 speaker_verification:0.0
docker exec -it sv_task3 /bin/bash
```
2. train 
```
python issai_task_3_train.py
```

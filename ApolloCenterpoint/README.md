## Hardware
Lidar:
Livox-Hap
Livox three-wire aviation connector
Converter

Computer: 
Alienware

## Create a virtual environment
conda create -n paddle_env python=3.8

## Activate the conda virtual environment
conda activate paddle_env

## (Optional) Add Tsinghua mirrors for users in China
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

## Install the GPU version of PaddlePaddle
## For CUDA 11.7, requires cuDNN 8.4.1 (NCCL >= 2.7 for multi-GPU environments)
conda install paddlepaddle-gpu==2.4.1 cudatoolkit=11.7 \
  -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ \
  -c conda-forge

## Clone the apollo-model-centerpoint repository
## Skip this step if you've already downloaded the source code
git clone https://github.com/ApolloAuto/apollo-model-centerpoint.git

## Install the dependencies
cd apollo-model-centerpoint
pip install -r requirements.txt

## Install apollo-model-centerpoint in editable mode
pip install -e .

## deply the model in python
cd deploy/centerpoint/python

python infer.py --model_file path to your model
--params_file path to your parameters --lidar_file path to your point cloud file --num_point_dim 4

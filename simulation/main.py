
#! conda install yaml
import numpy as np
import yaml

with open("simulation/config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile,Loader=yaml.FullLoader)


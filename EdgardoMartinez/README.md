# Sonic controller using pygame for open-ai retro.

To use this script you must setup a ***python 3 enviroment*** with the following command:

```
virtualenv -p python3  env
source env/bin/activate
pip3 install gym-retro
pip3 install opencv-python
pip3 install pygame
pip3 install imutils
mkdir roms
```

Download the md Genesis from **some place in the internet** and place it in the roms folder.
Execute ```python3 -m retro.import roms``` to import the game o retro open-ai.

Execute the extract the data, this method is **pretty slow** because store the information in a file for every step, is intent to be used just for a prove of concept.





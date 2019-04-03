import os
from shutil import copy, move
import pandas as pd

csv = './nexet_diffs.csv'
datadir = '/mnt/w/prj/data/nexet/nexet_2017_1/trainA'

df = pd.read_csv(csv, sep=',', encoding='utf8', skipinitialspace=True)

if not os.path.isdir(datadir + '/dismatch'):
    os.mkdir(datadir + '/dismatch')
if not os.path.isdir(datadir + '/dismatch/day'):
    os.mkdir(datadir + '/dismatch/day')
if not os.path.isdir(datadir + '/dismatch/night'):
    os.mkdir(datadir + '/dismatch/night')
if not os.path.isdir(datadir + '/dismatch/twilight'):
    os.mkdir(datadir + '/dismatch/twilight')

num_all = len(df)
already_processed = 0
for r, _, f in os.walk(datadir + '/dismatch'):
    print(r, len(f))
    already_processed += len(f)
print('Already processed:', already_processed)
with open('log.txt', 'a', encoding="utf-8") as log:
    print(f'---- start log ----', file=log)
    for r, d, f in os.walk(datadir):
        for i, file in enumerate(f):
            if file.endswith('.jpg') and df.image_filename.str.contains(file).any():
                row = df.loc[df.image_filename == file]
                dst = f'{datadir}/dismatch/{str(row.lighting_now.values[0]).lower()}/{file}'
                df = df[~df.image_filename.str.contains(file)]
                print(f'{num_all - len(df)} processed', end='\r')
                if not os.path.exists(dst):
                    lwas = str(row.lighting_was.values[0]).lower()
                    lnow = row.lighting_now.values[0]
                    print(f'{file[:-4]}\t{lwas}->{lnow} [{row.pixels_light.values[0]}]', file=log)
                    src = os.path.join(r, file)
                    move(src, dst)

print(f'{num_all - len(df)} moved! {len(df)} last')

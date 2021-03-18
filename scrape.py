import os

with open('input.csv') as f:
  names = [x.strip().replace(' ', '_') for x in next(f).split(',')[1:]]
  for i, line in enumerate(f):
    for j, url in enumerate(line.split(',')[1:]):
      if url != '':
        url = url.strip()
        os.system(f'curl -sL {url} --output {names[j]}_{i}.png')

os.system('find . -name "*.png" -size -4200c -delete')

for name in names:
  os.system(f'zip -q  {name}.zip {name}_* > /dev/null 2>&1')
os.system('rm *.png')

os.system(f'zip -q  WarmAndFuzzies.zip *.zip  > /dev/null 2>&1')

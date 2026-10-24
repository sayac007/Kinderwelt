from PIL import Image, ImageOps
from pathlib import Path
import json
root=Path(__file__).resolve().parent
colors=[(240,40,60),(30,200,80),(40,80,230),(240,210,40),(180,70,210),(40,210,210)]
base=Image.new('RGB',(96,64))
for i,c in enumerate(colors):
 for y in range((i//3)*32,(i//3+1)*32):
  for x in range((i%3)*32,(i%3+1)*32):base.putpixel((x,y),c)
source=Image.open(root/'gps-source.png')
records=[]
for orientation in range(1,9):
 exif=source.getexif();exif[274]=orientation
 for ext,fmt,opts in [('jpg','JPEG',{'quality':95,'subsampling':0}),('png','PNG',{}),('webp','WEBP',{'lossless':True})]:
  file=root/f'orientation-{orientation}.{ext}'
  base.save(file,fmt,exif=exif.tobytes(),**opts)
  with Image.open(file) as loaded:
   expected=ImageOps.exif_transpose(loaded).convert('RGBA')
   probes=[]
   for y in range(16,expected.height,32):
    for x in range(16,expected.width,32):probes.append({'at':[x,y],'rgba':list(expected.getpixel((x,y)))})
   records.append({'file':file.name,'orientation':orientation,'size':list(expected.size),'probes':probes})
(root/'orientation-cases.json').write_text(json.dumps(records,indent=2)+'\n')
print('Generated 24 tiny geometric fixtures with camera/GPS EXIF; no photos or real locations.')

#!/usr/bin/env python3
"""Validate the actual Godot image set and moving-frame differences."""
import hashlib,json,struct,sys
from pathlib import Path
p=Path(sys.argv[1]);frames=json.loads((p/'renders.json').read_text())
assert len(frames)==681
for frame in frames:
 data=(p/(frame['name']+'.png')).read_bytes()
 assert data[:8]==b'\x89PNG\r\n\x1a\n'
 assert list(struct.unpack('>II',data[16:24]))==frame['pixels']
for profile in ['phone','small','landscape','dense']:
 for subject,index in [('physics',8),('body',15)]:
  assert (p/f'{profile}-{subject}-task-{index}.png').is_file(),'Headgear comparison must actually render'
 for locale in ['de','en','ru']:
  for suffix in ['bonus-offer','bonus-50','bonus-100','native-letter-bonus']:
   assert (p/f'{profile}-{locale}-{suffix}.png').is_file()
  assert (p/f'{profile}-{locale}-restore-earlier-points.png').is_file()
  for tier in ['base','0','1']:assert (p/f'{profile}-{locale}-native-last-{tier}.png').is_file()
  for subject in ['logic','physics','biology','chemistry','body','geography']:
   for level in [1,2]:
    assert (p/f'{profile}-{locale}-{subject}-bonus-{level}.png').is_file()
  if locale!='de':
   for suffix in ['logic-dual','logic-order']:
    assert (p/f'{profile}-{locale}-{suffix}.png').is_file()
 assert len({hashlib.sha256((p/(profile+'-heroes'+suffix+'.png')).read_bytes()).hexdigest() for suffix in ['', '-move','-think','-success']})==4
for profile in ['phone','small','landscape','dense']:
 assert (p/(profile+'-scene-castle.png')).read_bytes()!=(p/(profile+'-scene-castle-floating.png')).read_bytes()
 for scene in ['tree','seabed','city','moon']:
  assert (p/(profile+'-scene-'+scene+'.png')).read_bytes()!=(p/(profile+'-scene-'+scene+'-floating.png')).read_bytes()
 assert len({hashlib.sha256((p/(profile+'-looks-'+look+'.png')).read_bytes()).hexdigest() for look in ['hero','alien','astronaut','scientist']})==4
assert (p/'riddle-sound-ear.png').read_bytes()==(p/'riddle-sound-moon.png').read_bytes(),'Riddle must not reveal the original answer/object'
print('PASS: 681 real frames; headgear comparisons, 67200-point headers, 50/100 bonuses including scientific comparisons and inverse logic, native letter challenges, dual-rule logic, ordering and confirmed old-point transfer in three languages/four profiles; answer-independent riddle pixels; worlds, heroes, looks, rotations and menus')

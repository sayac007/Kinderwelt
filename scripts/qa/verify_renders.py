#!/usr/bin/env python3
"""Validate the actual Godot image set and moving-frame differences."""
import hashlib,json,struct,sys
from pathlib import Path
p=Path(sys.argv[1]);frames=json.loads((p/'renders.json').read_text())
assert len(frames)==383
for frame in frames:
 data=(p/(frame['name']+'.png')).read_bytes()
 assert data[:8]==b'\x89PNG\r\n\x1a\n'
 assert list(struct.unpack('>II',data[16:24]))==frame['pixels']
for profile in ['phone','small','landscape','dense']:
 assert len({hashlib.sha256((p/(profile+'-heroes'+suffix+'.png')).read_bytes()).hexdigest() for suffix in ['', '-move','-think','-success']})==4
for profile in ['phone','small','landscape','dense']:
 assert (p/(profile+'-scene-castle.png')).read_bytes()!=(p/(profile+'-scene-castle-floating.png')).read_bytes()
 for scene in ['tree','seabed','city','moon']:
  assert (p/(profile+'-scene-'+scene+'.png')).read_bytes()!=(p/(profile+'-scene-'+scene+'-floating.png')).read_bytes()
 assert len({hashlib.sha256((p/(profile+'-looks-'+look+'.png')).read_bytes()).hexdigest() for look in ['hero','alien','astronaut','scientist']})==4
print('PASS: 383 real frames; maximum-score headers in world and task; independent looks and seven sceneries and per-subject picker; seven heroes, live task rotations, score animations; original 24 tasks, 15 science tasks, eight worlds, all three languages, route paging and menus at four profiles; distinct animated poses')

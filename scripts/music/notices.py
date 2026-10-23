#!/usr/bin/env python3
"""Reproduce accurate arrangement notices without changing licence assertions."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def arrangement(track):
    source=track['source']['file']
    common=f'Eigene Grand-Piano-Wiedergabe der Vorlage {source}.'
    if track['kind']=='lilypond_wiener':
        return common+' Walzerauszug aus vier Stimmen (Melodie, zweite Melodie, linke Hand, Pedal); MIDI-Score ergänzt; Vierteltempo von 200 auf 180 gesetzt.'
    if track['kind']=='midi':
        return common+f' MIDI-Zeitabstände mit Faktor {track.get("time_scale",1):g} skaliert; keine LilyPond-Konvertierung.'
    return common+' Notensatz und angegebene Include-Dateien per convert-ly für LilyPond 2.24.4 aufbereitet; reine Gravureinstellungen ohne Klangwirkung entfernt, soweit vorhanden.'
def render_notices():
    tracks=json.loads((ROOT/'scripts/music/catalog.json').read_text())['tracks']
    # The exact original legal assertions/URLs are a separately pinned fixture.
    licences=json.loads((ROOT/'scripts/music/notice-license-fixtures.json').read_text())
    assert len(tracks)==len(licences)==20
    lines=['Kinderwelt: 20 eigene Klavierwiedergaben klassischer Kompositionen.','Wiener Blut und O mio babbino caro sind Themenauszüge. Die anderen Titel sind Klavierfassungen der jeweiligen Noten-/MIDI-Ausgabe; keine fremden Orchesteraufnahmen.','GeneralUser GS 2.0.3: S. Christian Collins; Lizenz siehe licenses/GeneralUser-GS.txt.','Die Auswahl ist eine kuratierte Sammlung, keine objektive Rangliste.','']
    for t,lic in zip(tracks,licences):
        assert lic.startswith('Lizenz: '+t['license']+' · ')
        src=t['source'];url=src['repository'].removesuffix('.git')+'/blob/'+src['commit']+'/'+src['path']
        lines.extend([t['composer']+': '+t['title'],t['arranger'],lic,'Quelle: '+url,'Bearbeitung: '+arrangement(t)])
        if t.get('attribution_note'):lines.append(t['attribution_note'])
        lines.append('')
    return '\n'.join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=ROOT/'assets/music/NOTICES.txt';value=render_notices()
    if a.check:
        if path.read_text()!=value:raise SystemExit('Music notices are stale')
    else:path.write_text(value)
    print('Music notices: 20 distinct source arrangements; licence lines unchanged')
if __name__=='__main__':main()

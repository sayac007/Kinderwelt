#!/usr/bin/env python3
"""Reproduce accurate arrangement notices without changing licence assertions."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def recording_terms(track):
    """Propagate only the already selected source's same-version ShareAlike."""
    match=re.fullmatch(r'CC-BY-SA-([0-9]+\.[0-9]+)',track['license'])
    if not match and track['license'].startswith('CC-BY-SA-'):
        raise ValueError('Unsupported ShareAlike version; do not silently omit the recording notice')
    if not match:return None
    license=track['license'];url='https://creativecommons.org/licenses/by-sa/'+match[1]+'/'
    return {'license':license,'url':url,'notices':{
        'de':f'Die Aufnahme in dieser App steht ebenfalls unter {license}: {url}',
        'en':f'The recording in this app is also licensed under {license}: {url}',
        'ru':f'Запись в этом приложении также распространяется по лицензии {license}: {url}'}}

def with_recording_terms(track,license_url):
    data=track.copy();data['license_url']=license_url
    terms=recording_terms(track)
    if terms and terms['url']!=license_url:raise ValueError('Recording licence URL differs from the source version')
    if terms:data['recording_license']=terms
    else:data.pop('recording_license',None)
    return data

def license_urls():
    tracks=json.loads((ROOT/'scripts/music/catalog.json').read_text())['tracks']
    licences=json.loads((ROOT/'scripts/music/notice-license-fixtures.json').read_text())
    assert len(tracks)==len(licences)==20
    for t,lic in zip(tracks,licences):assert lic.startswith('Lizenz: '+t['license']+' · ')
    return {t['id']:lic.split(' · ',1)[1] for t,lic in zip(tracks,licences)}

def manifest_notices():
    data=json.loads((ROOT/'assets/music/manifest.json').read_text())
    tracks=json.loads((ROOT/'scripts/music/catalog.json').read_text())['tracks'];urls=license_urls()
    assert [t['id'] for t in data['tracks']]==[t['id'] for t in tracks],'Music catalogue order differs'
    for actual,source in zip(data['tracks'],tracks):
        assert actual['license']==source['license'],'Music source licence drift'
    data['tracks']=[with_recording_terms(t,urls[t['id']]) for t in data['tracks']]
    return json.dumps(data,ensure_ascii=False,indent=2)+'\n'

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
        recording=recording_terms(t)
        if recording:lines.append(recording['notices']['de'])
        if t.get('attribution_note'):lines.append(t['attribution_note'])
        lines.append('')
    return '\n'.join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();path=ROOT/'assets/music/NOTICES.txt';value=render_notices()
    manifest=ROOT/'assets/music/manifest.json';expected=manifest_notices()
    if a.check:
        if path.read_text()!=value:raise SystemExit('Music notices are stale')
        if manifest.read_text()!=expected:raise SystemExit('Music recording licence metadata is stale')
    else:path.write_text(value);manifest.write_text(expected)
    print('Music notices: 20 source arrangements; source licences preserved; same-version recording notices checked')
if __name__=='__main__':main()

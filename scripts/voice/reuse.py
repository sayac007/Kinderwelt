"""Reuse an unchanged utterance only with proof of the exact original model input.

This is a later lexical review, never a claim that old audio was regenerated.
Original generation parameters, seeds and waveform hashes remain unchanged.
"""
import hashlib,json
import pronunciation

def reviewed_current_rows(previous,texts,locale):
    wanted=set(texts.values())
    # Retired text may contain words deliberately absent from the new finite
    # vocabulary. Do not attempt to review or reuse an obsolete utterance.
    return {r['text']:r for r in previous['clips'] if r['text'] in wanted and r.get('pronunciation')==pronunciation.utterance(r['text'],locale)}

def reviewed_piper_row(original,current,previous,expected,manifest_sha256):
    """Keep an existing take only if the actual phonemes and settings agree."""
    if previous.get('locale')!='en' or expected.get('locale')!='en':return None
    for key in ['model','model_sha256','voice_gender']:
        if not previous.get(key) or previous[key]!=expected.get(key):return None
    if original['text']!=current['text']:return None
    before=[u['phonemes'] for u in original.get('phonetic_units',[])]
    after=[u['phonemes'] for u in current.get('phonetic_units',[])]
    if not before or before!=after:return None
    parameters=['length_scale','noise_scale','noise_w_scale','volume','lead_seconds','tail_seconds','sentence_pause_seconds']
    if any(original['generation_profile'].get(k)!=current['generation_profile'].get(k) for k in parameters):return None
    guidance=pronunciation.utterance(current['text'],'en')
    if current.get('pronunciation')!=guidance:return None
    row=dict(original,pronunciation=guidance)
    row['pronunciation_review']={'policy':'Later lexical review; original phonemes and synthesis settings verified equal; not regenerated',
                                'original_manifest_sha256':manifest_sha256,'reviewed_generation_profile':current['generation_profile']}
    return row

def exact_input_rows(previous,expected,texts,locale,manifest_sha256):
    identity=['model_sha256','speech_tokenizer_sha256','model_revision','speaker','locale']
    if any(not previous.get(k) or previous.get(k)!=expected.get(k) for k in identity):return {}
    batches=previous.get('generation_batches',{});wanted=set(texts.values());rows={}
    for original in previous['clips']:
        text=original['text']
        if text not in wanted:continue
        batch=batches.get(original.get('generation_batch_sha256'))
        if not batch:continue
        if hashlib.sha256(json.dumps(batch,ensure_ascii=False).encode()).hexdigest()!=original['generation_batch_sha256']:continue
        guidance=pronunciation.utterance(text,locale)
        if guidance['synthesis_text'] not in batch:continue
        row=dict(original)
        row['pronunciation']=guidance
        row['pronunciation_review']={'policy':'Later lexical review; exact original model input verified; not regenerated',
                                     'original_manifest_sha256':manifest_sha256}
        rows[text]=row
    return rows

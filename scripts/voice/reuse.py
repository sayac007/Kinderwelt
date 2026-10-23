"""Reuse an unchanged utterance only with proof of the exact original model input.

This is a later lexical review, never a claim that old audio was regenerated.
Original generation parameters, seeds and waveform hashes remain unchanged.
"""
import hashlib,json
import pronunciation

def exact_input_rows(previous,expected,texts,locale,manifest_sha256):
    identity=['model_sha256','speech_tokenizer_sha256','model_revision','speaker','locale']
    if any(previous.get(k)!=expected.get(k) for k in identity):return {}
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

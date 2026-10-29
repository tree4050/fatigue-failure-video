"""Generate original neural narration, timed captions, and translated transcript.

Run from the project root: python src/synthesize.py --models ../work/models
Audio is synthesized per caption phrase, so captions use measured audio lengths,
not word-count estimates. Fixed 180-second edit; no post-hoc audio acceleration.
"""
import argparse, json, re, textwrap
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
from lesson import SCENES, CUES, spoken

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
ASSETS=ROOT/'assets'

def stamp(t, sep=','):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{sep}{ms%1000:03}'

def wrap(text, width=68):
    lines=textwrap.wrap(text,width=width,break_long_words=False,break_on_hyphens=False)
    if len(lines)>2:
        words=text.split(); mid=min(range(1,len(words)),key=lambda k:abs(len(' '.join(words[:k]))-len(' '.join(words[k:]))))
        lines=[' '.join(words[:mid]),' '.join(words[mid:])]
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--models',default='models');args=ap.parse_args()
    model=Path(args.models)
    # CPU session is bounded for repeatability and to avoid thread oversubscription.
    opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
    session=ort.InferenceSession(str(model/'kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
    k=Kokoro.from_session(session,str(model/'voices-v1.0.bin'))
    OUT.mkdir(exist_ok=True);(ASSETS/'voice_clips').mkdir(exist_ok=True)
    cache_path=ASSETS/'voice_clips'/'settings.json'
    cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
    sr=24000; audio=np.zeros(sr*180,np.float32);timeline=[]
    for sc,(start,end,*_) in enumerate(SCENES):
        clips=[];base_speed=0.86
        for key,scene,english,chinese in CUES:
            if scene!=sc:continue
            path=ASSETS/'voice_clips'/f'{key}.wav'
            if path.exists() and cache.get(key,{}).get('text')==spoken(english): samples,srate=sf.read(path,dtype='float32')
            else:
                samples,srate=k.create(spoken(english),voice='af_heart',speed=base_speed,lang='en-us',sentence_pause=0.30,clause_pause=0.12)
                sf.write(path,samples,srate,subtype='PCM_16')
                cache[key]={'text':spoken(english),'voice':'af_heart','speed':base_speed,'sentence_pause':0.30,'clause_pause':0.12}
            assert srate==sr
            clips.append((key,english,chinese,samples))
        total=sum(len(x[3])/sr for x in clips)
        # Preserve breathing room; regenerate only if a scene does not fit.
        room=end-start-1.0-0.20*(len(clips)-1)
        if total>room:
            speed=min(1.12,base_speed*total/room*1.02)
            clips=[]
            for key,scene,english,chinese in CUES:
                if scene!=sc:continue
                samples,srate=k.create(spoken(english),voice='af_heart',speed=speed,lang='en-us',sentence_pause=0.25,clause_pause=0.10)
                sf.write(ASSETS/'voice_clips'/f'{key}.wav',samples,srate,subtype='PCM_16')
                cache[key]={'text':spoken(english),'voice':'af_heart','speed':speed,'sentence_pause':0.25,'clause_pause':0.10}
                clips.append((key,english,chinese,samples))
            total=sum(len(x[3])/sr for x in clips)
        else:speed=base_speed
        if total>room+0.15:raise RuntimeError(f'Scene {sc} does not fit: {total:.2f}s')
        # Each scene has deliberate visual pauses. Credits leave the last 7+ sec quiet.
        available=end-start-total
        lead=0.55
        if sc==6:gap=0
        else:gap=min(2.2,max(0.20,(available-1.1)/max(1,len(clips)-1)))
        t=start+lead
        for key,en,zh,samples in clips:
            # Soft fades prevent discontinuities without altering speech timing.
            samples=samples.copy();n=min(120,len(samples)//2)
            samples[:n]*=np.linspace(0,1,n);samples[-n:]*=np.linspace(1,0,n)
            i=round(t*sr);audio[i:i+len(samples)]+=samples
            d=len(samples)/sr
            timeline.append(dict(id=key,scene=sc,start=round(t,4),end=round(t+d,4),english=en,chinese=zh,caption=wrap(en),speed=cache[key]['speed']))
            t+=d+gap
        print(f'Scene {sc+1}: voice={total:.2f}s; speed={speed:.3f}; end={t-gap:.2f}/{end}',flush=True)
    # Uniform narration gain, plus final EBU R128 normalization in render.py.
    peak=float(np.max(np.abs(audio)));audio*=0.88/max(peak,1e-8)
    sf.write(ASSETS/'narration.wav',audio,sr,subtype='PCM_16')
    cache_path.write_text(json.dumps(cache,indent=2,ensure_ascii=False),encoding='utf-8')
    (ASSETS/'timeline.json').write_text(json.dumps(timeline,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'Fatigue_Failure_EN.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(timeline))+'\n',encoding='utf-8')
    transcript=['# Fatigue Failure: From Small Cracks to Sudden Fracture','',
        '英文旁白與繁體中文對照。K I 與 K I c 分別讀作 “K eye” 與 “K eye see”；符號讀音與字幕意義一致。','']
    for c in timeline:transcript.extend([f'**{stamp(c["start"], ".")}–{stamp(c["end"], ".")}**', '', c['english'],'',c['chinese'],''])
    (ROOT/'docs'/'Narration_EN_ZH.md').write_text('\n'.join(transcript),encoding='utf-8')
    count=len(re.findall(r"\b[\w]+(?:['’][\w]+)?\b",' '.join(c['english'] for c in timeline)))
    print('Word count:',count,'Peak:',peak,flush=True)

if __name__=='__main__':main()

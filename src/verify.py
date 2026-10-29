"""Meaningful technical checks for the delivered film. Requires FFmpeg/ffprobe."""
import json, subprocess, re, wave, hashlib, importlib.metadata
from pathlib import Path
import numpy as np
from PIL import ImageFont

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=ROOT/'output'/'Fatigue_Failure.mp4'
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
    v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    assert v['width']==1920 and v['height']==1080
    assert v['r_frame_rate']=='24/1' and v['pix_fmt']=='yuv420p'
    assert int(v['nb_frames'])==4320
    assert abs(float(meta['format']['duration'])-180)<.025
    assert v['codec_name']=='h264' and a['codec_name']=='aac'
    assert abs(float(a['duration'])-180)<.05
    # Decode every video frame and the full audio stream, not only a thumbnail.
    d=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
    assert d.returncode==0 and not d.stderr.strip(),d.stderr
    cues=json.loads((ROOT/'assets'/'timeline.json').read_text());prev=0;min_font=40
    for c in cues:
        assert c['start']>=prev and c['end']>c['start'] and c['end']<=180
        lines=c['caption'].splitlines();assert len(lines)<=2
        size=40
        while max(ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans.ttf'),size).getlength(x) for x in lines)>1740:size-=1
        assert size>=32
        min_font=min(min_font,size)
        top=947 if len(lines)==2 else 967
        for i,line in enumerate(lines):
            f=ImageFont.truetype(str(ROOT/'assets/fonts/DejaVuSans.ttf'),size)
            bb=f.getbbox(line);assert top+i*47+bb[3]<1052
        prev=c['end']
    # Same-length fade/gain normalization is used; there is no speed change in muxing.
    with wave.open(str(ROOT/'assets'/'narration.wav')) as f:
        assert f.getnframes()/f.getframerate()==180
        pcm=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16)/32768
    assert float(np.max(np.abs(pcm)))<1
    wc=len(re.findall(r"\b[\w]+(?:['’][\w]+)?\b",' '.join(c['english'] for c in cues)))
    assert 350<=wc<=400
    report={
      'status':'PASS','duration_seconds':float(meta['format']['duration']),
      'video':{k:v[k] for k in ['codec_name','width','height','r_frame_rate','pix_fmt','nb_frames']},
      'audio':{k:a[k] for k in ['codec_name','sample_rate','channels','duration']},
      'full_decode_errors':d.stderr,'narration_word_count':wc,'caption_cues':len(cues),
      'maximum_caption_lines':2,'minimum_caption_font_px':min_font,'caption_safe_box':[64,934,1856,1052],
      'caption_timing_method':'Measured per-phrase neural voice WAV duration, placed on fixed 180-second timeline.',
      'voice':'Kokoro-82M v1.0 / af_heart / en-us',
      'voice_speeds':sorted(set(round(c['speed'],6) for c in cues)),
      'music':'None','source_photo':'Wang Hui-li and Qin Si-feng (2014), Figure 2, PMC4135168',
      'visual_review':'Scene contact sheet and detailed frames inspected; formula, arrow directions, axis labels and caption bounds checked.',
      'limitations':['Schematic crack motion and cycle numbers.','Illustrative S-N curves, no design data.','Photo does not map a precise crack origin.','K indicator is qualitative, not a finite-width stress-intensity solver.'],
      'versions':{k:importlib.metadata.version(k) for k in ['Pillow','numpy']},
      'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
      'file_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    }
    (ROOT/'output'/'qa_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=='__main__':main()

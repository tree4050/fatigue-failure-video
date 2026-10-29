"""Download optional Kokoro voice dependencies and verify their exact bytes."""
import hashlib, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES={
    'kokoro-v1.0.onnx':('https://huggingface.co/fastrtc/kokoro-onnx/resolve/main/kokoro-v1.0.onnx','7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5'),
    'voices-v1.0.bin':('https://huggingface.co/fastrtc/kokoro-onnx/resolve/main/voices-v1.0.bin','bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d'),
}

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    dest=ROOT/'models';dest.mkdir(exist_ok=True)
    for name,(url,expected) in FILES.items():
        p=dest/name
        if p.exists() and sha(p)==expected:print('Verified',name);continue
        tmp=dest/(name+'.tmp')
        print('Downloading',name,flush=True)
        urllib.request.urlretrieve(url,tmp)
        actual=sha(tmp)
        if actual!=expected:raise RuntimeError(f'Checksum mismatch for {name}: {actual}. Do not use unverified weights.')
        tmp.replace(p);print('Verified',name,flush=True)

if __name__=='__main__':main()

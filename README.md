# Fatigue Failure: From Small Cracks to Sudden Fracture

A three-minute English teaching film for university engineering students. Original, deterministic animation; a genuine published bolt photograph; neural English narration; burned-in English captions. The finished MP4 is delivered separately so this source package stays small.

## Deliverables

- `output/Fatigue_Failure_EN.srt` — English captions.
- `docs/Narration_EN_ZH.md` — complete narration with Traditional Chinese translation.
- `docs/Storyboard.md` — timing, visuals, narration and sources.
- `docs/Sources_and_Licenses.md` — verified sources and asset licenses.
- `docs/Prompts_and_Workflow.md` — actual AI task prompt, voice inputs and production method.
- `docs/QA.md` and `output/qa_report.json` — final checks.
- `assets/narration.wav`, `assets/timeline.json`, photo and fonts — everything needed to re-render offline.
- `src/lesson.py` — authoritative English / Chinese text and scene boundaries.
- `src/render.py` — actual video rendering code used for this film.
- `src/synthesize.py` — actual voice and caption generation code.

## Re-render the film (no AI account or model download required)

Use Python 3.12, FFmpeg with the libx264 and AAC encoders, and the included assets. Commands work from this folder. On Windows, use `py` instead of `python` if necessary and add FFmpeg to PATH.

```sh
python -m venv .venv
# Activate .venv for your operating system, then:
python -m pip install -r requirements.txt
python src/render.py
python src/verify.py
```

Output: `output/Fatigue_Failure.mp4`, 1920 × 1080, 24 fps, 180.000 seconds, H.264 / yuv420p + AAC. The source photograph, measured phrase timing, font files and narration WAV are included. No paid service, API key or browser session is required. Different FFmpeg versions can produce bytewise different MP4 encodings with the same content and timing.

To inspect still frames:

```sh
python src/render.py --stills
```

## Regenerate or edit the neural voice

This optional step needs an internet connection for the model download (~354 MB). The model weights are not inside this source ZIP. Their download URLs and SHA-256 hashes are pinned in `src/fetch_models.py`. The already-generated WAV and caption clips are included, so rendering does not depend on the availability of those external URLs.

```sh
python -m pip install -r requirements-voice.txt
python src/fetch_models.py
python src/synthesize.py --models models
python src/render.py
python src/verify.py
```

Edit the English and Chinese text in `src/lesson.py` before regenerating. Matching cached voice clips are reused; delete `assets/voice_clips/` to force a full synthesis. Exact per-phrase synthesis parameters are in `assets/voice_clips/settings.json`. Voice: Kokoro-82M v1.0, `af_heart`, English (US). Caption spelling `K I` / `K I c` is pronounced “K eye” / “K eye see”; `S–N` is pronounced letter by letter. No real person's voice was cloned.

## Scientific scope

The single-edge-cracked plate is a teaching schematic, separate from the photographed bolt. All animation phases reuse that plate. `a` always means distance from the left edge to the crack tip, perpendicular to the applied tensile load. The counter and motion are illustrative. The S–N curve and its scatter points are invented teaching examples, not fitted measurements. The K indicator is qualitative, not a geometry-corrected numerical solver. Y may change as crack geometry changes.

The fast-fracture comparison uses linear-elastic fracture mechanics with valid plane-strain conditions. It is not a rule that covers all plastic collapse or all fracture geometries. Fatigue crack extension can occur at peak K below K_Ic. A laboratory fatigue limit is not a universal service guarantee. The video does not teach Paris' law or make one-beach-mark-per-cycle claims.

## GitHub upload

This is an upload-ready source folder; no GitHub repository was created and no repository URL is implied. A `.gitignore` excludes downloaded model weights and rendered large outputs. If uploading the finished MP4 later, use a release asset or Git LFS as appropriate. Preserve the photograph attribution and the included third-party font license.

## Rights

The original Python code and original explanatory text / drawings in this package may be reused and adapted for education or further development. Third-party assets retain their own licenses: the photograph follows the original article's CC BY 3.0 notice; DejaVu fonts retain their bundled license; optional Kokoro model weights are Apache-2.0 and the kokoro-onnx software is MIT. See the full credits before redistribution. No endorsement by any source institution is implied.

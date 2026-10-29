# References, photo provenance and licenses

Checked on 2026-10-29. Source pages were opened and their relevant content checked. None of the animation curves, points, crack-growth rates or cycle numbers are measured test data. No AI-generated image is represented as a real specimen.

## Teaching sources

| ID | Source | Used for | Verified URL |
|---|---|---|---|
| T1 | UNSW Sydney, School of Materials Science and Engineering, **Fatigue failure** | Fatigue below nominal yield strength; initiation, propagation and fast fracture. Explanations were written afresh; no source diagram was copied. | https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fatigue-failure |
| T2 | Dassault Systèmes, **SOLIDWORKS Design Help (2020): Stress–Life Cycle (S–N) Curve** | S and N axes; logarithmic cycle scale; mean stress / stress ratio and test conditions; scatter; qualified comparison of steel and aluminum. The help page may show a newer navigation shell. | https://help.solidworks.com/2020/English/SolidWorks/cworks/c_SN_Curve.htm |
| T3 | UNSW Sydney, **Fracture toughness** | Existing cracks, stress intensity, crack size and applied stress. | https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fracture-mechanics/fracture-toughness |
| T4 | ASTM International, **ASTM E399-24** public Scope / Significance and Use | Meaning and validity conditions of plane-strain toughness; small crack-tip plastic zone relative to relevant dimensions; fatigue extension below K_Ic. The paid standard was not purchased or reproduced. | https://store.astm.org/e0399-24.html |

## Real specimen photograph

**Authors as listed by the article:** Wang Hui-li and Qin Si-feng. **Year:** 2014. **Article:** *High-Strength Bolt Corrosion Fatigue Life Model and Application*, *The Scientific World Journal*, article 567318. **Figure:** 2, “Bolt fatigue fracture.” Published July 24, 2014. DOI: 10.1155/2014/567318. PMCID: PMC4135168.

- Original research: https://pmc.ncbi.nlm.nih.gov/articles/PMC4135168/
- DOI / publisher resolver: https://doi.org/10.1155/2014/567318
- Exact downloaded image: https://cdn.ncbi.nlm.nih.gov/pmc/blobs/6943/4135168/68b2a420ef66/TSWJ2014-567318.002.jpg
- Local asset: `assets/bolt-fatigue-fracture.jpg`, 600 × 524 pixels.
- Original article copyright: © 2014 W. Hui-li and Q. Si-feng.
- License followed: **Creative Commons Attribution 3.0 Unported**, as linked in the original PMC article metadata: https://creativecommons.org/licenses/by/3.0/
- Attribution used on screen: **Wang Hui-li & Qin Si-feng · 2014; Figure 2; doi:10.1155/2014/567318; CC BY 3.0.**
- Use: genuine research photograph resized proportionally for the 1080p film. The original pixels are not retouched, recolored or generated. A separate overlaid label and pointer identify the fracture surface as a whole; no crack origin, growth-zone boundary or final-zone boundary is inferred. The source image file is also included unchanged.
- The text next to Figure 2 discusses thread-root fracture. It does not map a precise initiation point or the boundaries of the different fracture regions on this photograph. That limitation is stated in narration and on screen.

**License discrepancy recorded:** the Wikimedia Commons mirror describes CC BY 4.0, whereas the original article's metadata links CC BY 3.0. This production downloaded from the original PMC-hosted image and follows the original article's CC BY 3.0 terms. The mirror was used only to discover the paper: https://commons.wikimedia.org/wiki/File:Bolt-fatigue-fracture.jpg

Only the photograph and its supported descriptive context are used from this article. Its corrosion-fatigue prediction model, numerical values and specialized equations are not used in the teaching animation.

## Other assets and software

| Item | Source / license | Use |
|---|---|---|
| DejaVu Sans / Sans Bold / Sans Mono | https://dejavu-fonts.github.io/ ; bundled `assets/fonts/LICENSE-DejaVu.txt` | Font files distributed unchanged to make rendering portable. |
| Kokoro-82M v1.0 | https://huggingface.co/hexgrad/Kokoro-82M ; Apache-2.0 | Original synthetic narration using `af_heart`; no voice cloning. |
| Kokoro ONNX weights mirror | https://huggingface.co/fastrtc/kokoro-onnx | Download source for optional voice regeneration. Upstream Kokoro model license applies; the mirror's software-facing MIT label is not substituted for the upstream weight license. |
| kokoro-onnx | https://github.com/thewh1teagle/kokoro-onnx ; MIT | Text-to-speech inference. |
| ONNX Runtime | https://github.com/microsoft/onnxruntime ; MIT | CPU model inference. |
| Pillow | https://python-pillow.github.io/ ; HPND | Original drawings, typography, image placement and frame rendering. |
| NumPy | https://numpy.org/ ; BSD-3-Clause | Signal arrays and deterministic geometry. |
| SoundFile | https://python-soundfile.readthedocs.io/ ; BSD-3-Clause | Voice WAV output. |
| FFmpeg | https://github.com/FFmpeg/FFmpeg ; license depends on build, libx264-enabled build used | H.264/AAC encoding, normalization, duration and decode checks. Executable is not redistributed. |
| faster-whisper (QA only) | https://github.com/SYSTRAN/faster-whisper ; MIT | Optional automated speech sanity check; not used for final caption timings. |
| Original graphics and code | Created for this request | Plate, crack animation, arrows, diagrams, illustrative curves and captions. No stock video, music or generative image asset. |

Technical software links identify upstream projects. Exact installed versions are recorded in `requirements*.txt` and `output/qa_report.json`. The science sources above and the photo provenance were the external content used to write the lesson.

## Interpretation notes

- A and B on the illustrative steel curve are **300 MPa at 10⁴ cycles** and **210 MPa at 10⁶ cycles**. The drawing function is `max(180, 480 − 45 log10(N))` over 10³–10⁸. This is an editorial teaching shape, not a fit to steel data.
- The illustrative aluminum curve is `325 − 46(log10(N) − 3)` MPa over that interval. Its lack of a plateau is the teaching point; no alloy, temper or service environment is assigned.
- Scatter dots are invented illustrations. No part-specific life guarantee is made.
- For K_I = Y × sigma × sqrt(pi × a), Y is dimensionless; sigma is in MPa and a is in meters, giving MPa√m. The indicator bar is qualitative. The video does not numerically assume Y stays constant as a finite-width crack grows.
- `a` is a single-edge crack depth, not half a center-crack length. The drawn plate and the bolt photo are explicitly different kinds of evidence.
- The diagram's crack-opening width, elastic deformation, cycle counter and animation duration are exaggerated or compressed for visibility.
- No beach marks are labeled or counted. No claim about one visible band per load cycle is made.

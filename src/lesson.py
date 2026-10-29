"""Authoritative narration and fixed editorial timeline (seconds)."""
SCENES = [
    (0, 15, '01', 'Fatigue Failure', 'From Small Cracks to Sudden Fracture'),
    (15, 35, '02', 'Read the evidence', 'A real bolt fracture'),
    (35, 65, '03', 'A crack changes everything', 'Initiation → propagation → final fracture'),
    (65, 105, '04', 'Read an S–N curve', 'Stress amplitude and fatigue life'),
    (105, 140, '05', 'When does a crack become critical?', 'Stress intensity and fracture toughness'),
    (140, 165, '06', 'Connect the ideas', 'From repeated loads to rapid fracture'),
    (165, 180, '07', 'References & credits', 'Full URLs and licenses accompany this video'),
]
# English captions represent the spoken words; technical symbols use normal notation.
# Spoken replacements below affect pronunciation only.
CUES = [
('hook', 0, "Why can a metal part fail even when no single load is large enough to break it?", "為什麼金屬零件會斷裂，即使每一次載重都不足以單獨把它弄斷？"),
('define', 0, "Fatigue is damage from repeated loading. It can occur when nominal stress stays below yield strength.", "疲勞是反覆載重造成的損傷。即使名義應力低於材料的降伏強度，也可能發生破壞。"),
('photo', 1, "This is a real fractured bolt from published research.", "這是一張已發表研究中的真實斷裂螺栓照片。"),
('root', 1, "The paper notes that fatigue commonly occurs at thread roots.", "論文指出，螺栓的疲勞破壞常發生在螺紋根部。"),
('unmapped', 1, "The exact origin is not mapped here.", "這張照片並未標示確切的裂紋起始位置。"),
('surfaces', 1, "Fatigue surfaces may show smoother growth regions and rougher final fracture; appearances vary.", "疲勞斷面可能有較平滑的成長區和較粗糙的最終斷裂區；實際外觀並不完全相同。"),
('schematic', 2, "Now follow one schematic specimen.", "現在我們用同一個示意試件，觀察整個過程。"),
('initiation', 2, "A scratch concentrates stress locally, and a small crack begins.", "刮痕造成局部應力集中，微小裂紋因而起始。"),
('tension', 2, "Repeated tension opens the crack.", "反覆拉伸使裂紋張開。"),
('growth', 2, "As cycle count N increases, crack length a grows, leaving less intact material.", "隨著循環次數 N 增加，裂紋長度 a 增長，剩餘完整的材料逐漸減少。"),
('hidden', 2, "The gradual growth may be hard to see. The sudden break is only the final stage.", "逐漸發展的裂紋可能很難察覺。突然斷裂只是整個過程的最後階段。"),
('fracture', 2, "Once the crack reaches a critical condition, the remaining section fractures rapidly.", "當裂紋達到臨界狀態，剩餘截面便快速斷裂。"),
('sn_intro', 3, "An S–N curve connects stress amplitude to fatigue life.", "S–N 曲線把應力振幅與疲勞壽命連結起來。"),
('amplitude', 3, "S is half the difference between maximum and minimum stress.", "S 是最大應力與最小應力之差的一半。"),
('axis_s', 3, "The vertical axis is stress amplitude in megapascals.", "縱軸是應力振幅，單位為百萬帕斯卡，也就是 MPa。"),
('axis_n', 3, "The horizontal axis shows cycles to failure on a logarithmic scale.", "橫軸用對數刻度表示試件破壞前所承受的循環次數。"),
('sn_read', 3, "Choose a stress, move across to the curve, then down to read life.", "選定應力振幅，水平移到曲線，再垂直向下讀出疲勞壽命。"),
('lower', 3, "For the same material and conditions, lower amplitude usually means longer life.", "對相同材料和試驗條件而言，較低的應力振幅通常代表較長的壽命。"),
('scatter', 3, "Actual results scatter.", "實際試驗結果具有分散性。"),
('steel', 3, "Some steels show a fatigue limit under specific test conditions.", "某些鋼材在特定試驗條件下會呈現疲勞限。"),
('aluminum', 3, "Aluminum alloys generally do not. These limits are not universal safety guarantees.", "鋁合金通常沒有明確的疲勞限。這些試驗中的極限，也不是適用於所有情況的安全保證。"),
('toughness', 4, "Fracture toughness measures resistance to fracture with a crack.", "斷裂韌性衡量材料已經存在裂紋時，抵抗斷裂的能力。"),
('ki', 4, "K I describes crack tip loading: the Mode one stress intensity factor.", "K I 描述裂紋尖端的載重狀態，是第一型，也就是張開型的應力強度因子。"),
('symbols', 4, "Y describes geometry; sigma is tensile stress; a measures edge to tip.", "Y 反映幾何形狀；sigma 是施加的拉伸應力；a 是從試件邊緣到裂紋尖端的長度。"),
('compare', 4, "Raising stress or lengthening the crack increases K I.", "提高應力，或使裂紋增長，都會增加 K I。"),
('kic', 4, "K I c is material plane strain fracture toughness, not yield strength.", "K I c 是材料的平面應變斷裂韌性，並不是降伏強度。"),
('critical', 4, "Under linear elastic, valid plane strain conditions, peak K I reaching K I c can trigger rapid fracture.", "在線彈性且符合有效平面應變條件下，最大 K I 達到 K I c 時，可能觸發快速斷裂。"),
('subcritical', 4, "Fatigue cracks can grow below this limit.", "疲勞裂紋在低於這個臨界值時，也能逐漸成長。"),
('recap1', 5, "Repeated loading can cause fatigue damage.", "反覆載重可能造成疲勞損傷。"),
('recap2', 5, "S–N curves relate stress amplitude to fatigue life.", "S–N 曲線描述應力振幅與疲勞壽命的關係。"),
('recap3', 5, "Fracture toughness helps assess when an existing crack becomes critical.", "斷裂韌性有助於評估既有裂紋何時達到臨界狀態。"),
('engineering', 5, "Reduce stress concentrations, improve surface condition, and inspect for cracks to reduce fatigue risk.", "降低應力集中、改善表面狀況，並檢查裂紋，可以降低疲勞破壞的風險。"),
('credits', 6, "These sources support the lesson. Full links, photo credits, and reproducible code accompany this video.", "本影片以這些來源為依據，並附上完整連結、照片出處和可重現的程式碼。"),
]

def spoken(text):
    return text.replace('S–N', 'S N').replace('K I c', 'K eye see').replace('K I', 'K eye')

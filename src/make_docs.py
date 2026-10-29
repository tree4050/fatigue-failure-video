"""Build the actual storyboard and one readable companion Markdown artifact."""
from pathlib import Path
import json
from lesson import SCENES

ROOT=Path(__file__).resolve().parents[1]

VISUALS={
'hook':'片頭完整題名；同一金屬板試件上下拉力箭頭反覆變長變短，左側顯示循環波形。',
'define':'維持反覆拉伸；強調多次載重可以累積損傷，畫面不是單次撞擊。',
'photo':'原始論文 Figure 2 斷裂螺栓照片；標示 Real specimen photograph、作者與年份。',
'root':'維持真實照片；旁邊說明螺紋根部會集中應力，箭頭僅指向整個斷面。',
'unmapped':'出現明確限制：來源未標示精確裂紋起點。',
'surfaces':'旁註一般斷面外觀可能不同；不把真實照片猜測分成成長區或最終區。',
'schematic':'切回單邊裂紋板試件，明確標示 Schematic — not to scale。',
'initiation':'表面刮痕局部圈選；紅色小裂紋出現，a 尺寸從左邊緣量到尖端。',
'tension':'上下拉伸箭頭週期變化，裂紋依同一方向張開，未出現剪切方向錯誤。',
'growth':'N 示意計數器遞增；紅色裂紋逐格向右增長；綠色剩餘完整截面縮短。',
'hidden':'維持漸進裂紋成長，讓學生看到緩慢累積與剩餘截面的變化。',
'fracture':'裂紋快速跨越剩餘截面，試件上下分離；成長速度明顯快於前一階段。',
'sn_intro':'畫出 S–N 曲線：MPa 縱軸、10³–10⁸ 對數橫軸；註明非設計資料。',
'amplitude':'右側單一應力週期標 max/min、半範圍 S，顯示 S = (max − min)/2。',
'axis_s':'保留可讀的 Stress amplitude, S (MPa) 標籤與刻度。',
'axis_n':'保留 Cycles to failure, N (log scale) 標籤與十倍間隔刻度。',
'sn_read':'A 點讀圖：300 MPa 水平至藍色曲線，再垂直落到 10⁴ 次循環。',
'lower':'B 點讀圖：同曲線 210 MPa 對應 10⁶ 次循環，與 A 並列比較。',
'scatter':'加入明確標示為示意的散點；沒有把曲線當作每個零件的保證。',
'steel':'藍色示意曲線的水平段加粗，標示 Some steels: fatigue limit。',
'aluminum':'加入持續下降的橙色鋁合金示意曲線；旁白提醒條件限制。',
'toughness':'大字公式 K_I = Y × sigma × sqrt(pi × a)；顯示 MPa√m。',
'ki':'定義 Mode I 張開型的應力強度因子；保留同一單邊裂紋試件。',
'symbols':'逐項符號說明，a 的雙箭頭由邊緣指到裂紋尖端，sigma 單位 MPa、a 單位 m。',
'compare':'先固定 a 提高拉力；接著固定應力延長 a；兩種示意 K_I 指示條均增加。',
'kic':'保留長裂紋比較，另標 K_Ic 為材料平面應變斷裂韌性。',
'critical':'K_I,max 接近 K_Ic 臨界線；標示 LEFM 與有效平面應變條件；試件快速分離。',
'subcritical':'明確回看斷裂前階段；顯示 K_I,max < K_Ic 時仍可疲勞成長。',
'recap1':'五步因果鏈依序亮起，搭配同一試件的縮圖與第一句重點。',
'recap2':'加上第二句重點，連結 S–N 曲線與整體疲勞壽命。',
'recap3':'加上第三句重點，連結既有裂紋與臨界狀態。',
'engineering':'三個工程圖示：平滑過渡、改善表面、放大檢查裂紋。',
'credits':'完整 15 秒來源頁；UNSW、SOLIDWORKS、ASTM、論文 DOI、CC BY 授權與製作工具。',
}

def timecode(t):return f'{int(t)//60}:{t%60:06.3f}'

def main():
    cues=json.loads((ROOT/'assets'/'timeline.json').read_text())
    sources=['T1','P1 / T1','T1','T2','T3 / T4','T1 / T2 / T3 / T4','T1–T4 / P1']
    lines=['# 分鏡表與實際時間軸','',
    '固定總長 180.000 秒。表列秒數包含可供看圖的停頓；逐句開始／結束時間來自實際旁白 WAV。T1–T4 與 P1 的完整來源、照片授權及使用方式見 Sources_and_Licenses.md。','',
    '| 影片時間 | 教學段落 | 視覺重點 | 來源 |','|---|---|---|---|']
    overview=['反覆載重，不是單次超載。','研究中的真實螺栓斷面，保留判讀限制。','起始、逐漸成長、快速最終斷裂。','應力振幅、對數壽命軸、兩點讀圖、條件限制。','K_I 公式、a 定義、應力與裂紋比較、K_Ic。','五步因果鏈與三句重點，改善設計與檢查。','教學來源、照片作者與 CC BY 3.0，工具致謝。']
    for i,(s,e,n,title,sub) in enumerate(SCENES):lines.append(f'| {int(s)//60}:{int(s)%60:02}–{int(e)//60}:{int(e)%60:02} | {title} | {overview[i]} | {sources[i]} |')
    lines+=['','## 逐句畫面與旁白','', '| 實際旁白時間 | 畫面／動畫 | 英文旁白 | 來源 |','|---|---|---|---|']
    for c in cues:lines.append(f'| {timecode(c["start"])}–{timecode(c["end"])} | {VISUALS[c["id"]]} | {c["english"]} | {sources[c["scene"]]} |')
    lines+=['','P1：Wang Hui-li & Qin Si-feng (2014), Figure 2, DOI 10.1155/2014/567318。','',
    '未提供實測疲勞曲線、實驗成長率或對此照片的精確區域判定。程式動畫屬教學示意。']
    (ROOT/'docs'/'Storyboard.md').write_text('\n'.join(lines),encoding='utf-8')
    guide=['# Fatigue Failure: From Small Cracks to Sudden Fracture','',
       '製作附冊｜3:00 英文教學影片｜355 個英文單字｜1920 × 1080 / 24 fps','',
       '本附冊包含完整雙語旁白、實際分鏡時間、來源與授權、實際使用的 AI 提示詞和製作流程。原始碼 ZIP 中另含所有程式、必要素材與可執行說明。','']
    for fname in ['Narration_EN_ZH.md','Storyboard.md','Sources_and_Licenses.md','Prompts_and_Workflow.md','QA.md']:
        p=ROOT/'docs'/fname
        if p.exists():guide+=['---','',p.read_text(encoding='utf-8'),'']
    (ROOT/'output'/'Fatigue_Failure_Production_Guide.md').write_text('\n'.join(guide),encoding='utf-8')
    print('Storyboard and production guide written.')

if __name__=='__main__':main()

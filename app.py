import streamlit as st
import wfdb
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ==========================================
# 1. 页面基本设置 (UI 初始化)
# 1. Page basic settings (UI initialization)
# 1. Grundlegende Seiteneinstellungen (UI-Initialisierung)
# ==========================================
st.set_page_config(page_title="EKG Analyse-Tool", layout="wide")
st.title("👨‍⚕️ Professionelles EKG-Signalverarbeitungs-Tool")
st.markdown("Entwickelt für die Medizintechnik. Dieses Tool demonstriert die Kaskadierung von digitalen Filtern zur Rauschunterdrückung.")

# ==========================================
# 2. 侧边栏控制台 (Sidebar Controls)
# 2. Sidebar console (Sidebar Controls)
# 2. Seitenleisten-Konsole (Sidebar Controls)
# ==========================================
st.sidebar.header("⚙️ Parameter-Einstellungen")


# 完整的 MIT-BIH 记录编号列表 (共 48 个)
mitdb_records = [
    '100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
    '111', '112', '113', '114', '115', '116', '117', '118', '119', '121',
    '122', '123', '124', '200', '201', '202', '203', '205', '207', '208',
    '209', '210', '212', '213', '214', '215', '217', '219', '220', '221',
    '222', '223', '228', '230', '231', '232', '233', '234'
]

# 选择患者记录
# Select patient record
# Patienten-Datensatz auswählen
# index=5 会让网页默认选中 '105' 号病人，方便直接展示带噪声的脏数据
record_name = st.sidebar.selectbox(
    "1. Patienten-Datensatz auswählen (MIT-BIH):", 
    mitdb_records,
    index=5, 
    help="Datensätze im 100er-Bereich sind Routine-EKGs, 200er-Bereich enthält komplexe Arrhythmien."
)
# 滤波器开关
# Filter switches
# Filter-Schalter
st.sidebar.markdown("---")
st.sidebar.subheader("2. Digitale Filter")
apply_notch = st.sidebar.checkbox("🟢 50Hz Notch-Filter (Gegen Netzbrummen)", value=False)
apply_bandpass = st.sidebar.checkbox("🔵 Bandpassfilter 0.5-40Hz (Gegen Basislinienwandern & EMG)", value=False)

# ==========================================
# 3. 核心后端逻辑 (数据读取与处理)
# 3. Core backend logic (Data loading & processing)
# 3. Kern-Backend-Logik (Daten laden & verarbeiten)
# ==========================================
# 使用 st.cache_data 缓存数据，避免每次点按钮都重新下载
# Use st.cache_data to cache data, avoid re-downloading on every button click
# Verwenden Sie st.cache_data, um Daten zu cachen und erneutes Herunterladen bei jedem Button-Klick zu vermeiden
@st.cache_data
def load_data(record_id):
    record = wfdb.rdrecord(record_id, pn_dir='mitdb', sampto=2000)
    return record.p_signal[:, 0]

raw_signal = load_data(record_name)
fs = 360.0  # 采样率 / Sampling rate / Abtastrate

# 信号处理管道 (Signal Processing Pipeline)
# Signal processing pipeline
# Signalverarbeitungs-Pipeline
processed_signal = np.copy(raw_signal)

# 级联滤波逻辑
# Cascaded filtering logic
# Kaskadierte Filterlogik
if apply_notch:
    b_notch, a_notch = signal.iirnotch(50.0, 30.0, fs)
    processed_signal = signal.filtfilt(b_notch, a_notch, processed_signal)

if apply_bandpass:
    nyq = 0.5 * fs
    b_bp, a_bp = signal.butter(4, [0.5/nyq, 40.0/nyq], btype='band')
    processed_signal = signal.filtfilt(b_bp, a_bp, processed_signal)

# ==========================================
# 4. 医疗级数据可视化 (UI 渲染)
# 4. Medical-grade data visualization (UI rendering)
# 4. Medizinische Datenvisualisierung (UI-Rendering)
# ==========================================
st.subheader(f"📊 EKG-Signal: Datensatz {record_name}")

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(processed_signal, color='#d62728', linewidth=1.2, zorder=3)

# 绘制医疗标准网格
# Draw medical standard grid
# Zeichne medizinisches Standardraster
ax.xaxis.set_major_locator(MultipleLocator(72))  
ax.xaxis.set_minor_locator(MultipleLocator(14.4)) 
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))

ax.grid(which='major', color='#ff9999', linestyle='-', linewidth=1.2, alpha=0.8)
ax.grid(which='minor', color='#ffcccc', linestyle='-', linewidth=0.5, alpha=0.5)

ax.set_xlabel("Zeitachse (Abtastwerte | 1 großes Kästchen = 0,2s)", fontsize=10)
ax.set_ylabel("Spannung (mV)", fontsize=10)
# 根据是否滤波动态改变标题
# Dynamically change title based on filtering status
# Titel dynamisch je nach Filterstatus ändern
status_text = "Gefiltert" if (apply_notch or apply_bandpass) else "Originalsignal (Ungefiltert)"
ax.set_title(f"Status: {status_text}", fontsize=12)
   
# 将画好的图表推送到 Streamlit 网页中
# Push the drawn chart to the Streamlit web page
# Das gezeichnete Diagramm auf die Streamlit-Webseite übertragen
st.pyplot(fig)

# 底部免责声明 (增加专业感)
# Footer disclaimer (adds a professional touch)
# Fußzeilen-Haftungsausschluss (fachliche Note)
st.info("⚠️ Hinweis: Diese Software ist ein akademischer Prototyp und nicht für die klinische Diagnostik zugelassen (Kein Medizinprodukt gem. MDR).")

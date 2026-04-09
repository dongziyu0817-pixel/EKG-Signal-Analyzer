# 👨‍⚕️ EKG Signal Processing Web App (Prototype)

**[🔗 https://ekg-signal-analyzer-5zdgmzbuhvv4oy7qtzrhsh.streamlit.app/]**

## 1. 🇩🇪 Projektübersicht / 🇬🇧 Project Overview / 🇨🇳 项目概述
* **DE:** Diese interaktive Web-Anwendung demonstriert den Einsatz digitaler Signalverarbeitung (DSP) zur Bereinigung von EKG-Signalen aus dem klinischen Alltag (Unterdrückung von Basislinienwandern und 50Hz-Netzbrummen).
* **EN:** This interactive web application demonstrates the application of Digital Signal Processing (DSP) to clean real-world clinical ECG signals (suppressing baseline wander and 50Hz powerline interference).
* **ZH:** 本交互式 Web 应用演示了如何利用数字信号处理技术（DSP）清洗真实临床环境下的 EKG 噪声（抑制基线漂移和 50Hz 工频干扰）。

## 2. 🗄️ Datenquelle / Data Source / 数据溯源
* **MIT-BIH Arrhythmia Database (PhysioNet)**.
* **Datensatz / Record 105:** Enthält starkes Rauschen für Stresstests von Filteralgorithmen. / Contains severe noise for stress-testing filtering algorithms. / 包含严重噪声，用于压力测试滤波算法。

## 3. ⚙️ Algorithmus / Algorithm / 算法架构
* **Cascaded Filtering Strategy (Kaskadierte Filterstrategie / 级联滤波策略)**
* **Stufe 1 (Stage 1):** 50Hz Notch-Filter (Gütefaktor / Quality Factor Q=30) zur Eliminierung von Netzbrummen.
* **Stufe 2 (Stage 2):** 0.5Hz - 40Hz Bandpassfilter (Butterworth 4. Ordnung / 4th-order) gegen Basislinienwandern und EMG-Artefakte. Zero-phase filtering (filtfilt) bewahrt die ST-Strecke.

## 4. 🐳 Entwicklerumgebung / Development Environment / 开发环境
* **DevContainers Ready:** Dieses Repository enthält einen `.devcontainer`, um eine standardisierte und reproduzierbare Entwicklungsumgebung via GitHub Codespaces oder VS Code Remote Containers zu gewährleisten.
* **EN:** This repository includes a `.devcontainer` to ensure a standardized and reproducible development environment via GitHub Codespaces or VS Code Remote Containers.

## 5. ⚠️ Haftungsausschluss / Disclaimer / 免责声明
* **DE:** Reiner akademischer Prototyp. **Kein Medizinprodukt (SaMD)** gem. MDR/FDA. Nicht für klinische Zwecke.
* **EN:** Strictly an academic prototype. **Not a medical device (SaMD)** under MDR/FDA. Not for clinical use.

# 🌿 EcoAudit — Sistema de Auditoria Ambiental

Sistema desenvolvido em Python para auditorias ambientais com geração automática de relatórios e dashboard estratégico interativo.

🔗 **Acesse online:**  
https://ecoaudit-cli-nylkklhszocohercbstsnu.streamlit.app/

---

## 🎯 Objetivo

O EcoAudit foi criado para estruturar auditorias ambientais de forma organizada, permitindo:

- Aplicação de checklists (Resíduos, Água, Energia)
- Classificação de conformidade (Conforme, Atenção, Não conforme)
- Geração automática de plano de ação
- Cálculo de KPI estratégico (Índice de Conformidade)
- Visualização executiva via Dashboard Web

---

## 📊 Dashboard Estratégico

O sistema apresenta:

- Indicadores percentuais de conformidade
- Classificação automática de risco
- KPI com categorização (Excelente / Atenção / Crítico)
- Visualização gráfica da distribuição de status
- Plano de ação estruturado

---

## 🧠 Arquitetura

O projeto foi estruturado seguindo separação de responsabilidades:

ecoaudit/
│── cli.py # Interface da aplicação CLI
│── domain.py # Regras de negócio
│── storage.py # Persistência (JSON / CSV)
│── report.py # Geração de relatórios
│
app.py # Dashboard Web (Streamlit)
main.py # Entry point da CLI

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- Streamlit
- Pytest
- JSON / CSV
- Arquitetura modular

---

## 🚀 Como Executar Localmente

```bash
pip install -r requirements.txt
streamlit run app.py

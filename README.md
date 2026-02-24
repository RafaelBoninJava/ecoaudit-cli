# 🌿 EcoAudit — Sistema de Auditoria Ambiental (CLI + Dashboard)

Ferramenta em Python para **criar auditorias ambientais via terminal** e **visualizar resultados em um dashboard web (Streamlit)**.  
Gera relatórios com **timestamp**, exporta **JSON/CSV/Markdown** e destaca **não conformidades com plano de ação**.

🔗 **Demo (Streamlit Cloud):**  
https://ecoaudit-cli-nylkklhszocohercbstsnu.streamlit.app/

---

## ✅ Funcionalidades

- Auditorias por template: **Resíduos / Água / Energia**
- Checklist item a item com status:
  - **Conforme / Atenção / Não conforme**
- Se **Não conforme**, registra **Prioridade** e **Prazo**
- Exportação automática:
  - JSON (`data/audits/audit_YYYYMMDD-HHMMSS.json`)
  - Markdown (`reports/report_YYYYMMDD-HHMMSS.md`)
  - CSV (quando habilitado no projeto)
- Dashboard Streamlit:
  - Resumo com métricas
  - Gráfico de distribuição (barras)
  - Tabela detalhada do checklist
  - Alertas de risco / índice de conformidade
- Testes com `pytest`

---

## 🧱 Arquitetura

Organizado com separação de responsabilidades:
ecoaudit-cli/
├── main.py # Entry point da CLI
├── app.py # Dashboard (Streamlit)
├── ecoaudit/
│ ├── cli.py # Interface da CLI / menu
│ ├── domain.py # Regras de negócio e modelos
│ ├── storage.py # Persistência (JSON/CSV)
│ └── report.py # Geração de relatórios (MD)
├── data/ # Auditorias geradas (ignorado no Git)
├── reports/ # Relatórios gerados (ignorado no Git)
└── tests/ # Testes automatizados

---

## 🛠 Tecnologias

- Python 3.10+
- Streamlit
- Pytest
- JSON / CSV / Markdown

---

## ▶️ Como executar localmente

python -m pip install -r requirements.txt
python main.py
python -m streamlit run app.py
python -m pytest

### 1) Clonar e instalar dependências
```bash
git clone https://github.com/RafaelBoninJava/ecoaudit-cli.git
cd ecoaudit-cli
python -m pip install -r requirements.txt

👤 Autor

Rafael Bonin
Projeto desenvolvido para portfólio, com foco em arquitetura de software, automação e visualização de dados.

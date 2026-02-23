# EcoAudit — CLI & Dashboard para Auditorias Ambientais

Sistema para auditorias ambientais desenvolvido em Python com arquitetura modular, interface via terminal (CLI) e dashboard web interativo.

O projeto permite registrar auditorias ambientais por template, gerar relatórios automáticos e visualizar estatísticas em um painel gráfico.

---

## Funcionalidades

- Criação de auditorias ambientais (Resíduos, Água, Energia)
- Checklist interativo item a item
- Registro de status: Conforme / Atenção / Não conforme
- Observação por item
- Plano de ação automático para não conformidades
- Geração automática de arquivos com timestamp:
  - JSON
  - Markdown
  - CSV
- Dashboard Web interativo com gráfico de barras (Streamlit)
- Testes automatizados com pytest
- Arquitetura modular (separação de responsabilidades)

---

## Arquitetura do Projeto

ecoaudit-cli/
│
├── main.py # Entrada da CLI
├── app.py # Dashboard Web (Streamlit)
│
├── ecoaudit/
│ ├── cli.py # Lógica da interface CLI
│ ├── domain.py # Regras de negócio
│ ├── storage.py # Persistência (JSON/CSV)
│ └── report.py # Geração de relatórios
│
├── tests/ # Testes automatizados
├── data/ # Auditorias geradas
└── reports/ # Relatórios gerados

---

## Requisitos

- Python 3.10+
- Streamlit
- Pytest

Instalar dependências:

```bash
pip install streamlit pytest
```


## Autor

Rafael Bonin
Projeto desenvolvido para portfólio com foco em arquitetura de software, automação e visualização de dados.
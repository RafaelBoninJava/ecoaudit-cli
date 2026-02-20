# EcoAudit CLI

Sistema de auditoria ambiental via terminal (CLI) feito em Python.  
Permite aplicar checklists por template, registrar conformidades e gerar automaticamente relatório em Markdown com plano de ação para não conformidades.

## Funcionalidades
- Templates de auditoria: **Resíduos**, **Água**, **Energia**
- Checklist interativo item a item
- Status por item: **Conforme / Atenção / Não conforme**
- Observação por item
- Se **Não conforme**: registra **Prioridade** e **Prazo**
- Gera arquivos com timestamp:
  - `data/audits/audit_YYYYMMDD-HHMMSS.json`
  - `reports/report_YYYYMMDD-HHMMSS.md`

## Requisitos
- Python 3.10+ (recomendado)

## Como executar
Clone o repositório e rode:

```bash
python ecoaudit.py
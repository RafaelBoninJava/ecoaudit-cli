from ecoaudit.report import build_markdown_report

def test_build_markdown_report_contains_sections():
    audit = {
        "id": "20260220-000000",
        "nome": "Teste",
        "local": "Local X",
        "template": "Resíduos",
        "criado_em": "2026-02-20T00:00:00",
        "respostas": [
            {"item": "Pergunta 1", "status": "Conforme", "observacao": "", "prioridade": "", "prazo": ""},
            {"item": "Pergunta 2", "status": "Não conforme", "observacao": "Falha", "prioridade": "Alta", "prazo": "2026-03-01"},
        ],
    }

    md = build_markdown_report(audit)

    assert "# Relatório de Auditoria Ambiental" in md
    assert "## Informações Gerais" in md
    assert "## Checklist Detalhado" in md
    assert "## Plano de Ação (Não conformidades)" in md
    assert "| # | Item | Prioridade | Prazo | Observação | Ação sugerida |" in md
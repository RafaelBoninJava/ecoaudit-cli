import os
from datetime import datetime
from typing import Any, Dict, List


def _count_status(respostas: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "Conforme": sum(1 for r in respostas if r.get("status") == "Conforme"),
        "Atenção": sum(1 for r in respostas if r.get("status") == "Atenção"),
        "Não conforme": sum(1 for r in respostas if r.get("status") == "Não conforme"),
        "Total": len(respostas),
    }


def build_markdown_report(audit: Dict[str, Any]) -> str:
    audit_id = audit.get("id", "")
    nome = audit.get("nome", "")
    local = audit.get("local", "")
    template = audit.get("template", "")
    criado_em = audit.get("criado_em", "")
    respostas = audit.get("respostas", [])

    counts = _count_status(respostas)

    md = f"""# Relatório de Auditoria Ambiental

## Informações Gerais
- **ID:** {audit_id}
- **Nome:** {nome}
- **Local:** {local}
- **Template:** {template}
- **Criado em:** {criado_em}
- **Gerado em:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Resumo
- Conforme: {counts["Conforme"]}
- Atenção: {counts["Atenção"]}
- Não conforme: {counts["Não conforme"]}
- Total de itens: {counts["Total"]}

## Checklist Detalhado
"""

    for i, r in enumerate(respostas, start=1):
        obs = r.get("observacao") or "Nenhuma"
        md += f"""
### Item {i}
- Pergunta: {r.get('item', '')}
- Status: {r.get('status', '')}
- Observação: {obs}
"""

    nao_conformes = [r for r in respostas if r.get("status") == "Não conforme"]
    md += "\n## Plano de Ação (Não conformidades)\n"

    if not nao_conformes:
        md += "Nenhuma não conformidade registrada.\n"
    else:
        md += "| # | Item | Prioridade | Prazo | Observação | Ação sugerida |\n"
        md += "|---:|---|---|---|---|---|\n"
        for i, r in enumerate(nao_conformes, start=1):
            obs = (r.get("observacao") or "Nenhuma").replace("\n", " ")
            prioridade = r.get("prioridade") or "-"
            prazo = r.get("prazo") or "-"
            acao = "Definir responsável; executar correção; registrar evidência."
            md += f"| {i} | {r.get('item','')} | {prioridade} | {prazo} | {obs} | {acao} |\n"

    return md


def save_report_markdown(markdown: str, audit_id: str) -> str:
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", f"report_{audit_id}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return path
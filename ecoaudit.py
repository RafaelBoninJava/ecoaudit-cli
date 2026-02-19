import json
import os
from datetime import datetime


CHECKLISTS = {
    "Resíduos": [
        "Lixeiras identificadas e disponíveis (orgânico/reciclável/rejeito).",
        "Armazenamento temporário de resíduos adequado e limpo.",
        "Destinação de resíduos com controle/registro (quando aplicável).",
        "Resíduos perigosos armazenados corretamente (quando aplicável).",
        "Equipe orientada sobre descarte correto."
    ],
    "Água": [
        "Sem vazamentos visíveis em torneiras, tubulações e descargas.",
        "Práticas de uso racional implementadas (quando aplicável).",
        "Consumo de água monitorado (conta/registro).",
        "Sem desperdício em áreas externas (lavagens/mangueiras).",
        "Sinalização/ações de conscientização (quando aplicável)."
    ],
    "Energia": [
        "Iluminação eficiente (preferência por LED).",
        "Equipamentos desligados quando fora de uso.",
        "Ar-condicionado com manutenção e uso adequado.",
        "Consumo de energia monitorado (conta/registro).",
        "Ações para redução de consumo implementadas."
    ]
}

def escolher_template():
    templates = {
        "1": "Resíduos",
        "2": "Água",
        "3": "Energia"
    }

    print("\nEscolha o tipo de auditoria:")
    for chave, valor in templates.items():
        print(f"{chave} - {valor}")

    while True:
        opcao = input("Digite o número correspondente: ").strip()
        if opcao in templates:
            return templates[opcao]
        else:
            print("Opção inválida. Tente novamente.")


def main():
    print("=== EcoAudit CLI ===")

    nome = input("Nome da auditoria: ").strip()
    local = input("Local: ").strip()

    template_escolhido = escolher_template()

    print("\n--- Resumo ---")
    print(f"Auditoria: {nome}")
    print(f"Local: {local}")
    print(f"Tipo: {template_escolhido}")

def escolher_status():
    opcoes = {
        "1": "Conforme",
        "2": "Atenção",
        "3": "Não conforme"
    }

    print("Status:")
    print("1 - Conforme")
    print("2 - Atenção")
    print("3 - Não conforme")

    while True:
        opcao = input("Digite o número do status: ").strip()
        if opcao in opcoes:
            return opcoes[opcao]
        print("Opção inválida. Tente novamente.")

def main():
    print("=== EcoAudit CLI ===")

    nome = input("Nome da auditoria: ").strip()
    local = input("Local: ").strip()

    template_escolhido = escolher_template()

    print("\nIniciando checklist...\n")

    itens = CHECKLISTS[template_escolhido]
    respostas = []

    for item in itens:
        print("\nPergunta:", item)

        status = escolher_status()
        observacao = input("Observação (opcional): ").strip()

        respostas.append({
            "item": item,
            "status": status,
            "observacao": observacao
        })
        from datetime import datetime

def main():
    print("=== EcoAudit CLI ===")

    nome = input("Nome da auditoria: ").strip()
    local = input("Local: ").strip()

    template_escolhido = escolher_template()
    print("\nIniciando checklist...\n")

    itens = CHECKLISTS[template_escolhido]
    respostas = []

    for item in itens:
        print("\nPergunta:", item)

        status = escolher_status()
        observacao = input("Observação (opcional): ").strip()

        prioridade = ""
        prazo = ""

        if status == "Não conforme":
            prioridade = input("Prioridade (Baixa/Média/Alta): ").strip()
            prazo = input("Prazo (YYYY-MM-DD, opcional): ").strip()

        respostas.append({
            "item": item,
            "status": status,
            "observacao": observacao,
            "prioridade": prioridade,
            "prazo": prazo
        })

    # ID único para arquivos
    audit_id = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Pastas
    os.makedirs("data/audits", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Salvar JSON
    dados_auditoria = {
        "id": audit_id,
        "nome": nome,
        "local": local,
        "template": template_escolhido,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
        "respostas": respostas
    }

    json_path = f"data/audits/audit_{audit_id}.json"
    with open(json_path, "w", encoding="utf-8") as arquivo:
        json.dump(dados_auditoria, arquivo, indent=4, ensure_ascii=False)

    # Contagem de status
    conforme = sum(1 for r in respostas if r["status"] == "Conforme")
    atencao = sum(1 for r in respostas if r["status"] == "Atenção")
    nao_conforme = sum(1 for r in respostas if r["status"] == "Não conforme")
    total = len(respostas)

    # Markdown
    conteudo_md = f"""# Relatório de Auditoria Ambiental

## Informações Gerais
- **ID:** {audit_id}
- **Nome:** {nome}
- **Local:** {local}
- **Template:** {template_escolhido}
- **Gerado em:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Resumo
- Conforme: {conforme}
- Atenção: {atencao}
- Não conforme: {nao_conforme}
- Total de itens: {total}

## Checklist Detalhado
"""

    for i, r in enumerate(respostas, start=1):
        obs = r["observacao"] if r["observacao"] else "Nenhuma"
        conteudo_md += f"""
### Item {i}
- Pergunta: {r['item']}
- Status: {r['status']}
- Observação: {obs}
"""

    # Plano de Ação
    nao_conformes = [r for r in respostas if r["status"] == "Não conforme"]
    conteudo_md += "\n## Plano de Ação (Não conformidades)\n"

    if not nao_conformes:
        conteudo_md += "Nenhuma não conformidade registrada.\n"
    else:
        conteudo_md += "| # | Item | Prioridade | Prazo | Observação | Ação sugerida |\n"
        conteudo_md += "|---:|---|---|---|---|---|\n"

        for i, r in enumerate(nao_conformes, start=1):
            obs = (r["observacao"] if r["observacao"] else "Nenhuma").replace("\n", " ")
            prioridade = r["prioridade"] if r["prioridade"] else "-"
            prazo = r["prazo"] if r["prazo"] else "-"
            acao = "Definir responsável; executar correção; registrar evidência."
            conteudo_md += f"| {i} | {r['item']} | {prioridade} | {prazo} | {obs} | {acao} |\n"

    md_path = f"reports/report_{audit_id}.md"
    with open(md_path, "w", encoding="utf-8") as arquivo_md:
        arquivo_md.write(conteudo_md)

    print("\nAuditoria salva com sucesso.")
    print(f"- JSON: {json_path}")
    print(f"- Relatório: {md_path}")


    # Criar pasta se não existir e salvar JSON
    os.makedirs("data", exist_ok=True)

    dados_auditoria = {
        "nome": nome,
        "local": local,
        "template": template_escolhido,
        "respostas": respostas
    }

    with open("data/auditoria.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_auditoria, arquivo, indent=4, ensure_ascii=False)

    print("\nAuditoria salva com sucesso em data/auditoria.json")

    # Gerar relatório Markdown
    os.makedirs("reports", exist_ok=True)

    conforme = sum(1 for r in respostas if r["status"] == "Conforme")
    atencao = sum(1 for r in respostas if r["status"] == "Atenção")
    nao_conforme = sum(1 for r in respostas if r["status"] == "Não conforme")
    total = len(respostas)

    conteudo_md = f"""# Relatório de Auditoria Ambiental

## Informações Gerais
- **Nome:** {nome}
- **Local:** {local}
- **Template:** {template_escolhido}

## Resumo
- Conforme: {conforme}
- Atenção: {atencao}
- Não conforme: {nao_conforme}
- Total de itens: {total}

## Checklist Detalhado
"""

    for i, r in enumerate(respostas, start=1):
        obs = r["observacao"] if r["observacao"] else "Nenhuma"
        conteudo_md += f"""
### Item {i}
- Pergunta: {r['item']}
- Status: {r['status']}
- Observação: {obs}
"""
        # Plano de Ação (somente Não conforme)
    nao_conformes = [r for r in respostas if r["status"] == "Não conforme"]

    conteudo_md += "\n## Plano de Ação (Não conformidades)\n"

    if not nao_conformes:
        conteudo_md += "Nenhuma não conformidade registrada.\n"
    else:
        conteudo_md += "| # | Item | Observação | Ação sugerida |\n"
        conteudo_md += "|---:|---|---|---|\n"

        for i, r in enumerate(nao_conformes, start=1):
            obs = r["observacao"] if r["observacao"] else "Nenhuma"
            acao = "Definir responsável e prazo; executar correção; registrar evidência."
            # Evita quebrar tabela se tiver enter
            obs = obs.replace("\n", " ")
            conteudo_md += f"| {i} | {r['item']} | {obs} | {acao} |\n"
    

    with open("reports/relatorio.md", "w", encoding="utf-8") as arquivo_md:
        arquivo_md.write(conteudo_md)

    print("Relatório gerado em reports/relatorio.md")


if __name__ == "__main__":
    main()





            




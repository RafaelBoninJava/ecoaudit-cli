from datetime import datetime
from typing import Any, Dict, List

from .domain import CHECKLISTS, STATUS_OPCOES, TEMPLATES
from .report import build_markdown_report, save_report_markdown
from .storage import list_audit_files, load_audit_json, save_audit_json


def escolher_template() -> str:
    print("\nEscolha o tipo de auditoria:")
    for k, v in TEMPLATES.items():
        print(f"{k} - {v}")

    while True:
        opcao = input("Digite o número correspondente: ").strip()
        if opcao in TEMPLATES:
            return TEMPLATES[opcao]
        print("Opção inválida. Tente novamente.")


def escolher_status() -> str:
    print("Status:")
    print("1 - Conforme")
    print("2 - Atenção")
    print("3 - Não conforme")

    while True:
        opcao = input("Digite o número do status: ").strip()
        if opcao in STATUS_OPCOES:
            return STATUS_OPCOES[opcao]
        print("Opção inválida. Tente novamente.")


def criar_auditoria() -> None:
    print("=== EcoAudit CLI ===")

    nome = input("Nome da auditoria: ").strip()
    local = input("Local: ").strip()
    template = escolher_template()

    print("\nIniciando checklist...\n")

    itens = CHECKLISTS[template]
    respostas: List[Dict[str, Any]] = []

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

    audit_id = datetime.now().strftime("%Y%m%d-%H%M%S")

    audit = {
        "id": audit_id,
        "nome": nome,
        "local": local,
        "template": template,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
        "respostas": respostas
    }

    json_path = save_audit_json(audit, audit_id)
    md = build_markdown_report(audit)
    md_path = save_report_markdown(md, audit_id)

    print("\nAuditoria salva com sucesso.")
    print(f"- JSON: {json_path}")
    print(f"- Relatório: {md_path}")


def listar_auditorias() -> List[str]:
    files = list_audit_files()
    if not files:
        print("\nNenhuma auditoria encontrada ainda.")
        return []

    print("\nAuditorias salvas:")
    for i, f in enumerate(files, start=1):
        print(f"{i} - {f}")
    return files


def ver_detalhes_auditoria(filename: str) -> None:
    audit = load_audit_json(filename)
    respostas = audit.get("respostas", [])

    conforme = sum(1 for r in respostas if r.get("status") == "Conforme")
    atencao = sum(1 for r in respostas if r.get("status") == "Atenção")
    nao_conforme = sum(1 for r in respostas if r.get("status") == "Não conforme")
    total = len(respostas)

    print("\n--- Detalhes da Auditoria ---")
    print(f"ID: {audit.get('id', '-')}")
    print(f"Nome: {audit.get('nome', '-')}")
    print(f"Local: {audit.get('local', '-')}")
    print(f"Template: {audit.get('template', '-')}")
    print(f"Criado em: {audit.get('criado_em', '-')}")
    print(f"Resumo: Conforme={conforme} | Atenção={atencao} | Não conforme={nao_conforme} | Total={total}")


def run_menu() -> None:
    while True:
        print("\n=== Menu EcoAudit ===")
        print("1 - Criar nova auditoria")
        print("2 - Listar auditorias salvas")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_auditoria()

        elif opcao == "2":
            arquivos = listar_auditorias()
            if not arquivos:
                continue

            escolha = input("\nDigite o número para ver detalhes (ou Enter para voltar): ").strip()
            if not escolha:
                continue
            if not escolha.isdigit():
                print("Entrada inválida.")
                continue

            idx = int(escolha)
            if idx < 1 or idx > len(arquivos):
                print("Número fora do intervalo.")
                continue

            ver_detalhes_auditoria(arquivos[idx - 1])

        elif opcao == "3":
            print("Encerrando.")
            break

        else:
            print("Opção inválida.")
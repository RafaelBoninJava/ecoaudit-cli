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


def escolher_template() -> str:
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
        print("Opção inválida. Tente novamente.")


def escolher_status() -> str:
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


def main() -> None:
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


if __name__ == "__main__":
    main()





            




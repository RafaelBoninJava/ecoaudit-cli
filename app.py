import os
import json
import streamlit as st


# =========================
# Helpers (arquivos/JSON)
# =========================
AUDITS_DIR = os.path.join("data", "audits")


def list_audit_files() -> list[str]:
    if not os.path.exists(AUDITS_DIR):
        return []
    files = [f for f in os.listdir(AUDITS_DIR) if f.endswith(".json")]
    files.sort(reverse=True)  # mais recente primeiro
    return files


def load_audit_json(filename: str) -> dict:
    path = os.path.join(AUDITS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_str(value, default="-"):
    return value if value not in (None, "", []) else default


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="EcoAudit Dashboard",
    page_icon="🌿",
    layout="wide",
)

# =========================
# Sidebar
# =========================
st.sidebar.title("EcoAudit")
st.sidebar.caption("Auditorias ambientais • CLI + Dashboard")
st.sidebar.success("Sistema online")

st.sidebar.markdown("### Auditorias")
files = list_audit_files()

if not files:
    st.sidebar.info("Nenhuma auditoria encontrada em data/audits.")
    st.stop()

selected = st.sidebar.selectbox("Selecione uma auditoria", files)

st.sidebar.divider()
st.sidebar.markdown("### Links")
st.sidebar.link_button(
    "Repositório no GitHub",
    "https://github.com/RafaelBoninJava/ecoaudit-cli",
)

# =========================
# Load audit
# =========================
audit = load_audit_json(selected)

# Padroniza chaves (caso algumas venham com letra maiúscula dependendo do JSON)
audit_id = audit.get("id") or audit.get("ID")
nome = audit.get("nome") or audit.get("Nome")
local = audit.get("local") or audit.get("Local")
template = audit.get("template") or audit.get("Template")
criado_em = audit.get("criado_em") or audit.get("Criado em") or audit.get("Criado_em")

respostas = audit.get("respostas", [])
if not isinstance(respostas, list):
    respostas = []

# Contagem de status
conforme = sum(1 for r in respostas if r.get("status") == "Conforme")
atencao = sum(1 for r in respostas if r.get("status") == "Atenção")
nao_conforme = sum(1 for r in respostas if r.get("status") == "Não conforme")
total = len(respostas)

# Alertas principais
if nao_conforme > 0:
    st.error(f"Risco identificado: {nao_conforme} não conformidade(s) exigem plano de ação imediato.")
elif atencao > 0:
    st.warning(f"Existem {atencao} item(ns) em atenção que devem ser monitorados.")
else:
    st.success("Auditoria 100% conforme.")

# =========================
# Header
# =========================
st.title("EcoAudit — Painel de Auditoria Ambiental")
st.caption("Visualização estratégica de auditorias ambientais com indicadores e plano de ação.")
st.write("Painel para visualizar auditorias ambientais geradas pelo EcoAudit CLI.")

st.divider()

# =========================
# Layout: info + resumo
# =========================
left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("Informações da Auditoria")

    st.markdown(f"**ID:** {safe_str(audit_id)}")
    st.markdown(f"**Nome:** {safe_str(nome)}")
    st.markdown(f"**Local:** {safe_str(local)}")
    st.markdown(f"**Template:** {safe_str(template)}")
    st.markdown(f"**Criado em:** {safe_str(criado_em)}")

with right:
    st.subheader("Resumo")

    # cria colunas dos cards
    c1, c2, c3, c4 = st.columns(4)

    conforme_pct = round((conforme / total) * 100, 1) if total else 0
    atencao_pct = round((atencao / total) * 100, 1) if total else 0
    nao_pct = round((nao_conforme / total) * 100, 1) if total else 0

    c1.metric("Conforme", f"{conforme} ({conforme_pct}%)")
    c2.metric("Atenção", f"{atencao} ({atencao_pct}%)")
    c3.metric("Não conforme", f"{nao_conforme} ({nao_pct}%)", delta=f"{nao_conforme} pendência(s)")
    c4.metric("Total de Itens", total)

    # Índice (baseado em conformidade)
    indice = conforme_pct
    if indice >= 90:
        st.success(f"Índice de Conformidade: {indice}% (Excelente)")
    elif indice >= 70:
        st.warning(f"Índice de Conformidade: {indice}% (Atenção)")
    else:
        st.error(f"Índice de Conformidade: {indice}% (Crítico)")

    st.markdown("**Distribuição de status**")
    chart_data = {
        "Conforme": conforme,
        "Atenção": atencao,
        "Não conforme": nao_conforme,
    }
    st.bar_chart(chart_data)

st.divider()

# =========================
# Plano de Ação (não conformidades)
# =========================
st.markdown("## Plano de Ação")

nao_conformes = [r for r in respostas if r.get("status") == "Não conforme"]

if nao_conformes:
    # Garante colunas consistentes e mais “profissional” na tabela
    rows = []
    for i, r in enumerate(nao_conformes, start=1):
        rows.append(
            {
                "#": i,
                "Item": r.get("item", ""),
                "Observação": r.get("observacao", "") or "Nenhuma",
                "Prioridade": r.get("prioridade", "") or "-",
                "Prazo": r.get("prazo", "") or "-",
            }
        )
    st.dataframe(rows, use_container_width=True)
else:
    st.success("Nenhuma não conformidade encontrada.")

st.divider()

# =========================
# Checklist detalhado
# =========================
st.subheader("Checklist (Detalhado)")

if not respostas:
    st.info("Esta auditoria não possui respostas.")
else:
    rows = []
    for i, r in enumerate(respostas, start=1):
        rows.append(
            {
                "#": i,
                "Item": r.get("item", ""),
                "Status": r.get("status", ""),
                "Observação": r.get("observacao", "") or "Nenhuma",
                "Prioridade": r.get("prioridade", "") or "-",
                "Prazo": r.get("prazo", "") or "-",
            }
        )
    st.dataframe(rows, use_container_width=True)
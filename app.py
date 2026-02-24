import os
import streamlit as st

from ecoaudit.storage import list_audit_files, load_audit_json
from ecoaudit.report import build_markdown_report

st.set_page_config(page_title="EcoAudit Dashboard", page_icon="🌱", layout="wide")

st.title("EcoAudit — Painel de Auditoria Ambiental")
st.caption("Visualização estratégica de auditorias ambientais com indicadores e plano de ação.")
st.caption("Painel para visualizar auditorias ambientais geradas pelo EcoAudit CLI.")

# --- Sidebar ---
st.sidebar.header("Auditorias")
files = list_audit_files()

if not files:
    st.sidebar.info("Nenhuma auditoria encontrada em data/audits.")
    st.stop()

selected = st.sidebar.selectbox("Selecione uma auditoria", files)

audit = load_audit_json(selected)
respostas = audit.get("respostas", [])

conforme = sum(1 for r in respostas if r.get("status") == "Conforme")
atencao = sum(1 for r in respostas if r.get("status") == "Atenção")
nao_conforme = sum(1 for r in respostas if r.get("status") == "Não conforme")
total = len(respostas)

# --- Header info ---
left, right = st.columns([2, 3], gap="large")

with left:
    st.subheader("Informações da Auditoria")

    st.markdown(f"""
    **ID:** {audit.get("id", "-")}  
    **Nome:** {audit.get("nome", "-")}  
    **Local:** {audit.get("local", "-")}  
    **Template:** {audit.get("template", "-")}  
    **Criado em:** {audit.get("criado_em", "-")}
    """)

with right:
    st.subheader("Resumo")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Conforme", conforme)
    c2.metric("Atenção", atencao)
    delta_txt = "pendência" if nao_conforme == 1 else "pendências"
    c3.metric("Não conforme", nao_conforme, delta=f"{nao_conforme} {delta_txt}")
    c4.metric("Total de Itens", total)

    st.markdown("**Distribuição de status**")
    chart_data = {
        "Conforme": conforme,
        "Atenção": atencao,
        "Não conforme": nao_conforme,
    }
    st.bar_chart(chart_data)

st.divider()

# --- Checklist table (clean view) ---
st.subheader("Checklist (Detalhado)")

view_rows = []
for r in respostas:
    view_rows.append(
        {
            "Item": r.get("item", ""),
            "Status": r.get("status", ""),
            "Observação": r.get("observacao", "") or "—",
            "Prioridade": r.get("prioridade", "") or "—",
            "Prazo": r.get("prazo", "") or "—",
        }
    )

st.dataframe(view_rows, use_container_width=True, hide_index=True)

st.divider()

# --- Action plan (only if needed) ---
st.subheader("Plano de Ação (Não conformidades)")

nao_conformes = [r for r in respostas if r.get("status") == "Não conforme"]

if not nao_conformes:
    st.success("Nenhuma não conformidade registrada.")
else:
    plan = []
    for r in nao_conformes:
        plan.append(
            {
                "Item": r.get("item", ""),
                "Prioridade": r.get("prioridade", "") or "—",
                "Prazo": r.get("prazo", "") or "—",
                "Observação": r.get("observacao", "") or "—",
                "Ação sugerida": "Definir responsável; executar correção; registrar evidência.",
            }
        )
    st.dataframe(plan, use_container_width=True, hide_index=True)

st.divider()

# --- Reports download ---
st.subheader("Relatórios")

audit_id = audit.get("id", "")
md_path = os.path.join("reports", f"report_{audit_id}.md")
csv_path = os.path.join("reports", f"report_{audit_id}.csv")

colA, colB = st.columns(2, gap="large")

with colA:
    st.write("**Markdown (.md)**")
    st.code(md_path)
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            st.download_button(
                "Baixar relatório Markdown",
                f.read(),
                file_name=f"report_{audit_id}.md",
                mime="text/markdown",
                use_container_width=True,
            )
    else:
        st.warning("Arquivo .md não encontrado.")

with colB:
    st.write("**CSV (.csv)**")
    st.code(csv_path)
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            st.download_button(
                "Baixar relatório CSV",
                f,
                file_name=f"report_{audit_id}.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.warning("Arquivo .csv não encontrado.")

st.divider()

# --- Markdown preview ---
with st.expander("Prévia do relatório (Markdown)", expanded=False):
    st.markdown(build_markdown_report(audit))
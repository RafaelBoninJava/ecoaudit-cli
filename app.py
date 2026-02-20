import os
import streamlit as st

from ecoaudit.storage import list_audit_files, load_audit_json
from ecoaudit.report import build_markdown_report

st.set_page_config(page_title="EcoAudit Dashboard", layout="wide")

st.title("EcoAudit Dashboard")
st.caption("Visualização de auditorias ambientais geradas pelo EcoAudit CLI.")

col1, col2 = st.columns([2, 3], gap="large")

with col1:
    st.subheader("Auditorias salvas")
    files = list_audit_files()

    if not files:
        st.info("Nenhuma auditoria encontrada em data/audits. Crie uma auditoria pelo CLI primeiro (python main.py).")
        st.stop()

    selected = st.selectbox("Selecione uma auditoria", files)

with col2:
    audit = load_audit_json(selected)
    respostas = audit.get("respostas", [])

    conforme = sum(1 for r in respostas if r.get("status") == "Conforme")
    atencao = sum(1 for r in respostas if r.get("status") == "Atenção")
    nao_conforme = sum(1 for r in respostas if r.get("status") == "Não conforme")
    total = len(respostas) if respostas else 1

    st.subheader("Resumo")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Conforme", conforme)
    m2.metric("Atenção", atencao)
    m3.metric("Não conforme", nao_conforme)
    m4.metric("Total", len(respostas))
    st.subheader("Distribuição de status")

    chart_data = {
        "Conforme": conforme,
        "Atenção": atencao,
        "Não conforme": nao_conforme,
}

    st.bar_chart(chart_data)

    st.divider()

    st.subheader("Informações")
    st.write(
        {
            "ID": audit.get("id"),
            "Nome": audit.get("nome"),
            "Local": audit.get("local"),
            "Template": audit.get("template"),
            "Criado em": audit.get("criado_em"),
        }
    )

    st.divider()

    st.subheader("Checklist")
    st.dataframe(respostas, use_container_width=True)

    st.divider()

    st.subheader("Relatórios")
    audit_id = audit.get("id", "")
    md_path = os.path.join("reports", f"report_{audit_id}.md")
    csv_path = os.path.join("reports", f"report_{audit_id}.csv")

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Markdown**:", md_path)
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                st.download_button("Baixar relatório .md", f.read(), file_name=f"report_{audit_id}.md")
        else:
            st.warning("Arquivo .md não encontrado.")

    with c2:
        st.write("**CSV**:", csv_path)
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                st.download_button("Baixar relatório .csv", f, file_name=f"report_{audit_id}.csv")
        else:
            st.warning("Arquivo .csv não encontrado.")

    st.divider()

    st.subheader("Prévia do relatório (Markdown)")
    st.markdown(build_markdown_report(audit))
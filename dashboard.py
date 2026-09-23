"""Streamlit dashboard for R&D Services metrics.

Run locally with:
    streamlit run dashboard.py
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="R&D Services Metrics",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_service_data() -> pd.DataFrame:
    """Return the supplied R&D service metrics."""
    return pd.DataFrame(
        [
            {
                "Category": "Project Coordination",
                "Tickets": 313,
                "Saving Hours": 3003.5,
                "Savings (week)": 79,
            },
            {
                "Category": "Testing",
                "Tickets": 40,
                "Saving Hours": 914,
                "Savings (week)": 24,
            },
            {
                "Category": "Documentation",
                "Tickets": 596,
                "Saving Hours": 4643,
                "Savings (week)": 122,
            },
        ]
    )


def apply_chart_theme(fig):
    """Apply a consistent readable theme to Plotly charts."""
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
    )
    return fig


def main() -> None:
    data = load_service_data()

    st.title("R&D Services Metrics Dashboard")
    st.caption("Overview of tickets received, saving hours, and weekly savings by category")

    total_tickets = int(data["Tickets"].sum())
    total_hours = float(data["Saving Hours"].sum())
    total_weekly_savings = int(data["Savings (week)"].sum())

    kpi_tickets, kpi_hours, kpi_weeks = st.columns(3)
    kpi_tickets.metric("Total Tickets Received", f"{total_tickets:,}")
    kpi_hours.metric("Total Saving Hours", f"{total_hours:,.1f}")
    kpi_weeks.metric("Total Savings (Week)", f"{total_weekly_savings:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        ticket_chart = px.pie(
            data,
            names="Category",
            values="Tickets",
            hole=0.45,
            title="Tickets Received by Category",
            color_discrete_sequence=["#2563eb", "#16a34a", "#f97316"],
        )
        ticket_chart.update_traces(textinfo="label+percent", hovertemplate="%{label}: %{value:,}<extra></extra>")
        st.plotly_chart(apply_chart_theme(ticket_chart), use_container_width=True)

    with right:
        hours_chart = px.bar(
            data,
            x="Category",
            y="Saving Hours",
            text="Saving Hours",
            title="Saving Hours by Category",
            color="Category",
            color_discrete_sequence=["#2563eb", "#16a34a", "#f97316"],
        )
        hours_chart.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
        hours_chart.update_layout(showlegend=False, yaxis_title="Hours", xaxis_title="")
        st.plotly_chart(apply_chart_theme(hours_chart), use_container_width=True)

    weekly_chart = px.bar(
        data,
        x="Category",
        y="Savings (week)",
        text="Savings (week)",
        title="Savings (Week) by Category",
        color="Category",
        color_discrete_sequence=["#2563eb", "#16a34a", "#f97316"],
    )
    weekly_chart.update_traces(textposition="outside")
    weekly_chart.update_layout(showlegend=False, yaxis_title="Savings (week)", xaxis_title="")
    st.plotly_chart(apply_chart_theme(weekly_chart), use_container_width=True)

    st.subheader("Service Metrics Detail")
    st.dataframe(
        data.style.format(
            {"Tickets": "{:,.0f}", "Saving Hours": "{:,.1f}", "Savings (week)": "{:,.0f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download metrics as CSV",
        data=csv_data,
        file_name="rnd_services_metrics.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()

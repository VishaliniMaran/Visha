"""R&D Services Metrics dashboard.

Run locally:
    python -m pip install -r requirements.txt
    streamlit run dashboard.py
"""

from __future__ import annotations

import io

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="R&D Services Metrics",
    page_icon="📊",
    layout="wide",
)


CATEGORY_COLORS = {
    "Project Coordination": "#2563eb",
    "Testing": "#16a34a",
    "Documentation": "#f97316",
}


@st.cache_data
def load_metrics() -> pd.DataFrame:
    """Return the R&D service metrics supplied by the user."""
    return pd.DataFrame(
        [
            {"Category": "Project Coordination", "Tickets": 313, "Saving Hours": 3003.5, "Savings (Week)": 79},
            {"Category": "Testing", "Tickets": 40, "Saving Hours": 914, "Savings (Week)": 24},
            {"Category": "Documentation", "Tickets": 596, "Saving Hours": 4643, "Savings (Week)": 122},
        ]
    )


def chart_layout(fig):
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=65, b=20),
        legend_title_text="",
        font=dict(color="#172033"),
    )
    return fig


def main() -> None:
    data = load_metrics()

    st.title("R&D Services Metrics Dashboard")
    st.caption("Tickets received, saving hours, and weekly savings by category")

    total_tickets = int(data["Tickets"].sum())
    total_hours = float(data["Saving Hours"].sum())
    total_weeks = int(data["Savings (Week)"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets Received", f"{total_tickets:,}")
    col2.metric("Total Saving Hours", f"{total_hours:,.1f}")
    col3.metric("Total Savings (Week)", f"{total_weeks:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        pie = px.pie(
            data,
            names="Category",
            values="Tickets",
            hole=0.45,
            title="Tickets Received by Category",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
        )
        pie.update_traces(
            textinfo="label+percent",
            hovertemplate="%{label}: %{value:,} tickets<extra></extra>",
        )
        st.plotly_chart(chart_layout(pie), use_container_width=True)

    with right:
        hours = px.bar(
            data,
            x="Category",
            y="Saving Hours",
            text="Saving Hours",
            title="Saving Hours by Category",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
        )
        hours.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
        hours.update_layout(showlegend=False, xaxis_title="", yaxis_title="Saving hours")
        st.plotly_chart(chart_layout(hours), use_container_width=True)

    weekly = px.bar(
        data,
        x="Category",
        y="Savings (Week)",
        text="Savings (Week)",
        title="Savings (Week) by Category",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
    )
    weekly.update_traces(textposition="outside")
    weekly.update_layout(showlegend=False, xaxis_title="", yaxis_title="Savings (week)")
    st.plotly_chart(chart_layout(weekly), use_container_width=True)

    st.subheader("R&D Services Metrics")
    st.dataframe(
        data.style.format(
            {"Tickets": "{:,.0f}", "Saving Hours": "{:,.1f}", "Savings (Week)": "{:,.0f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv_file = io.StringIO()
    data.to_csv(csv_file, index=False)
    st.download_button(
        "⬇ Export metrics as CSV",
        data=csv_file.getvalue(),
        file_name="rnd_services_metrics.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()

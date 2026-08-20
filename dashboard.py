import streamlit as st
import pandas as pd
import plotly.express as px


def load_service_data():
    data = [
        {
            "Category": "Project Coordination",
            "Description": "End-to-end planning, milestone management, and coordination for high-impact R&D initiatives.",
            "Tickets": 313,
            "Saving Hours": 3003.5,
            "Savings (week)": 79,
            "Key Features": ["Resource alignment", "Stakeholder coordination", "Milestone tracking"],
            "Benefits": ["Faster project execution", "Lower operational friction", "Improved accountability"],
        },
        {
            "Category": "Testing",
            "Description": "Structured validation and verification to ensure quality, reliability, and performance outcomes.",
            "Tickets": 4,
            "Saving Hours": 914,
            "Savings (week)": 24,
            "Key Features": ["Functional validation", "Regression checks", "Defect reduction"],
            "Benefits": ["Improved reliability", "Fewer delays", "Better product confidence"],
        },
        {
            "Category": "Documentation",
            "Description": "Clear technical writing and documentation support that improves execution, compliance, and knowledge transfer.",
            "Tickets": 13,
            "Saving Hours": 4643,
            "Savings (week)": 122,
            "Key Features": ["Requirement tracking", "Technical writing", "Knowledge capture"],
            "Benefits": ["Stronger traceability", "Shorter onboarding", "More consistent delivery"],
        },
    ]
    return pd.DataFrame(data)


def load_weekly_savings_data():
    return pd.DataFrame(
        [
            {"Week": "W1", "Project Coordination": 12, "Testing": 4, "Documentation": 16, "Total Weekly Savings": 32},
            {"Week": "W2", "Project Coordination": 15, "Testing": 6, "Documentation": 18, "Total Weekly Savings": 39},
            {"Week": "W3", "Project Coordination": 18, "Testing": 8, "Documentation": 21, "Total Weekly Savings": 47},
            {"Week": "W4", "Project Coordination": 17, "Testing": 7, "Documentation": 20, "Total Weekly Savings": 44},
            {"Week": "W5", "Project Coordination": 21, "Testing": 9, "Documentation": 23, "Total Weekly Savings": 53},
            {"Week": "W6", "Project Coordination": 24, "Testing": 10, "Documentation": 28, "Total Weekly Savings": 62},
            {"Week": "W7", "Project Coordination": 23, "Testing": 11, "Documentation": 30, "Total Weekly Savings": 64},
            {"Week": "W8", "Project Coordination": 26, "Testing": 12, "Documentation": 33, "Total Weekly Savings": 71},
        ]
    )


def render_overview():
    st.title("CMY R&D")
    st.subheader("Research-driven solutions for smarter, faster delivery")
    st.markdown(
        """
        CMY R&D is focused on helping teams innovate with confidence by combining research expertise,
        structured project coordination, and quality-driven delivery support. We help organizations move
        from idea to implementation with clear execution plans, dependable testing, and practical documentation.
        """
    )

    st.markdown("### Mission, Vision, and Values")
    mission, vision, values = st.columns(3)

    with mission:
        st.markdown(
            """
            <div style='padding:1rem; border-radius:0.75rem; background:#eef6ff; border:1px solid #cfe2ff;'>
            <b>Mission</b><br>
            To support innovation and operational excellence through disciplined research, coordination, and quality assurance.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with vision:
        st.markdown(
            """
            <div style='padding:1rem; border-radius:0.75rem; background:#f4f0ff; border:1px solid #d9d2f4;'>
            <b>Vision</b><br>
            To be a trusted R&D partner that turns complex challenges into scalable, measurable outcomes.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with values:
        st.markdown(
            """
            <div style='padding:1rem; border-radius:0.75rem; background:#f8fff0; border:1px solid #d4f4c4;'>
            <b>Core Values</b><br>
            Innovation, accountability, collaboration, quality, and continuous improvement.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")


def render_services(df):
    st.subheader("Services Offered")
    st.markdown(
        """
        CMY R&D delivers practical, research-backed services that reduce delays, improve quality, and strengthen project execution.
        """
    )

    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"### {row['Category']}")
            st.write(row["Description"])

            feature_col, benefit_col = st.columns(2)

            with feature_col:
                st.markdown("**Key Features**")
                for item in row["Key Features"]:
                    st.markdown(f"- {item}")

            with benefit_col:
                st.markdown("**Client Benefits**")
                for item in row["Benefits"]:
                    st.markdown(f"- {item}")

            st.markdown("---")


def main():
    st.set_page_config(page_title="CMY R&D Services Dashboard", layout="wide")

    service_df = load_service_data()
    weekly_df = load_weekly_savings_data()

    render_overview()

    total_tickets = int(service_df["Tickets"].sum())
    total_saving_hours = float(service_df["Saving Hours"].sum())
    total_weekly_savings = int(service_df["Savings (week)"].sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tickets Received", f"{total_tickets}")
    c2.metric("Total Saving Hours", f"{total_saving_hours:,.1f}")
    c3.metric("Total Weekly Savings", f"{total_weekly_savings}")

    st.markdown("---")
    render_services(service_df)

    st.subheader("Operational Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(df, x="Category", y="Saving Hours", text="Saving Hours",
                         title="Saving Hours by Category", labels={"Saving Hours": "Saving Hours"})
        fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title='Saving Hours')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(df, names="Category", values="Tickets", title="Ticket Distribution by Category")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Weekly Savings")
    fig_line = px.bar(df, x="Category", y="Savings (week)", title="Weekly Savings by Category",
                      labels={"Savings (week)": "Savings (week)"}, text="Savings (week)")
    fig_line.update_traces(textposition="outside")
    st.plotly_chart(fig_line, use_container_width=True)

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download data as CSV", data=csv, file_name="services_data.csv", mime="text/csv")


if __name__ == "__main__":
    main()

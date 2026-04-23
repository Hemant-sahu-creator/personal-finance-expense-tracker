import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import json
from datetime import datetime, date
import calendar
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💰 Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0f0f;
    color: #f0f0f0;
}

.main { background-color: #0f0f0f; }

h1, h2, h3 {
    font-family: 'Space Mono', monospace;
}

.metric-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #00d4aa33;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00d4aa;
}

.metric-label {
    font-size: 0.8rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.category-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
}

.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #0099cc);
    color: #0f0f0f;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 0.9rem;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px #00d4aa44;
}

.stSelectbox > div, .stNumberInput > div, .stTextInput > div {
    background-color: #1a1a2e !important;
    border-color: #00d4aa33 !important;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f0f 0%, #1a1a2e 100%);
    border-right: 1px solid #00d4aa22;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 1.2rem;
    color: #00d4aa;
    border-bottom: 1px solid #00d4aa33;
    padding-bottom: 8px;
    margin-bottom: 20px;
}

.success-msg {
    background: #00d4aa22;
    border: 1px solid #00d4aa;
    border-radius: 8px;
    padding: 12px 16px;
    color: #00d4aa;
    font-weight: 600;
}

.warning-msg {
    background: #ff6b3522;
    border: 1px solid #ff6b35;
    border-radius: 8px;
    padding: 12px 16px;
    color: #ff6b35;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
CATEGORIES = [
    "Food & Dining", "Transportation", "Housing & Rent",
    "Shopping", "Entertainment", "Healthcare", "Education",
    "Travel", "Utilities", "Personal Care", "Investment", "Other"
]

CATEGORY_COLORS = {
    "Food & Dining": "#ff6b35",
    "Transportation": "#00d4aa",
    "Housing & Rent": "#7c5cbf",
    "Shopping": "#ffd700",
    "Entertainment": "#ff4d9e",
    "Healthcare": "#4dd9ff",
    "Education": "#a8ff78",
    "Travel": "#ff9f43",
    "Utilities": "#81ecec",
    "Personal Care": "#fd79a8",
    "Investment": "#55efc4",
    "Other": "#b2bec3"
}

DATA_FILE = "expenses.csv"

# ── Data Functions ────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["date"])
        return df
    else:
        return pd.DataFrame(columns=["date", "category", "amount", "description", "payment_method"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_expense(date_val, category, amount, description, payment_method):
    df = load_data()
    new_row = pd.DataFrame([{
        "date": pd.to_datetime(date_val),
        "category": category,
        "amount": float(amount),
        "description": description,
        "payment_method": payment_method
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    return df

def get_monthly_summary(df):
    if df.empty:
        return pd.DataFrame()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    return df.groupby("month")["amount"].agg(["sum", "count", "mean"]).reset_index()

def get_category_summary(df):
    if df.empty:
        return pd.DataFrame()
    return df.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)

# ── Chart Style ───────────────────────────────────────────────────────────────
def apply_dark_style():
    plt.rcParams.update({
        "figure.facecolor": "#0f0f0f",
        "axes.facecolor": "#1a1a2e",
        "axes.edgecolor": "#00d4aa33",
        "axes.labelcolor": "#888",
        "xtick.color": "#888",
        "ytick.color": "#888",
        "text.color": "#f0f0f0",
        "grid.color": "#00d4aa11",
        "grid.linestyle": "--",
        "font.family": "monospace",
    })

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 Finance Tracker")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Expense", "📋 All Expenses", "📈 Analytics", "📄 Monthly Report"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    df_all = load_data()
    if not df_all.empty:
        total = df_all["amount"].sum()
        st.markdown(f"**Total Spent:** ₹{total:,.0f}")
        st.markdown(f"**Transactions:** {len(df_all)}")
    else:
        st.info("No data yet. Add your first expense!")

# ── Dashboard Page ────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown("# 📊 Dashboard")
    df = load_data()

    if df.empty:
        st.markdown("""
        <div class="warning-msg">
        No expenses yet! Go to <b>➕ Add Expense</b> to add your first transaction, 
        or use the <b>Load Sample Data</b> button below.
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱 Load Sample Data"):
            sample_data = []
            categories = CATEGORIES[:-1]
            for i in range(50):
                sample_data.append({
                    "date": pd.to_datetime(f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,28):02d}"),
                    "category": np.random.choice(categories),
                    "amount": round(np.random.uniform(100, 5000), 2),
                    "description": f"Sample expense {i+1}",
                    "payment_method": np.random.choice(["Cash", "UPI", "Card", "Net Banking"])
                })
            df = pd.DataFrame(sample_data)
            save_data(df)
            st.rerun()
    else:
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        total_spent = df["amount"].sum()
        avg_per_txn = df["amount"].mean()
        top_category = df.groupby("category")["amount"].sum().idxmax()
        this_month = df[pd.to_datetime(df["date"]).dt.month == datetime.now().month]["amount"].sum()

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Spent</div>
                <div class="metric-value">₹{total_spent:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">This Month</div>
                <div class="metric-value">₹{this_month:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg per Transaction</div>
                <div class="metric-value">₹{avg_per_txn:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Category</div>
                <div class="metric-value" style="font-size:1.1rem">{top_category}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        col_left, col_right = st.columns([1, 1])

        # Pie Chart
        with col_left:
            st.markdown('<div class="section-header">Spending by Category</div>', unsafe_allow_html=True)
            cat_df = get_category_summary(df)
            apply_dark_style()
            fig, ax = plt.subplots(figsize=(6, 5))
            colors = [CATEGORY_COLORS.get(c, "#888") for c in cat_df["category"]]
            wedges, texts, autotexts = ax.pie(
                cat_df["amount"], labels=None,
                colors=colors, autopct="%1.1f%%",
                pctdistance=0.75, startangle=90,
                wedgeprops=dict(width=0.6, edgecolor="#0f0f0f", linewidth=2)
            )
            for at in autotexts:
                at.set_color("#f0f0f0")
                at.set_fontsize(8)
            ax.legend(
                cat_df["category"], loc="lower center",
                bbox_to_anchor=(0.5, -0.15), ncol=2,
                fontsize=7, framealpha=0, labelcolor="#ccc"
            )
            ax.set_title("Category Breakdown", color="#00d4aa", pad=10, fontsize=11)
            fig.patch.set_facecolor("#0f0f0f")
            st.pyplot(fig)
            plt.close()

        # Monthly Bar Chart
        with col_right:
            st.markdown('<div class="section-header">Monthly Spending Trend</div>', unsafe_allow_html=True)
            df["month_str"] = pd.to_datetime(df["date"]).dt.strftime("%b %Y")
            monthly = df.groupby("month_str")["amount"].sum().reset_index()
            monthly["date_sort"] = pd.to_datetime(monthly["month_str"], format="%b %Y")
            monthly = monthly.sort_values("date_sort")

            apply_dark_style()
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            bars = ax2.bar(
                monthly["month_str"], monthly["amount"],
                color="#00d4aa", alpha=0.85,
                edgecolor="#0f0f0f", linewidth=1.5,
                width=0.6
            )
            ax2.set_xlabel("Month", fontsize=9)
            ax2.set_ylabel("Amount (₹)", fontsize=9)
            ax2.set_title("Month-wise Expenses", color="#00d4aa", pad=10, fontsize=11)
            plt.xticks(rotation=45, ha="right", fontsize=7)
            ax2.grid(axis="y", alpha=0.3)
            fig2.patch.set_facecolor("#0f0f0f")
            st.pyplot(fig2)
            plt.close()

        # Recent Transactions
        st.markdown("---")
        st.markdown('<div class="section-header">Recent Transactions</div>', unsafe_allow_html=True)
        recent = df.sort_values("date", ascending=False).head(8)
        recent["date"] = pd.to_datetime(recent["date"]).dt.strftime("%d %b %Y")
        recent["amount"] = recent["amount"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(
            recent[["date", "category", "amount", "description", "payment_method"]],
            use_container_width=True,
            hide_index=True
        )

# ── Add Expense Page ──────────────────────────────────────────────────────────
elif page == "➕ Add Expense":
    st.markdown("# ➕ Add New Expense")
    st.markdown("")

    col1, col2 = st.columns([1, 1])
    with col1:
        expense_date = st.date_input("📅 Date", value=date.today())
        category = st.selectbox("🗂️ Category", CATEGORIES)
        amount = st.number_input("💵 Amount (₹)", min_value=0.01, step=10.0, format="%.2f")

    with col2:
        description = st.text_input("📝 Description", placeholder="e.g., Lunch at restaurant")
        payment_method = st.selectbox("💳 Payment Method", ["UPI", "Cash", "Credit Card", "Debit Card", "Net Banking"])
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.button("✅ Add Expense")

    if submit:
        if amount > 0 and description.strip():
            add_expense(expense_date, category, amount, description, payment_method)
            st.markdown(f"""
            <div class="success-msg">
            ✅ Expense of ₹{amount:,.2f} added under <b>{category}</b>!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-msg">⚠️ Please fill all fields and enter a valid amount.</div>', unsafe_allow_html=True)

# ── All Expenses Page ─────────────────────────────────────────────────────────
elif page == "📋 All Expenses":
    st.markdown("# 📋 All Expenses")
    df = load_data()

    if df.empty:
        st.info("No expenses found. Add some expenses first!")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            cat_filter = st.multiselect("Filter by Category", CATEGORIES, default=CATEGORIES)
        with col2:
            method_filter = st.multiselect("Payment Method", ["UPI", "Cash", "Credit Card", "Debit Card", "Net Banking"],
                                           default=["UPI", "Cash", "Credit Card", "Debit Card", "Net Banking"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Amount (High)", "Amount (Low)"])

        filtered = df[df["category"].isin(cat_filter) & df["payment_method"].isin(method_filter)]

        if sort_by == "Date (Newest)":
            filtered = filtered.sort_values("date", ascending=False)
        elif sort_by == "Date (Oldest)":
            filtered = filtered.sort_values("date", ascending=True)
        elif sort_by == "Amount (High)":
            filtered = filtered.sort_values("amount", ascending=False)
        else:
            filtered = filtered.sort_values("amount", ascending=True)

        st.markdown(f"**Showing {len(filtered)} transactions | Total: ₹{filtered['amount'].sum():,.2f}**")
        display_df = filtered.copy()
        display_df["date"] = pd.to_datetime(display_df["date"]).dt.strftime("%d %b %Y")
        display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df[["date", "category", "amount", "description", "payment_method"]],
                     use_container_width=True, hide_index=True)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "expenses.csv", "text/csv")

# ── Analytics Page ────────────────────────────────────────────────────────────
elif page == "📈 Analytics":
    st.markdown("# 📈 Analytics")
    df = load_data()

    if df.empty:
        st.info("No data to analyze yet!")
    else:
        df["date"] = pd.to_datetime(df["date"])
        df["weekday"] = df["date"].dt.day_name()
        df["week"] = df["date"].dt.isocalendar().week

        col1, col2 = st.columns(2)

        # Spending by weekday
        with col1:
            st.markdown('<div class="section-header">Spending by Day of Week</div>', unsafe_allow_html=True)
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_df = df.groupby("weekday")["amount"].sum().reindex(day_order, fill_value=0)
            apply_dark_style()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors_bar = ["#00d4aa" if d in ["Saturday", "Sunday"] else "#7c5cbf" for d in day_order]
            ax.bar(day_df.index, day_df.values, color=colors_bar, edgecolor="#0f0f0f", linewidth=1.5)
            ax.set_title("Weekday vs Weekend Spending", color="#00d4aa", fontsize=10)
            plt.xticks(rotation=30, ha="right", fontsize=7)
            ax.grid(axis="y", alpha=0.3)
            fig.patch.set_facecolor("#0f0f0f")
            st.pyplot(fig)
            plt.close()

        # Category heatmap
        with col2:
            st.markdown('<div class="section-header">Category vs Payment Method</div>', unsafe_allow_html=True)
            pivot = df.pivot_table(values="amount", index="category", columns="payment_method", aggfunc="sum", fill_value=0)
            apply_dark_style()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.heatmap(pivot, ax=ax2, cmap="YlOrRd", linewidths=0.5,
                        linecolor="#0f0f0f", annot=True, fmt=".0f",
                        annot_kws={"size": 6}, cbar_kws={"shrink": 0.8})
            ax2.set_title("Spending Heatmap", color="#00d4aa", fontsize=10)
            ax2.set_xlabel("")
            ax2.set_ylabel("")
            plt.xticks(fontsize=6, rotation=20)
            plt.yticks(fontsize=6)
            fig2.patch.set_facecolor("#0f0f0f")
            st.pyplot(fig2)
            plt.close()

        # Box plot
        st.markdown('<div class="section-header">Expense Distribution per Category</div>', unsafe_allow_html=True)
        top_cats = df.groupby("category")["amount"].sum().nlargest(6).index
        df_top = df[df["category"].isin(top_cats)]
        apply_dark_style()
        fig3, ax3 = plt.subplots(figsize=(12, 4))
        colors_box = [CATEGORY_COLORS.get(c, "#888") for c in top_cats]
        bp = ax3.boxplot(
            [df_top[df_top["category"] == c]["amount"].values for c in top_cats],
            labels=top_cats, patch_artist=True, notch=False,
            medianprops=dict(color="#fff", linewidth=2)
        )
        for patch, color in zip(bp["boxes"], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax3.set_title("Expense Spread by Category (Top 6)", color="#00d4aa", fontsize=10)
        plt.xticks(fontsize=8)
        ax3.grid(axis="y", alpha=0.3)
        fig3.patch.set_facecolor("#0f0f0f")
        st.pyplot(fig3)
        plt.close()

# ── Monthly Report Page ───────────────────────────────────────────────────────
elif page == "📄 Monthly Report":
    st.markdown("# 📄 Monthly Report")
    df = load_data()

    if df.empty:
        st.info("No data available for report!")
    else:
        df["date"] = pd.to_datetime(df["date"])
        months = df["date"].dt.to_period("M").unique()
        month_strs = sorted([str(m) for m in months], reverse=True)
        selected_month = st.selectbox("Select Month", month_strs)

        month_df = df[df["date"].dt.to_period("M") == selected_month]

        st.markdown(f"### Report for **{selected_month}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Spent", f"₹{month_df['amount'].sum():,.2f}")
        with col2:
            st.metric("Transactions", len(month_df))
        with col3:
            st.metric("Avg per Day", f"₹{month_df['amount'].sum() / max(month_df['date'].dt.day.max(), 1):,.2f}")

        st.markdown("---")
        st.markdown("#### Category Breakdown")
        cat_report = month_df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
        cat_report.columns = ["Category", "Total (₹)", "Count"]
        cat_report["% of Total"] = (cat_report["Total (₹)"] / cat_report["Total (₹)"].sum() * 100).round(1)
        cat_report["Total (₹)"] = cat_report["Total (₹)"].apply(lambda x: f"₹{x:,.2f}")
        cat_report["% of Total"] = cat_report["% of Total"].apply(lambda x: f"{x}%")
        st.dataframe(cat_report, use_container_width=True, hide_index=True)

        st.markdown("#### Top 5 Transactions")
        top5 = month_df.nlargest(5, "amount")[["date", "category", "amount", "description"]]
        top5["date"] = top5["date"].dt.strftime("%d %b %Y")
        top5["amount"] = top5["amount"].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(top5, use_container_width=True, hide_index=True)

        csv = month_df.to_csv(index=False).encode("utf-8")
        st.download_button(f"⬇️ Download {selected_month} Report", csv, f"report_{selected_month}.csv", "text/csv")

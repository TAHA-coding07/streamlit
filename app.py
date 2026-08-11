import os
import json
import datetime
import re

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

APP_TITLE = "Ad Hoc File Transfer Tracker"
APP_ICON = "📡"
DEVELOPER_NAME = "Your Name"
CSV_FILE = "transfers.csv"

COLUMNS = [
    "Transfer ID",
    "File Name",
    "Sender Device",
    "Receiver Device",
    "Owner Name",
    "File Size (MB)",
    "Transfer Date",
    "Connection Type",
    "Transfer Status",
    "Encryption",
    "Notes",
]

CONNECTION_TYPES = [
    "WiFi Direct",
    "Bluetooth",
    "NFC",
    "Hotspot"
]

TRANSFER_STATUSES = [
    "Completed",
    "Pending",
    "Failed"
]

STATUS_COLORS = {
    "Completed": "#28a745",
    "Pending": "#ffc107",
    "Failed": "#dc3545",
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        # Add missing columns if required
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""

        # Keep only required columns
        df = df[COLUMNS]

        # Convert file size to number
        df["File Size (MB)"] = pd.to_numeric(
            df["File Size (MB)"],
            errors="coerce"
        ).fillna(0)

        return df

    # If CSV does not exist
    return pd.DataFrame(columns=COLUMNS)


# ============================================================
# SAVE DATA
# ============================================================

def save_data(df):

    df.to_csv(
        CSV_FILE,
        index=False
    )


# ============================================================
# VALIDATION
# ============================================================

def validate_transfer(
    transfer_id,
    file_name,
    sender,
    receiver,
    owner,
    file_size,
    notes,
    df,
):

    errors = []

    # Required fields
    if not transfer_id.strip():
        errors.append("❌ Transfer ID is required.")

    if not file_name.strip():
        errors.append("❌ File Name is required.")

    if not sender.strip():
        errors.append("❌ Sender Device is required.")

    if not receiver.strip():
        errors.append("❌ Receiver Device is required.")

    if not owner.strip():
        errors.append("❌ Owner Name is required.")

    # File size
    if file_size <= 0:
        errors.append(
            "❌ File Size must be greater than 0."
        )

    # Sender and receiver
    if (
        sender.strip()
        and receiver.strip()
        and sender.strip().lower()
        == receiver.strip().lower()
    ):
        errors.append(
            "❌ Sender and Receiver cannot be the same."
        )

    # Transfer ID uniqueness
    if not df.empty:

        existing_ids = (
            df["Transfer ID"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        if transfer_id.strip().lower() in existing_ids.values:

            errors.append(
                f"❌ Transfer ID '{transfer_id}' already exists."
            )

    # Owner name validation
    if owner.strip():

        if not re.fullmatch(
            r"[A-Za-z .\-]+",
            owner.strip()
        ):
            errors.append(
                "❌ Owner Name can contain only letters, "
                "spaces, dots and hyphens."
            )

    # Notes validation
    if len(notes.strip()) > 200:

        errors.append(
            "❌ Notes cannot exceed 200 characters."
        )

    return errors


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    st.title(
        f"{APP_ICON} {APP_TITLE}"
    )

    st.caption(
        "A tool to manage wireless file transfers between devices"
    )

    with st.expander(
        "👋 Welcome",
        expanded=True
    ):

        st.info(
            "This application helps you track, manage and analyze "
            "file transfers between devices using WiFi Direct, "
            "Bluetooth, NFC or Hotspot."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📖 Domain Description")

        st.write(
            "Ad hoc file transfer allows devices to share files "
            "directly without depending on a central server. "
            "This application records important transfer details "
            "such as sender, receiver, file size, connection type "
            "and transfer status."
        )

    with col2:

        st.subheader("🎯 Objectives")

        st.markdown(
            """
            - Demonstrate Streamlit widgets
            - Collect and validate user data
            - Store transfer records
            - Search and filter records
            - Display charts
            - Download CSV and JSON data
            """
        )

    st.divider()

    st.subheader("✨ Key Features")

    features = [
        "📊 Interactive Dashboard",
        "➕ Add Transfer",
        "✏️ Edit Transfer",
        "🗑️ Delete Transfer",
        "🔎 Search and Filter",
        "📈 Interactive Charts",
        "⬇️ Download CSV and JSON",
    ]

    for feature in features:
        st.markdown(
            f"- {feature}"
        )

    st.divider()

    st.markdown(
        f"""
        <div style="text-align:center;">
            <p>
                Built using Streamlit<br>
                Developed by <b>{DEVELOPER_NAME}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page(df):

    st.title("📊 Dashboard")

    total = len(df)

    completed = len(
        df[df["Transfer Status"] == "Completed"]
    )

    pending = len(
        df[df["Transfer Status"] == "Pending"]
    )

    failed = len(
        df[df["Transfer Status"] == "Failed"]
    )

    if total > 0:

        average = df["File Size (MB)"].mean()
        largest = df["File Size (MB)"].max()
        smallest = df["File Size (MB)"].min()

    else:

        average = 0
        largest = 0
        smallest = 0

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Total Transfers",
        total
    )

    col2.metric(
        "✅ Completed",
        completed
    )

    col3.metric(
        "⏳ Pending",
        pending
    )

    col4.metric(
        "❌ Failed",
        failed
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "📏 Average Size",
        f"{average:.2f} MB"
    )

    col6.metric(
        "⬆️ Largest File",
        f"{largest:.2f} MB"
    )

    col7.metric(
        "⬇️ Smallest File",
        f"{smallest:.2f} MB"
    )

    st.divider()

    if total > 0:

        completion_rate = (
            completed / total
        ) * 100

        st.subheader(
            "📈 Completion Rate"
        )

        st.progress(
            int(completion_rate)
        )

        st.write(
            f"{completion_rate:.1f}% transfers completed."
        )

    st.divider()

    st.subheader(
        "🕒 Recent Transfers"
    )

    if total > 0:

        recent = df.tail(5)[
            [
                "Transfer Date",
                "File Name",
                "Connection Type",
                "Transfer Status"
            ]
        ]

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No transfer records available."
        )


# ============================================================
# ADD TRANSFER
# ============================================================

def add_transfer_page(df):

    st.title("➕ Add Transfer")

    with st.form(
        "add_transfer_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            transfer_id = st.text_input(
                "🆔 Transfer ID",
                placeholder="HT001"
            )

            file_name = st.text_input(
                "📄 File Name",
                placeholder="report.pdf"
            )

            sender = st.text_input(
                "📤 Sender Device",
                placeholder="Laptop"
            )

            file_size = st.number_input(
                "💾 File Size (MB)",
                min_value=0.0,
                step=0.1
            )

        with col2:

            receiver = st.text_input(
                "📥 Receiver Device",
                placeholder="Mobile"
            )

            owner = st.text_input(
                "👤 Owner Name",
                placeholder="John Doe"
            )

            transfer_date = st.date_input(
                "📅 Transfer Date",
                value=datetime.date.today()
            )

            connection_type = st.selectbox(
                "🔗 Connection Type",
                CONNECTION_TYPES
            )

        status = st.radio(
            "🚦 Transfer Status",
            TRANSFER_STATUSES,
            horizontal=True
        )

        encryption = st.checkbox(
            "🔒 Encryption Enabled",
            value=True
        )

        notes = st.text_area(
            "📝 Notes",
            max_chars=200
        )

        submitted = st.form_submit_button(
            "💾 Save Transfer",
            use_container_width=True
        )

    if submitted:

        errors = validate_transfer(
            transfer_id,
            file_name,
            sender,
            receiver,
            owner,
            file_size,
            notes,
            df
        )

        if errors:

            for error in errors:
                st.error(error)

        else:

            new_record = {
                "Transfer ID": transfer_id.strip(),
                "File Name": file_name.strip(),
                "Sender Device": sender.strip(),
                "Receiver Device": receiver.strip(),
                "Owner Name": owner.strip(),
                "File Size (MB)": file_size,
                "Transfer Date": str(transfer_date),
                "Connection Type": connection_type,
                "Transfer Status": status,
                "Encryption": "Yes"
                if encryption
                else "No",
                "Notes": notes.strip()
            }

            new_df = pd.concat(
                [
                    df,
                    pd.DataFrame([new_record])
                ],
                ignore_index=True
            )

            save_data(new_df)

            st.session_state["data"] = new_df

            st.success(
                "✅ Transfer added successfully!"
            )

            st.balloons()


# ============================================================
# VIEW / EDIT / DELETE
# ============================================================

def view_transfers_page(df):

    st.title("📋 View Transfers")

    if df.empty:

        st.warning(
            "No transfer records available."
        )

        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "✏️ Manage Records"
    )

    selected_id = st.selectbox(
        "Select Transfer ID",
        df["Transfer ID"].tolist()
    )

    record = df[
        df["Transfer ID"] == selected_id
    ].iloc[0]

    record_index = df.index[
        df["Transfer ID"] == selected_id
    ][0]

    action = st.radio(
        "Action",
        ["Edit Record", "Delete Record"],
        horizontal=True
    )

    # EDIT

    if action == "Edit Record":

        with st.form("edit_form"):

            file_name = st.text_input(
                "File Name",
                value=record["File Name"]
            )

            sender = st.text_input(
                "Sender Device",
                value=record["Sender Device"]
            )

            receiver = st.text_input(
                "Receiver Device",
                value=record["Receiver Device"]
            )

            owner = st.text_input(
                "Owner Name",
                value=record["Owner Name"]
            )

            file_size = st.number_input(
                "File Size (MB)",
                min_value=0.0,
                value=float(
                    record["File Size (MB)"]
                )
            )

            connection_type = st.selectbox(
                "Connection Type",
                CONNECTION_TYPES,
                index=(
                    CONNECTION_TYPES.index(
                        record["Connection Type"]
                    )
                    if record["Connection Type"]
                    in CONNECTION_TYPES
                    else 0
                )
            )

            status = st.selectbox(
                "Transfer Status",
                TRANSFER_STATUSES,
                index=(
                    TRANSFER_STATUSES.index(
                        record["Transfer Status"]
                    )
                    if record["Transfer Status"]
                    in TRANSFER_STATUSES
                    else 0
                )
            )

            encryption = st.checkbox(
                "Encryption Enabled",
                value=(
                    record["Encryption"] == "Yes"
                )
            )

            notes = st.text_area(
                "Notes",
                value=record["Notes"],
                max_chars=200
            )

            update = st.form_submit_button(
                "💾 Update"
            )

        if update:

            temp_df = df.drop(
                index=record_index
            )

            errors = validate_transfer(
                selected_id,
                file_name,
                sender,
                receiver,
                owner,
                file_size,
                notes,
                temp_df
            )

            if errors:

                for error in errors:
                    st.error(error)

            else:

                df.at[
                    record_index,
                    "File Name"
                ] = file_name.strip()

                df.at[
                    record_index,
                    "Sender Device"
                ] = sender.strip()

                df.at[
                    record_index,
                    "Receiver Device"
                ] = receiver.strip()

                df.at[
                    record_index,
                    "Owner Name"
                ] = owner.strip()

                df.at[
                    record_index,
                    "File Size (MB)"
                ] = file_size

                df.at[
                    record_index,
                    "Connection Type"
                ] = connection_type

                df.at[
                    record_index,
                    "Transfer Status"
                ] = status

                df.at[
                    record_index,
                    "Encryption"
                ] = (
                    "Yes"
                    if encryption
                    else "No"
                )

                df.at[
                    record_index,
                    "Notes"
                ] = notes.strip()

                save_data(df)

                st.session_state["data"] = df

                st.success(
                    "✅ Record updated!"
                )

                st.rerun()

    # DELETE

    else:

        st.warning(
            f"You are about to delete {selected_id}"
        )

        confirm = st.checkbox(
            "I understand this action is permanent."
        )

        if st.button(
            "🗑️ Delete Record"
        ):

            if confirm:

                df = df.drop(
                    index=record_index
                ).reset_index(drop=True)

                save_data(df)

                st.session_state["data"] = df

                st.success(
                    "🗑️ Record deleted!"
                )

                st.rerun()

            else:

                st.error(
                    "Please confirm deletion."
                )


# ============================================================
# SEARCH
# ============================================================

def search_filter_page(df):

    st.title("🔎 Search & Filter")

    if df.empty:

        st.warning(
            "No records available."
        )

        return

    keyword = st.text_input(
        "Search",
        placeholder="Enter file name, device or owner"
    )

    connection_filter = st.multiselect(
        "Connection Type",
        CONNECTION_TYPES
    )

    status_filter = st.multiselect(
        "Transfer Status",
        TRANSFER_STATUSES
    )

    filtered = df.copy()

    if keyword:

        mask = (
            filtered["Transfer ID"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
            |
            filtered["File Name"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
            |
            filtered["Owner Name"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
            |
            filtered["Sender Device"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
            |
            filtered["Receiver Device"]
            .astype(str)
            .str.contains(
                keyword,
                case=False,
                na=False
            )
        )

        filtered = filtered[mask]

    if connection_filter:

        filtered = filtered[
            filtered["Connection Type"].isin(
                connection_filter
            )
        ]

    if status_filter:

        filtered = filtered[
            filtered["Transfer Status"].isin(
                status_filter
            )
        ]

    st.subheader(
        f"📌 Results: {len(filtered)}"
    )

    if not filtered.empty:

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No matching records."
        )

    with st.expander(
        "🔎 Record Inspector"
    ):

        if not filtered.empty:

            pick_id = st.selectbox(
                "Select Record",
                filtered["Transfer ID"].tolist()
            )

            pick = filtered[
                filtered["Transfer ID"] == pick_id
            ].iloc[0]

            st.json(
                pick.to_dict()
            )


# ============================================================
# ANALYTICS
# ============================================================

def analytics_page(df):

    st.title("📈 Analytics")

    if df.empty:

        st.warning(
            "No data available."
        )

        return

    # PIE CHART

    st.subheader(
        "🥧 Transfer Status"
    )

    status_counts = (
        df["Transfer Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig_pie = px.pie(
        status_counts,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map=STATUS_COLORS,
        hole=0.4
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

    # BAR CHART

    st.subheader(
        "📊 Connection Types"
    )

    connection_counts = (
        df["Connection Type"]
        .value_counts()
        .reset_index()
    )

    connection_counts.columns = [
        "Connection Type",
        "Count"
    ]

    fig_bar = px.bar(
        connection_counts,
        x="Connection Type",
        y="Count",
        color="Connection Type"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # HISTOGRAM

    st.subheader(
        "📶 File Size Distribution"
    )

    fig_hist = px.histogram(
        df,
        x="File Size (MB)",
        nbins=10
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

    # BOX PLOT

    st.subheader(
        "📦 File Size by Connection"
    )

    fig_box = px.box(
        df,
        x="Connection Type",
        y="File Size (MB)",
        color="Connection Type"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )


# ============================================================
# DOWNLOAD
# ============================================================

def download_page(df):

    st.title(
        "⬇️ Download Dataset"
    )

    if df.empty:

        st.warning(
            "Dataset is empty."
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            data=csv_data,
            file_name="transfers.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        json_data = json.dumps(
            df.to_dict(
                orient="records"
            ),
            indent=2
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download JSON",
            data=json_data,
            file_name="transfers.json",
            mime="application/json",
            use_container_width=True
        )


# ============================================================
# ABOUT
# ============================================================

def about_page():

    st.title("ℹ️ About")

    st.write(
        "The Ad Hoc File Transfer Tracker is a Streamlit "
        "application used to manage and analyze file transfers "
        "between devices."
    )

    st.subheader(
        "🛠 Technologies"
    )

    st.markdown(
        """
        - Python
        - Streamlit
        - Pandas
        - Plotly
        - JSON
        - CSV
        """
    )

    st.subheader(
        "👨‍💻 Developer"
    )

    st.write(
        DEVELOPER_NAME
    )


# ============================================================
# MAIN
# ============================================================

def main():

    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide"
    )

    # Load dataset

    if "data" not in st.session_state:

        st.session_state["data"] = load_data()

    df = st.session_state["data"]

    # SIDEBAR

    with st.sidebar:

        st.title(
            f"{APP_ICON} File Tracker"
        )

        page = st.radio(
            "Navigation",
            [
                "Home",
                "Dashboard",
                "Add Transfer",
                "View Transfers",
                "Search & Filter",
                "Analytics",
                "Download Dataset",
                "About"
            ]
        )

        st.divider()

        st.write(
            f"📦 Total Records: **{len(df)}**"
        )

        if st.button(
            "🔄 Refresh Data",
            use_container_width=True
        ):

            st.session_state["data"] = load_data()

            st.rerun()

    # PAGE ROUTING

    if page == "Home":
        home_page()

    elif page == "Dashboard":
        dashboard_page(df)

    elif page == "Add Transfer":
        add_transfer_page(df)

    elif page == "View Transfers":
        view_transfers_page(df)

    elif page == "Search & Filter":
        search_filter_page(df)

    elif page == "Analytics":
        analytics_page(df)

    elif page == "Download Dataset":
        download_page(df)

    elif page == "About":
        about_page()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
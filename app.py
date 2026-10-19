
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Craigmyle Parts Price Hunter",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Craigmyle Parts Price Hunter")
st.caption("Automotive • Diesel Trucks • Trailers")

st.subheader("Search Automotive Parts")

part = st.text_input(
    "Enter part number or description",
    placeholder="Example: DD15 fuel filter"
)

category = st.selectbox(
    "Vehicle category",
    [
        "All Vehicles",
        "Passenger Cars",
        "Light Trucks",
        "Heavy Duty Trucks",
        "Trailers"
    ]
)

if st.button("Find Best Prices"):
    if part.strip():
        st.info(
            f"Search requested: {part} | {category}"
        )
        st.warning(
            "Live supplier connections are not "
            "configured yet. No prices retrieved."
        )
    else:
        st.warning("Enter a part number first.")

st.divider()

st.subheader("Compare Supplier Prices")

uploaded = st.file_uploader(
    "Upload supplier price CSV",
    type=["csv"]
)

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)

        required = {
            "supplier",
            "part_number",
            "price",
            "shipping"
        }

        if not required.issubset(df.columns):
            st.error(
                "CSV needs supplier, part_number, "
                "price, and shipping columns."
            )
        else:
            df["price"] = pd.to_numeric(
                df["price"], errors="coerce"
            )
            df["shipping"] = pd.to_numeric(
                df["shipping"], errors="coerce"
            )

            df["total"] = (
                df["price"] + df["shipping"]
            )

            df = df.dropna(subset=["total"])
            df = df.sort_values("total")

            st.dataframe(
                df,
                use_container_width=True
            )

            if not df.empty:
                st.success(
                    "Lowest listed total: "
                    f"${df.iloc[0]['total']:.2f} "
                    f"from {df.iloc[0]['supplier']}"
                )
    except Exception as error:
        st.error(f"Unable to read CSV: {error}")

st.divider()
st.caption(
    "Prices must be verified for fitment, "
    "taxes, core charges, and availability."
)

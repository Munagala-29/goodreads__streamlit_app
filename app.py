import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📘 Book-Based Dashboard", layout="wide")
st.title("📘 Goodreads Book-Based Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("goodreads_library_export.csv", on_bad_lines='skip')

df = load_data()

# Preprocessing
df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
df['Date Added'] = pd.to_datetime(df['Date Added'], errors='coerce')
df['Read Year'] = df['Date Read'].dt.year
df['Days to Finish'] = (df['Date Read'] - df['Date Added']).dt.days

# Sidebar: Book selector
st.sidebar.header("Select a Book")
book_titles = sorted(df['Title'].dropna().unique())
selected_book = st.sidebar.selectbox("Choose a book title", book_titles)

# Filter only that book
book_df = df[df['Title'] == selected_book]

if book_df.empty:
    st.warning("No data available for the selected book.")
else:
    st.subheader(f"📊 Analytics for: {selected_book}")

    # Rating
    st.markdown("### ⭐ Your Rating vs Goodreads Rating")
    fig1 = px.bar(
        x=["Your Rating", "Goodreads Avg"],
        y=[book_df['My Rating'].values[0], book_df['Average Rating'].values[0]],
        labels={'x': 'Rating Source', 'y': 'Rating'},
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Pages
    st.markdown("### 📄 Number of Pages")
    st.metric("Page Count", int(book_df['Number of Pages'].values[0]))

    # Publication Year
    st.markdown("### 🗓️ Publication Year")
    st.metric("Year Published", int(book_df['Year Published'].values[0]))

    # Days to Finish
    if pd.notna(book_df['Days to Finish'].values[0]):
        st.markdown("### ⏱️ Time Taken to Read")
        st.metric("Days to Finish", int(book_df['Days to Finish'].values[0]))
    else:
        st.info("No valid Date Added or Date Read to calculate Days to Finish.")

    # 📅 Reading Timeline (Improved for Single Book)
if pd.notna(book_df['Date Added'].values[0]) and pd.notna(book_df['Date Read'].values[0]):
    st.markdown("### 📅 Reading Timeline")

    timeline_data = pd.DataFrame({
        'Task': [selected_book],
        'Start': [book_df['Date Added'].values[0]],
        'Finish': [book_df['Date Read'].values[0]]
    })

    fig2 = px.timeline(timeline_data, x_start='Start', x_end='Finish', y='Task')
    fig2.update_yaxes(autorange="reversed")  # Better display
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Missing reading dates — timeline not available.")

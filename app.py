import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📚 Goodreads Dashboard", layout="wide")
st.title("📚 Goodreads Reading Dashboard")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("goodreads_library_export.csv", on_bad_lines='skip')

df = load_data()

# Convert date columns
df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
df['Date Added'] = pd.to_datetime(df['Date Added'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filters")
min_year = st.sidebar.slider("Filter by Year", 1900, 2025, (2000, 2025))

# Book Read by Year
st.subheader("📖 Books Read by Year")
df['Read Year'] = df['Date Read'].dt.year
books_per_year = df[df['Read Year'].between(*min_year)]['Read Year'].value_counts().sort_index()
fig1 = px.bar(x=books_per_year.index, y=books_per_year.values, labels={'x': 'Year', 'y': 'Books Read'})
st.plotly_chart(fig1, use_container_width=True)

# Book Age by Publication Year
st.subheader("📚 Book Age by Publication Year")
fig2 = px.histogram(df, x='Year Published', nbins=50, title="Publication Year Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Rating Distribution
st.subheader("⭐ How You Rated Your Reads")
fig3 = px.histogram(df, x='My Rating', nbins=10)
st.plotly_chart(fig3, use_container_width=True)

# Goodreads Ratings
st.subheader("🌟 Goodreads User Ratings")
fig4 = px.histogram(df, x='Average Rating', nbins=20)
st.plotly_chart(fig4, use_container_width=True)

# Book Length Distribution
st.subheader("📏 Book Length (Pages)")
fig5 = px.histogram(df, x='Number of Pages', nbins=50)
st.plotly_chart(fig5, use_container_width=True)

# Days to Finish Reading
st.subheader("⏱️ How Quickly You Read")
df['Days to Finish'] = (df['Date Read'] - df['Date Added']).dt.days
fig6 = px.histogram(df, x='Days to Finish', nbins=40)
st.plotly_chart(fig6, use_container_width=True)

# Gender Breakdown (if gender column exists)
if 'Author Gender' in df.columns:
    st.subheader("⚧️ General Breakdown by Author Gender")
    gender_counts = df['Author Gender'].value_counts()
    fig7 = px.pie(values=gender_counts.values, names=gender_counts.index, title="Books by Gender")
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("📈 Gender Distribution Over Time")
    gender_time = df.groupby(['Read Year', 'Author Gender']).size().reset_index(name='Count')
    fig8 = px.line(gender_time, x='Read Year', y='Count', color='Author Gender')
    st.plotly_chart(fig8, use_container_width=True)

# 🔍 Search for a Specific Book by Title
st.subheader("🔍 Search for a Book by Title")

search_title = st.text_input("Enter book title to search:")

if search_title:
    result = df[df['Title'].str.contains(search_title, case=False, na=False)]

    if not result.empty:
        st.success(f"Found {len(result)} result(s):")
        st.dataframe(result[['Title', 'Author', 'My Rating', 'Average Rating', 'Number of Pages', 'Date Read', 'Date Added', 'Exclusive Shelf']])
    else:
        st.warning("No matching books found.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page title & layout
st.set_page_config(page_title="Netflix Analysis", layout="wide")

# Load dataset
@st.cache_data  # Cache for faster loading
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_type = st.sidebar.selectbox("Type", ["All"] + list(df["type"].unique()))
selected_country = st.sidebar.selectbox("Country", ["All"] + list(df["country"].dropna().unique()))

# Apply filters
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

# Main dashboard
st.title("📊 Netflix Movies & TV Shows Analysis")
st.write(f"**Total Titles:** {len(filtered_df)}")

# 1. Show top 10 movies/shows
st.subheader("Top 10 Titles by Release Year")
top_10 = filtered_df.sort_values("release_year", ascending=False).head(10)
st.dataframe(top_10[["title", "type", "release_year", "rating"]])

# 2. Distribution by Type (Pie Chart)
st.subheader("Distribution by Type")
type_counts = filtered_df["type"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%")
st.pyplot(fig1)

# 3. Trend of Releases Over Years (Line Chart)
st.subheader("Releases Over Time")
yearly_counts = filtered_df["release_year"].value_counts().sort_index()
fig2 = px.line(yearly_counts, x=yearly_counts.index, y=yearly_counts.values)
st.plotly_chart(fig2)

# 4. Ratings Distribution (Bar Chart)
st.subheader("Ratings Distribution")
fig3 = px.histogram(filtered_df, x="rating", color="type")
st.plotly_chart(fig3)

# 5. Show raw data (optional)
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(filtered_df)
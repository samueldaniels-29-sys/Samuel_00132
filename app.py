import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

st.set_page_config(
    page_title="IMDb Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202B40);
    color: white;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #202B40);
    border-right: 2px solid #34445E;
}
h1, h2, h3, h4, p, label {
    color: white !important;
}
[data-testid="stMetric"] {
    padding: 15px;
    border-radius: 12px;
    background: #1976D2;
    border: none;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: white !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #182235;
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    color: white;
    background: #202B40;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: #1685EF !important;
}
.stButton > button {
    background: linear-gradient(90deg, #1685EF, #2868C7);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background: #20A568;
    color: white;
}
[data-testid="stDataFrame"] {
    border: 1px solid #405675;
    border-radius: 8px;
}
[data-testid="stExpander"] {
    background: #202B40;
    border: 1px solid #405675;
    border-radius: 10px;
}
.stSuccess {
    background-color: #145B42;
}
.stInfo {
    background-color: #183B63;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("ToP 250 movies on imdb in 2026.csv")

def find_column(names):
    for name in names:
        for col in df.columns:
            if col.lower().strip() == name.lower().strip():
                return col
    return None

title_col = find_column(["primaryTitle", "originalTitle", "title"])
rating_col = find_column(["averageRating"])
votes_col = find_column(["numVotes"])
genre_col = find_column(["genres", "genre"])
country_col = find_column([
    "countriesOfOrigin",
    "countryOfOrigin",
    "country",
    "countries"
])
gross_col = find_column(["grossWorldwide"])

if any(x is None for x in [title_col, rating_col, votes_col, genre_col]):
    st.error("Required columns are missing in the CSV file.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
df[votes_col] = pd.to_numeric(df[votes_col], errors="coerce").fillna(0)

def convert_gross(value):
    if pd.isna(value):
        return None

    value = str(value).strip().replace("$", "").replace(",", "")

    multiplier = 1

    if value.upper().endswith("B"):
        multiplier = 1000000000
        value = value[:-1]
    elif value.upper().endswith("M"):
        multiplier = 1000000
        value = value[:-1]
    elif value.upper().endswith("K"):
        multiplier = 1000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except ValueError:
        return None

if gross_col:
    df[gross_col] = df[gross_col].apply(convert_gross)

def split_values(value):
    if pd.isna(value):
        return []

    values = re.split(r"[,;|]", str(value))

    return [
        x.strip().strip("[]").strip("'").strip('"')
        for x in values
        if x.strip().strip("[]").strip("'").strip('"')
    ]

genres = sorted(set(
    df[genre_col].dropna().apply(split_values).explode().dropna()
))

countries = []

if country_col:
    countries = sorted(set(
        df[country_col].dropna().apply(split_values).explode().dropna()
    ))

min_rating = float(df[rating_col].min())
max_rating = float(df[rating_col].max())

if min_rating == max_rating:
    max_rating = min_rating + 0.1

st.sidebar.markdown("""
<div style="background:#F5C518;color:black;padding:10px;
border-radius:10px;width:100px;text-align:center;
font-size:25px;font-weight:bold;">
IMDb
</div>
""", unsafe_allow_html=True)

st.sidebar.title("Movie Analytics Dashboard")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Movie Explorer", "Movie Search"]
)

with st.sidebar.expander("ℹ️ Dataset Information", expanded=True):
    st.write("Top 250 Movies on IMDb (2026)")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
    st.write("This dataset contains movie titles, ratings, votes and genres.")

st.sidebar.success("Dataset Loaded Successfully!")

st.markdown("""
<div style="
background:linear-gradient(90deg,#111827,#283B56,#111827);
padding:25px;
border-radius:12px;
text-align:center;
border:1px solid #405675;">
<h1 style="color:white;">🎬 IMDb Movie Analytics Dashboard</h1>
<h3 style="color:#F5C518;">Explore. Analyze. Discover.</h3>
</div>
""", unsafe_allow_html=True)

st.success("Dashboard loaded successfully! Enjoy exploring the top 250 movies on IMDb.")

with st.expander("Q1 - Dataset Loading and Initial Exploration"):

    st.subheader("First 10 Records")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Dataset Information")

    c1, c2 = st.columns(2)

    c1.metric("Total Rows", df.shape[0])
    c2.metric("Total Columns", df.shape[1])

    st.write("Column Names:")
    st.write(df.columns.tolist())

    st.write("Data Types:")
    st.write(df.dtypes.astype(str))

    st.write("Missing Values:")
    st.dataframe(df.isnull().sum().rename("Missing Values"))

    st.success("Dataset exploration completed successfully!")

st.divider()

if page == "Dashboard":

    st.header("📊 Movie Analytics Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div style="background:#1976D2;padding:15px;border-radius:12px;">', unsafe_allow_html=True)
        st.metric("🎬 Total Movies", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div style="background:#20A568;padding:15px;border-radius:12px;">', unsafe_allow_html=True)
        st.metric("⭐ Average IMDb Rating", f"{df[rating_col].mean():.1f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div style="background:#783CC1;padding:15px;border-radius:12px;">', unsafe_allow_html=True)
        st.metric("🏆 Highest Rating", f"{df[rating_col].max():.1f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div style="background:#FF8800;padding:15px;border-radius:12px;">', unsafe_allow_html=True)
        st.metric("👥 Total Votes", f"{int(df[votes_col].sum()):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.header("Movie Data Visualizations")

    tab1, tab2, tab3 = st.tabs([
        "📊 Genre Analysis",
        "🥧 Rating Analysis",
        "💰 Gross Collection"
    ])

    with tab1:

        st.subheader("Movies by Genre")

        genre_data = (
            df[genre_col].dropna().apply(split_values).explode().dropna()
        )

        genre_count = genre_data.value_counts()

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        genre_count.plot(
            kind="bar",
            ax=ax,
            color=["#1976D2", "#20A568", "#FFB52E",
                   "#8945C9", "#35B5E5", "#E99A19"]
        )

        ax.set_title("Movies by Genre", color="#101827")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=0)
        ax.grid(axis="y", alpha=0.2)

        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(genre_count.rename("Number of Movies"))

    with tab2:

        st.subheader("IMDb Rating Distribution")

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.hist(
            df[rating_col].dropna(),
            bins=12,
            color="#2585EF",
            edgecolor="white"
        )

        ax.set_title("IMDb Rating Distribution")
        ax.set_xlabel("IMDb Rating")
        ax.set_ylabel("Number of Movies")
        ax.grid(alpha=0.2)

        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Rating vs Number of Votes")

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        sns.scatterplot(
            data=df,
            x=rating_col,
            y=votes_col,
            color="#1685EF",
            ax=ax
        )

        ax.set_title("Rating vs Number of Votes")
        ax.set_xlabel("IMDb Rating")
        ax.set_ylabel("Number of Votes")
        ax.grid(alpha=0.2)

        st.pyplot(fig)
        plt.close(fig)

    with tab3:

        st.subheader("Top 10 Movies by Worldwide Gross")

        if gross_col and df[gross_col].notna().any():

            top_gross = (
                df.dropna(subset=[gross_col])
                .sort_values(by=gross_col, ascending=False)
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor("white")
            ax.set_facecolor("white")

            ax.barh(
                top_gross[title_col],
                top_gross[gross_col],
                color="#FF9418"
            )

            ax.set_title("Top 10 Movies by Worldwide Gross")
            ax.set_xlabel("Worldwide Gross Collection")
            ax.set_ylabel("Movie Title")
            ax.invert_yaxis()

            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            st.dataframe(
                top_gross[[title_col, gross_col]],
                use_container_width=True
            )

        else:
            st.info("Worldwide gross collection data is not available in this dataset.")

    st.divider()

if page in ["Dashboard", "Movie Explorer"]:

    st.header("🔎 Interactive Movie Explorer")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        selected_genre = st.selectbox(
            "Genre",
            ["All"] + genres,
            key="genre_filter"
        )

    with col2:
        if country_col and countries:
            selected_countries = st.multiselect(
                "Countries",
                countries,
                key="country_filter"
            )
        else:
            selected_countries = []
            st.info("Country information is unavailable.")

    with col3:
        min_votes = st.number_input(
            "Minimum Votes",
            min_value=0,
            value=0,
            step=1000,
            key="votes_filter"
        )

    rating_range = st.slider(
        "IMDb Rating",
        min_value=min_rating,
        max_value=max_rating,
        value=(min_rating, max_rating),
        step=0.1,
        key="rating_filter"
    )

    col4, col5 = st.columns([2, 1])

    with col4:
        search_title = st.text_input(
            "Search Movie Title",
            placeholder="Enter movie title...",
            key="title_filter"
        )

    with col5:
        sort_order = st.radio(
            "Sort Order",
            ["Ascending", "Descending"],
            key="sort_filter"
        )

    filtered_df = df.copy()

    if selected_genre != "All":
        filtered_df = filtered_df[
            filtered_df[genre_col].apply(
                lambda x: selected_genre in split_values(x)
            )
        ]

    if selected_countries and country_col:
        filtered_df = filtered_df[
            filtered_df[country_col].apply(
                lambda x: any(
                    country in split_values(x)
                    for country in selected_countries
                )
            )
        ]

    filtered_df = filtered_df[
        (filtered_df[rating_col] >= rating_range[0]) &
        (filtered_df[rating_col] <= rating_range[1])
    ]

    filtered_df = filtered_df[
        filtered_df[votes_col] >= min_votes
    ]

    if search_title:
        filtered_df = filtered_df[
            filtered_df[title_col].astype(str).str.contains(
                search_title,
                case=False,
                na=False
            )
        ]

    filtered_df = filtered_df.sort_values(
        by=rating_col,
        ascending=(sort_order == "Ascending")
    )

    st.metric("Filtered Movies", len(filtered_df))

    display_columns = [
        title_col,
        genre_col,
        rating_col,
        votes_col
    ]

    if country_col:
        display_columns.append(country_col)

    if gross_col:
        display_columns.append(gross_col)

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True
    )

    def reset_filters():
        keys = [
            "genre_filter",
            "country_filter",
            "rating_filter",
            "votes_filter",
            "title_filter",
            "sort_filter"
        ]

        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

    st.button(
        "🔄 Reset Filters",
        on_click=reset_filters
    )

    st.success("Movie Explorer is ready!")

    st.divider()

if page in ["Dashboard", "Movie Search"]:

    st.header("🎥 Movie Search (Form + Session State)")

    if "selected_movie" not in st.session_state:
        st.session_state.selected_movie = None

    with st.form("movie_search_form"):

        movie_name = st.text_input(
            "Movie Title",
            placeholder="Enter movie title..."
        )

        preferred_genre = st.selectbox(
            "Preferred Genre",
            genres,
            key="form_genre"
        )

        preferred_rating = st.slider(
            "Minimum IMDb Rating",
            min_value=min_rating,
            max_value=max_rating,
            value=min_rating,
            step=0.1,
            key="form_rating"
        )

        submitted = st.form_submit_button("🔍 Search Movie")

    if submitted:

        search_df = df[
            df[rating_col] >= preferred_rating
        ]

        if preferred_genre != "All":
            search_df = search_df[
                search_df[genre_col].apply(
                    lambda x: preferred_genre in split_values(x)
                )
            ]

        if movie_name:
            search_df = search_df[
                search_df[title_col].astype(str).str.contains(
                    movie_name,
                    case=False,
                    na=False
                )
            ]

        if not search_df.empty:
            st.session_state.selected_movie = search_df.iloc[0].to_dict()
            st.success("Matching movie found successfully!")
        else:
            st.session_state.selected_movie = None
            st.info("No matching movie found. Try different preferences.")

    if st.session_state.selected_movie is not None:

        movie = st.session_state.selected_movie

        st.subheader("Selected Movie Information")

        st.write("Movie Title:", movie[title_col])
        st.write("Genre:", movie[genre_col])

        c1, c2 = st.columns(2)

        c1.metric("IMDb Rating", movie[rating_col])
        c2.metric("Number of Votes", f"{int(movie[votes_col]):,}")

st.divider()

st.success("IMDb Movie Analytics Dashboard Completed Successfully!")
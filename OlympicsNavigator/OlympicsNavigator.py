# Import the Streamlit library
import streamlit as st
import pandas as pd

selected_tab = st.sidebar.radio("Contents", options=["Overview", "Medalists Data", "Notable Olympic Games"])

if selected_tab == "Overview":
    st.title("Welcome to the Olympics Navigation Tool!")
    st.image("OlympicsNavigator/images/olympicrings.jpeg")
    st.markdown("""
    ## About

    This is a tool that allows users to both filter through Olympic medalist data and read about notable Olympic games.

    ## Table of Contents

    - **Overview**
    - **Medalists Data**
    - **Notable Olympic Games**
    """)

elif selected_tab == "Medalists Data":

        # Load Medalist Data
        df = pd.read_csv("OlympicsNavigator/data/olympicmedalists.csv")
        df["Year"] = df["Year"].astype(str)
        # Dashboard title
        st.title("Olympic Athletes Dashboard")
        st.image("OlympicsNavigator/images/OlympicsPodium.jpg")
        # ============================================================================
        # Cascading Filters: Season -> Sport -> Event (with "All" as default)
        # ============================================================================
        st.header("Filters")

        # --- Season Filter ---
        seasons = sorted(df["Season"].unique())
        season_options = ["All"] + seasons
        selected_season = st.selectbox("Select Season", options=season_options, index=0)

        # Filter based on selected season if not "All"
        if selected_season == "All":
            df_season = df
        else:
            df_season = df[df["Season"] == selected_season]

        # --- Sport Filter ---
        sports = sorted(df_season["Sport"].unique())
        sport_options = ["All"] + sports
        selected_sport = st.selectbox("Select Sport", options=sport_options, index=0)

        # Filter further based on the selected sport if not "All"
        if selected_sport == "All":
            df_sport = df_season
        else:
            df_sport = df_season[df_season["Sport"] == selected_sport]

        # --- Event Filter ---
        events = sorted(df_sport["Event"].unique())
        event_options = ["All"] + events
        selected_event = st.selectbox("Select Event", options=event_options, index=0)

        # ============================================================================
        # Independent Filters: Country, Medal, and Year (default to "All")
        # ============================================================================

        # --- Country Filter ---
        countries = sorted(df["NOC"].unique())
        country_options = ["All"] + countries
        selected_countries = st.multiselect("Select Country/Countries", options=country_options, default=["All"])

        # --- Medal Filter ---
        medals = sorted(df["Medal"].unique())
        medal_options = ["All"] + medals
        selected_medals = st.multiselect("Select Medal Type(s)", options=medal_options, default=["All"])

        # --- Year Filter ---
        years = sorted(df["Year"].unique())
        year_options = ["All"] + [str(year) for year in years]
        selected_year = st.selectbox("Select Year", options=year_options, index=0)

        # ============================================================================
        # Apply All Filters to the DataFrame
        # ============================================================================
        filtered_df = df.copy()

        # Apply cascading filters (Season, Sport, Event)
        if selected_season != "All":
            filtered_df = filtered_df[filtered_df["Season"] == selected_season]
        if selected_sport != "All":
            filtered_df = filtered_df[filtered_df["Sport"] == selected_sport]
        if selected_event != "All":
            filtered_df = filtered_df[filtered_df["Event"] == selected_event]

        # Apply independent filters:
        # Country filter: if "All" is not among selected, then filter by selected country codes
        if "All" not in selected_countries:
            filtered_df = filtered_df[filtered_df["NOC"].isin(selected_countries)]
        # Medal filter: if "All" is not among selected, then filter by selected medal types
        if "All" not in selected_medals:
            filtered_df = filtered_df[filtered_df["Medal"].isin(selected_medals)]
        # Year filter: if a specific year is selected (not "All")
        if selected_year != "All":
            filtered_df = filtered_df[filtered_df["Year"] == selected_year]

        # ============================================================================
        # Display the Filtered Data
        # ============================================================================
        st.subheader("Filtered Results")
        st.dataframe(filtered_df)


elif selected_tab == "Notable Olympic Games":

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summer 1896 - Athens, Greece", 
                                            "Winter 1924 - Charmonix, France", 
                                            "Summer 1936 - Berlin, Germany", 
                                            "Summer/Winter 1980", 
                                            "Summer 2021 - Tokyo, Japan"])

    with tab1:
        st.title("Summer 1896 - Athens, Greece : The First Modern Olympic Games")
        st.image("OlympicsNavigator/images/1896Athens.jpg")
    
    with tab2:
        st.title("Winter 1924 - Charmonix France : The Inaugural Winter Olympic Games")
        st.image("OlympicsNavigator/images/Charmonix1924.jpg")
    with tab3:
        st.title("Summer 1936 - Berlin, Germany : Olympics and World War II")
        st.image("OlympicsNavigator/images/Berlin1936.jpg")
    
    with tab4:
        st.title("Winter 1980 - Lake Placid, USA : 'Miracle on Ice'")
        st.image("OlympicsNavigator/images/LakePlacid1980.jpeg")

        st.title("Summer 1980 - Moscow, Soviet Union : Boycott")
        st.image("OlympicsNavigator/images/Summer1980.jpg")

    with tab5:
        st.title("Summer 2021 - Tokyo, Japan : The COVID Olympics")
        st.image("OlympicsNavigator/images/2021Summer.jpg")
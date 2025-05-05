# Import the Streamlit library
import streamlit as st
import pandas as pd
import plotly.express as px

selected_tab = st.sidebar.radio("Contents", options=["Overview", "Medalists Data", "Olympics Around the World", "Notable Olympic Games", "Works Cited"])

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

elif selected_tab == "Olympics Around the World":
    # Set page title
    st.title("Olympics Around the World: Host Cities Map")

    # Load dataset
    hosts = pd.read_csv("OlympicsNavigator/data/hosts.csv")

    # Create a 'Season' column based on which column is not null
    hosts['Season'] = hosts.apply(lambda row: 'Summer' if pd.notna(row['Summer']) else 'Winter', axis=1)

    # Create the interactive map
    fig = px.scatter_geo(
        hosts,
        lat='Latitude',
        lon='Longitude',
        color='Season',
        color_discrete_map={'Summer': 'red', 'Winter': 'blue'},
        text=["City", "Country"],
        title="Olympic Host Cities"
    )

    # Adjust map and hover appearance
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    fig.update_layout(legend_title_text='Olympic Season')

    # Display map in Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Notable Olympic Games":

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summer 1896 - Athens, Greece", 
                                            "Winter 1924 - Charmonix, France", 
                                            "Summer 1936 - Berlin, Germany", 
                                            "Summer/Winter 1980", 
                                            "Summer 2021 - Tokyo, Japan"])

    with tab1:
        st.title("Summer 1896 - Athens, Greece : The First Modern Olympic Games")

        st.image("OlympicsNavigator/images/1896Athens.jpg")
        st.caption("Panathaneic Stadium - Athens, Greece. 1896")
        
        st.markdown("""## Summary

The Olympics are here! It is fitting that the first ever modern Olympic games were hosted in Athens, Greece, the birthplace of the ancient Olympic Games. These games took place from April 6 – April 15 and included 43 events with about 280 athletes from 14 nations. The Opening Ceremony was held in the Panathenaic Stadium (shown above). This was the original stadium built for the ancient Olympics that was later excavated and rebuilt for these Olympic games.

A French aristocrat by the name of Pierre, baron de Coubertin pioneered the movement for an international Olympic Games and was a founding member of the [International Olympic Committee (IOC)](https://olympics.com/ioc). As a result, Coubertin also served as the president of the 1896 games.

Though the Olympics of today still bare the same name, the events of 1896 looked much different. For example, rather than the modern Olympic pools that exist today for the swimming events, swimmers in the 1896 games were transported by boat out to sea and left to swim the required distance back to shore.
                    """)

    with tab2:
        st.title("Winter 1924 - Chamonix France : The Inaugural Winter Olympic Games")

        st.image("OlympicsNavigator/images/Charmonix1924.jpg")
        st.caption("Olympic Stand - Chamonix France. 1924")

        st.markdown("""## Summary
                    
The games held in Chamonix, France in 1924 were first known as "Winter Sports Week" at the time of their occurrence and then retroactively deemed the First Olympic Wnter Games by the IOC in 1926. Chamonix was a perfect location as it sits at the base of Europe's tallest mountain, Mont Blanc. The Games consisted of over 10,000 spectators watching 258 athletes from 16 nations (estimated numbers) competing in 16 events across five sports (Bobsleigh, Curling, Ice Hockey, Skating, and Nordic Skiing) over the course of 11 days.
                    
Some notable performances from these games were Charles Jewtraw (USA) taking home the first Olympic gold medal in the 500m speed skating and the Canadian Hockey Team winning their gold medal with a point differential of +119!

The Winter Olympic Games we know today look drastically different than the Chamonix Games. For example, athletes used to have to carry their gear and equipment with them during the Opening Ceremony, bobsleigh teams did not wear helmets, and hockey players did not wear helmets or gloves! 
                    """)

    with tab3:
        st.title("Summer 1936 - Berlin, Germany : Olympics and World War II")

        st.image("OlympicsNavigator/images/Berlin1936.jpg")
        st.caption("Jesse Owens winning 1 of his 4 gold medals. 1936")

        st.markdown("""## Summary

In 1931, the IOC awarded the 1936 Summer Olympic bid to Berlin, Germany to signify their return to the global community following World War I. However, the following years were characterized by the rise of the Nazi regime in Germany sparking controversy as the host of the Olympic games. German abolition of Jewish athletes from their national delegation sparked discussions of boycott that yielded no action; only the Soviet Union chose not to participate.
                    
Ultimately, the 1936 Summer Olympic Games hosted 49 delegations, 3,963 athletes, and 129 events. The games are best remembered for Jesse Owens' spectacular performance as a dagger to the Nazi regime's attempt to promote Aryan racial superiority. Jesse Owens, a black American track star won 4 gold medals in the 100m, 200m, 4x100m relay, and the long jump. Another inspiring story arose out of the friendship of 2 Japanese pole vaulters, Sueo Oe and Shuhei Nishida who both tied for second place. Out of mutual respect for one another, the two pole vaulters declined a jump-off tiebreaker. After returning to Japan, the two exchanged halves of medals so they each possess a half silver medal and a half bronze medal. These medals have been termed "The Friendship Medals."

Finally, the Berlin Olympic Games saw a lot of firsts. Sports like basketball, canoeing, and handball made their Olympic debuts. Additionally, American Marjorie Gestring became the youngest gold medalist, taking home the gold in springboard diving at just 13-years-old. However, it was 12-year-old Inge Sorensen from Denmark who became the youngest medalist of all time taking home the bronze in breastroke.

                    """)

    with tab4:
        st.title("Winter 1980 - Lake Placid, USA : 'Miracle on Ice'")
        st.image("OlympicsNavigator/images/LakePlacid1980.jpeg")
        st.caption("Winter Olympics Opening Ceremony - Lake Placid, USA. 1980")
        st.markdown("""

Hosting the games for the second time (first in 1932), Lake Placid hosted 37 countries with 1,072 athletes competing in 38 events. These Olympics were marked by innovation as this was the first Olympics to use artificial snow.    

These Olympics also consisted of numerous memorable champions. Hanni Wenzel from Liechtenstein won gold in both giant and regular slalom events making Liechtenstein the smallest country to ever produce an Olympic champion. In the biathlon, Aleksander Tikhonov won his fourth straight gold medal in the event. In speed skating, American Eric Heiden won gold in all five olympic speed skating events while also setting an Olympic record in every one. Finally, the U.S.A hockey team upset the U.S.S.R hockey team in the gold medal game which later yielded a Disney movie titled "Miracle on Ice."
             
                    """)

        st.title("Summer 1980 - Moscow, Soviet Union : Boycott")
        st.image("OlympicsNavigator/images/Summer1980.jpg")
        st.caption("Summer Olympics Opening Ceremony - Moscow, Soviet Union. 1980")
        st.markdown("""

The year 1980 marked an escalation in the rivalry between the U.S. and U.S.S.R. Tensions in the Cold War rose as the two countries spearheaded the ideological conflict of Democracy vs. Communism. In 1979, the Soviet Union invaded Afghanistan. In response, U.S. President Jimmy Carter withdrew the U.S. and all American athletes from the Olympic Games in boycott. 55 other countries followed, however some nations such as Great Brtiain and Australia allowed their athletes to compete independently if they would like (because of the varying reasons for not participating and varied participation agreements, this number fluctuates depending on the source). As a result, only 80 nations participated in the 1980 Moscow Olympics, the lowest number since 1956. Additionally, National Broadcasting Company (NBC) also boycotted these games so little is known about these games in the U.S. .There were a total of 5,179 athletes competing in 203 events. This was the first time the Olympic Games were held in a socialist country. Four years later, the Summer Olympics were held in Los Angeles, U.S.A and the Soviet Union along with many Eastern European countries boycotted for security reasons.
                    
Notable performances from the games included gymnast Aleksander Dityatin of the U.S.S.R. winning 8 individual medals and Miruts Yifter of Ethiopia winning both the 5,000 and 10,000-meter runs. Finally, this was the first Olympic Games to include women's field hockey. However, the boycott left many voids in the field. Zimbabwe, who had officially become a country just a few months before was invited to send their field hockey team to the Olympics just a week before the games started. Amazingly, the team went on to go undefeated in the round-robin tournament and bring home the gold medal!
                    
                    """)

    with tab5:
        st.title("Summer 2021 - Tokyo, Japan : The COVID Olympics")
        st.image("OlympicsNavigator/images/2021Summer.jpg")
        st.caption("2021 Summer Olympics Flyer")
        st.markdown("""

In March of 2020, the COVID-19 pandemic swept across the globe causing many events and gatherings to shut down and be cancelled. The Summer Olympic Games were no exception; in the best interest of the health of everyone involved, the games were pushed back to the following summer. The 2020 Games, held in the summer of 2021, included the most events ever (339) in 33 sports including the debut of many new events such as skateboarding, sport climbing, surfing, karate, BMX freestyle, and 3x3 basketball. The games also were the most gender-equal in history, sporting an almost 50/50 split of male/female athletes. 
                    
Though an excellent display of international unity and resilience, the decision to host the Olympics even in 2021 faced much opposition. An Ipsos Mori survery showed the 78 percent of Japanese residents did not want the games to be held at all, even with no spectators being allowed. Needless to say, the Games went on. Notable performances included swimmer Ahmed Hafnaoui from Tunisia winning the gold medal in th 400-meter freestyle, Allyson Felix became the most decorated U.S. athlete in track and field victory, and Qatar's Mutaz Essah Barshim and Italy's Gianmarco Tamberi sharing the gold medal in the men's high jump.

                    """)
        



        
elif selected_tab == "Works Cited":
    st.title("Works Cited")
    st.markdown("""

“The 1936 Olympics.” American Experience, Public Broadcasting Service, www.pbs.org/wgbh/americanexperience/features/goebbels-olympics/. Accessed 5 May 2025. 

“1980 Summer Olympics.” Olympedia, www.olympedia.org/editions/20. Accessed 5 May 2025. 

Gold, John R., and Margaret M. Gould. “Revival and Reinvention: The Olympic Games, Athens 1896.” Origins, The Ohio State University, origins.osu.edu/milestones/revival-and-reinvention-olympic-games-athens-1896. Accessed 5 May 2025. 

“How We Got to the Tokyo Olympics despite a Global Pandemic.” CNN, Cable News Network, edition.cnn.com/interactive/2021/07/sport/tokyo-olympics-arduous-journey-timeline-spt-intl-cmd/. Accessed 5 May 2025. 

Kennedy, Merrit, et al. “The 14 Moments That Swept Us Away at the Tokyo Olympics.” NPR, NPR, 8 Aug. 2021, www.npr.org/sections/tokyo-olympics-live-updates/2021/08/08/1025527026/tokyo-summer-olympics-best-moments-simone-biles-caeleb-dressel-allyson-felix#jumpers. 

“Moscow 1980 Olympic Games.” Encyclopædia Britannica, Encyclopædia Britannica, inc., www.britannica.com/event/Moscow-1980-Olympic-Games. Accessed 5 May 2025. 

Olympics.Com | Olympic Games, Medals, Results & Latest News, www.olympics.com/en/. Accessed 5 May 2025. 

Senesac, Emily. “No Snow in Sight: The NWS and the 1980 Olympic Winter Games.” National Weather Service Heritage, vlab.noaa.gov/web/nws-heritage/-/no-snow-in-sight-the-nws-and-the-1980-olympic-winter-games. Accessed 5 May 2025. 

Vignemont, Diane. Chamonix 1924: Inventing the Winter Olympics, France-Amerique, 23 Jan. 2024, france-amerique.com/chamonix-1924-inventing-the-winter-olympics/. 
                """)
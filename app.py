import streamlit as st
import pandas as pd
import pymysql
from streamlit_option_menu import option_menu

connection = pymysql.connect(

                            host = "localhost", # IP address of your server
                            user = "rahila",
                            password = "12345",
                            database = "asteriod"
                           
                    )
cursor = connection.cursor()

st.set_page_config(layout="wide")
st.markdown("<h1 style ='text-align: centre; color: #8888BE;'>🚀💥 NASA Asteriod Data 💫🧑🏻‍🚀</h1>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    selected = option_menu(
        menu_title="Asteriod Approaches",
        options=["Filter Criteria", "Queries"],
        icons = ["moon", "star"],
        menu_icon= "sun",
        default_index=1              
)

option=[]
q1 = []

if selected == "Queries":
    st.subheader("🖍️❓ Queries")
    option = st.selectbox(
        "Select your query", [
            '1.Count how many times each asteroid has approached Earth',
            '2.Average velocity of each asteroid over multiple approaches',
            '3.List top 10 fastest asteroids',
            '4.Find potentially hazardous asteroids that have approached Earth more than 3 times',
            '5.Find the month with the most asteroid approaches',
            '6.Get the asteroid with the fastest ever approach speed',
            '7.Sort asteroids by maximum estimated diameter (descending)',
            '8.Asteroids whose closest approach is getting nearer over time',
            '9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth',
            '10.List names of asteroids that approached Earth with velocity > 50,000 km/h',
            '11.Count how many approaches happened per month',
            '12.Find asteroid with the highest brightness (lowest magnitude value)',
            '13.Get number of hazardous vs non-hazardous asteroids',
            '14.Find asteroids that passed closer than the Moon (less than 1 LD), along with their close approach date and distance',
            '15.Find asteroids that came within 0.05 AU(astronomical distance)',
            '16.Find distinct asteriods',
            '17.Average estimated diameter (min and max) of all asteroids',
            '18.Generate all possible asteroid-approach combinations',
            '19.Find asteroids that have never approached Earth',
            '20.Yearly count of unique asteroid approaches to Earth'
        ])

    if option == '1.Count how many times each asteroid has approached Earth':
        q1 = """
        SELECT a.id, a.name, COUNT(c.id) AS approach_count
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.orbiting_body = 'Earth'
        GROUP BY a.id, a.name
        ORDER BY approach_count DESC 
        LIMIT 100;
        """

    elif option == '2.Average velocity of each asteroid over multiple approaches':
        q1 = """
        SELECT a.id, a.name, AVG(c.relative_velocity_kmph) AS avg_velocity
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        GROUP BY a.id, a.name
        ORDER BY avg_velocity DESC;
        """

    elif option == '3.List top 10 fastest asteroids':
        q1 = """
        SELECT a.id, a.name, c.relative_velocity_kmph
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        ORDER BY c.relative_velocity_kmph DESC
        LIMIT 10;
        """

    elif option == '4.Find potentially hazardous asteroids that have approached Earth more than 3 times':
        q1 = """
        SELECT a.id, a.name, COUNT(c.id) as approaches
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE a.is_potentially_hazardous_asteroid = 1 AND c.orbiting_body = 'Earth'
        GROUP BY a.id, a.name
        HAVING approaches > 3
        ORDER BY approaches DESC;
        """

    elif option == '5.Find the month with the most asteroid approaches':
        q1 = """
        SELECT MONTH(c.close_approach_date) AS month, COUNT(*) AS num_approaches
        FROM close_approach c
        GROUP BY month
        ORDER BY num_approaches DESC
        LIMIT 1;
        """

    elif option == '6.Get the asteroid with the fastest ever approach speed':
        q1 = """
        SELECT a.id, a.name, MAX(c.relative_velocity_kmph) AS max_speed
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        GROUP BY a.id, a.name
        ORDER BY max_speed DESC
        LIMIT 1;
        """

    elif option == '7.Sort asteroids by maximum estimated diameter (descending)':
        q1 = """
        SELECT id, name, estimated_diameter_max_km
        FROM asteroids
        ORDER BY estimated_diameter_max_km DESC;
        """

    elif option == '8.Asteroids whose closest approach is getting nearer over time':
        q1 = """
        SELECT a.id, a.name, c.close_approach_date, c.miss_distance_km
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.orbiting_body = 'Earth'
        ORDER BY a.id, c.close_approach_date; 
        """

    elif option == '9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth':
        q1 = """
        SELECT a.name, c.close_approach_date, c.miss_distance_km
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.orbiting_body = 'Earth'
        ORDER BY c.miss_distance_km ASC;
        """

    elif option == '10.List names of asteroids that approached Earth with velocity > 50,000 km/h':
        q1 = """
        SELECT a.name, c.relative_velocity_kmph
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.orbiting_body = 'Earth' AND c.relative_velocity_kmph > 50000;
        """

    elif option == '11.Count how many approaches happened per month':
        q1 = """
        SELECT MONTH(c.close_approach_date) AS month, COUNT(*) AS approach_count
        FROM close_approach c
        GROUP BY month
        ORDER BY approach_count DESC;
        """

    elif option == '12.Find asteroid with the highest brightness (lowest magnitude value)':
        q1 = """
        SELECT id, name, absolute_magnitude_h
        FROM asteroids
        ORDER BY absolute_magnitude_h ASC
        LIMIT 1;
        """

    elif option == '13.Get number of hazardous vs non-hazardous asteroids':
        q1 = """
        SELECT is_potentially_hazardous_asteroid, COUNT(*) as count
        FROM asteroids
        GROUP BY is_potentially_hazardous_asteroid;
        """

    elif option == '14.Find asteroids that passed closer than the Moon (less than 1 LD), along with their close approach date and distance':
        q1 = """
        SELECT a.name, c.close_approach_date, c.miss_distance_lunar
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.miss_distance_lunar < 1
        ORDER BY c.miss_distance_lunar ASC;
        """

    elif option == '15.Find asteroids that came within 0.05 AU(astronomical distance)':
        q1 = """
        SELECT a.name, c.close_approach_date, c.astronomical
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.astronomical < 0.05
        ORDER BY c.astronomical ASC;
        """
    elif option == '16.Find distinct asteriods':
        q1 = """
        select distinct name from asteroids;
        """
    elif option == '17.Average estimated diameter (min and max) of all asteroids':
        q1 = """
        SELECT AVG(estimated_diameter_min_km) AS avg_diameter_min_km, 
        AVG(estimated_diameter_max_km) AS avg_diameter_max_km
        FROM asteroids;
        """
        
    elif option == '18.Generate all possible asteroid-approach combinations':
        q1 = """
        SELECT a.id, a.name, c.close_approach_date, c.orbiting_body
        FROM asteroids a CROSS JOIN close_approach c LIMIT 100;
        """
    
    elif option == '19.Find asteroids that have never approached Earth':
        q1 = """
        SELECT COUNT(*) AS asteroids_without_approaches
        FROM asteroids a
        LEFT JOIN close_approach c ON a.id = c.id AND c.orbiting_body = 'Earth'
        WHERE c.id IS NULL;
        """
        
    elif option == '20.Yearly count of unique asteroid approaches to Earth':
        q1 = """
        SELECT YEAR(c.close_approach_date) AS year, COUNT(DISTINCT a.id) AS unique_asteroids
        FROM asteroids a
        JOIN close_approach c ON a.id = c.id
        WHERE c.orbiting_body = 'Earth'
        GROUP BY year
        ORDER BY year;
        """

    if q1:
        cursor.execute(q1)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)



#filtering based on criteria
elif selected == "Filter Criteria":
    st.subheader("🔎 Filter Criteria")

    # Date range filter
    start_date = st.date_input("Start Date", pd.to_datetime("2024-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2025-04-01"))

    # Astronomical Unit filter
    au_min, au_max = st.slider("Miss Distance (AU)", 0.0, 1.0, (0.0, 0.05), step=0.001)

    # Lunar Distance filter

    ld_min, ld_max = st.slider("Miss Distance (Lunar)", 0.0, 100.0, (0.0, 10.0), step=0.5)

    # Velocity filter
    velocity_min = st.slider("Minimum Relative Velocity (km/h)", 0, 150000, 50000, step=1000)

    # Estimated diameter filter
    dia_min, dia_max = st.slider("Estimated Diameter (km)", 0.0, 10.0, (0.0, 1.0), step=0.1)

    # Hazardous filter
    hazardous_filter = st.selectbox("Potentially Hazardous?", ["All", "Yes", "No"])

    query = f"""
    SELECT 
    a.name,
    c.close_approach_date,
    c.relative_velocity_kmph,
    c.astronomical,
    c.miss_distance_lunar,
    a.estimated_diameter_min_km,
    a.estimated_diameter_max_km,
    a.is_potentially_hazardous_asteroid
    FROM asteroids a
    JOIN close_approach c ON a.id = c.id
    WHERE c.close_approach_date BETWEEN '{start_date}' AND '{end_date}'
    AND c.relative_velocity_kmph >= {velocity_min}
    AND c.astronomical BETWEEN {au_min} AND {au_max}
    AND c.miss_distance_lunar BETWEEN {ld_min} AND {ld_max}
    AND a.estimated_diameter_min_km >= {dia_min}
    AND a.estimated_diameter_max_km <= {dia_max}
    """

# Apply hazardous filter
    if hazardous_filter == "Yes":
         query += " AND a.is_potentially_hazardous_asteroid = 1"
    elif hazardous_filter == "No":
        query += " AND a.is_potentially_hazardous_asteroid = 0"

    query += " ORDER BY c.close_approach_date DESC;"

      # ✨ Show query for transparency
    with st.expander("📜 Show SQL Query"):
        st.code(query, language="sql")

    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)

    st.success(f"✅⌛Related records")
    st.dataframe(df, use_container_width=True)

    

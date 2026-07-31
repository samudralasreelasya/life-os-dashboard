import os
import pandas as pd
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Life-OS Wellbeing Dashboard", page_icon="📱", layout="wide"
)

# Initialize Gemini Client
# For Streamlit Cloud, keys are fetched from st.secrets. Locally, it looks for environment variables.
# Initialize Gemini Client (safely checks environment first, then Streamlit secrets)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
  try:
    api_key = st.secrets.get("GEMINI_API_KEY")
  except Exception:
    api_key = None
client = None
if api_key:
  try:
    client = genai.Client(api_key=api_key)
  except Exception as e:
    st.error(f"Failed to initialize Gemini client: {e}")


# Load Data Pipeline
@st.cache_data
def load_data():
  return pd.read_csv("screentime.csv")


try:
  df = load_data()
except Exception as e:
  st.error(
      f"Error loading screentime.csv. Make sure the file is in the folder. Details:"
      f" {e}"
  )
  st.stop()

# --- Sidebar Controls ---
st.sidebar.title("🎛️ Command Center")
st.sidebar.markdown("Manage your daily digital boundaries.")

# Date Filter Selector
available_dates = sorted(df["Date"].unique())
selected_date = st.sidebar.selectbox("Select Date to Analyze", available_dates)

# Daily Goal Slider (in hours, converted to minutes)
daily_goal_hours = st.sidebar.slider(
    "Daily Screen Time Goal (Hours)", min_value=1, max_value=12, value=4
)
daily_goal_minutes = daily_goal_hours * 60

# --- Main Dashboard Layout ---
st.title("🧠 Life-OS Wellbeing Dashboard")
st.markdown(
    "Your personalized command center for digital detox and extreme"
    " accountability."
)
st.divider()

# Filter data for selected day
day_data = df[df["Date"] == selected_date]

if day_data.empty:
  st.warning(f"No data found for {selected_date}.")
else:
  # Compute Metrics
  total_minutes = int(day_data["Minutes_Used"].sum())
  total_hours = round(total_minutes / 60, 1)

  # Most used app of the day
  most_used_row = day_data.loc[day_data["Minutes_Used"].idxmax()]
  top_app = f"{most_used_row['App_Name']} ({most_used_row['Minutes_Used']}m)"

  # Delta against goal
  diff_from_goal = total_minutes - daily_goal_minutes

  # --- KPI Row (`st.metric` + `st.columns`) ---
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric(
        label=f"Total Screen Time ({selected_date})", value=f"{total_hours} hrs"
    )

  with col2:
    st.metric(label="Most Used App Today", value=top_app)

  with col3:
    st.metric(
        label="Vs. Daily Goal",
        value=f"{abs(diff_from_goal)} mins {'Over' if diff_from_goal > 0 else 'Under'}",
        delta=f"{-diff_from_goal}m limit buffer"
        if diff_from_goal <= 0
        else f"+{diff_from_goal}m over",
        delta_color="inverse",
    )

  st.divider()

  # --- Visualizations ---
  col_left, col_right = st.columns(2)

  with col_left:
    st.subheader("📊 Category Breakdown Today")
    category_summary = (
        day_data.groupby("Category")["Minutes_Used"].sum().reset_index()
    )
    st.bar_chart(
        category_summary, x="Category", y="Minutes_Used", color="#FF4B4B"
    )

  with col_right:
    st.subheader("📈 14-Day Trend Overview")
    trend_summary = df.groupby("Date")["Minutes_Used"].sum().reset_index()
    st.line_chart(trend_summary, x="Date", y="Minutes_Used", color="#00CC96")

  st.divider()

  # --- Phase 3: AI Integration (Gemini Life Coach) ---
  st.subheader("🤖 Gemini Life Coach Analysis")

  if st.button("Generate Brutal-But-Fair Coaching Feedback", type="primary"):
    if not client:
      st.error(
          "Gemini API Key is missing. Please configure it in your environment or"
          " Streamlit secrets."
      )
    else:
      with st.spinner("Analyzing your digital habits..."):
        # Convert day data into a clean string representation for the AI bridge
        data_string = day_data[
            ["App_Name", "Category", "Minutes_Used"]
        ].to_string(index=False)

        # Build System Prompt
        prompt = f"""
                You are a holistic, brutal-but-fair personal lifestyle and productivity coach. 
                Here is the user's screen time breakdown for {selected_date}:
                {data_string}

                Total screen time today: {total_minutes} minutes.
                User's daily max limit goal: {daily_goal_minutes} minutes.

                Task:
                1. Critically analyze the user's application and category breakdown. Do not just say "use your phone less."
                2. Call out specific apps or doomscrolling patterns if usage is high.
                3. Suggest concrete, real-world physical replacements for that wasted time (e.g., swapping social media time for physical fitness, cooking, reading a book, or going outside).
                4. Maintain a sharp, motivating, no-excuses tone. Keep it structured and punchy.
                """

        try:
          response = client.models.generate_content(
              model="gemini-3.6-flash",
              contents=prompt,
          )

          # Render output based on severity
          if diff_from_goal > 60:
            st.warning(
                "🚨 **Severe Overconsumption Detected:** Your screen time"
                " heavily breached your target limit today."
            )
          elif diff_from_goal > 0:
            st.info(
                "⚠️ **Slightly Over Limit:** You crossed your goal, but it's"
                " salvageable."
            )
          else:
            st.success(
                "🎉 **Goal Achieved:** Great digital discipline maintained"
                " today!"
            )

          st.markdown(response.text)

        except Exception as e:
          st.error(f"Error generating AI feedback: {e}")
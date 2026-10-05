
import streamlit as st
import pandas as pd
import ollama


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartPick AI",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f7f9fc;
}

/* Main width */

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    background: linear-gradient(
        135deg,
        #172554 0%,
        #1e3a8a 55%,
        #2563eb 100%
    );

    border-radius: 24px;

    padding: 42px 46px;

    margin-bottom: 28px;

    box-shadow:
        0 14px 35px rgba(30, 64, 175, 0.18);
}

.hero h1 {
    color: white !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 10px !important;
}

.hero p {
    color: #dbeafe !important;
    font-size: 17px;
    max-width: 650px;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

h2, h3 {
    color: #172033 !important;
}

h2 {
    font-weight: 800 !important;
}

h3 {
    font-weight: 700 !important;
}

p {
    color: #596579;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8ecf3;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    color: #172033;
}


/* =========================================================
   CARDS
   ========================================================= */

.card {
    background: white;
    border: 1px solid #e7ebf2;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.05);

    transition: 0.2s ease;
}

.card:hover {
    border-color: #b9c7ee;
    box-shadow:
        0 9px 25px rgba(30, 64, 175, 0.09);
    transform: translateY(-2px);
}


/* =========================================================
   PHONE CARD
   ========================================================= */

.phone-card {
    background: #ffffff;

    border: 1px solid #e5eaf2;

    border-radius: 20px;

    padding: 24px;

    margin-bottom: 20px;

    box-shadow:
        0 6px 20px rgba(15, 23, 42, 0.06);

    transition: all 0.2s ease;
}

.phone-card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 12px 28px rgba(15, 23, 42, 0.10);

    border-color: #aabcf0;
}

.phone-name {
    font-size: 23px;
    font-weight: 800;
    color: #172033;
}

.phone-brand {
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
}

.phone-price {
    color: #1d4ed8;
    font-size: 26px;
    font-weight: 800;
}

.badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 20px;
    background: #eef4ff;
    color: #1d4ed8;
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
}

.badge-gold {
    background: #fff7df;
    color: #9a6700;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    border-radius: 11px !important;

    min-height: 44px;

    background: #ffffff;

    color: #24324a;

    border: 1px solid #d9e0eb;

    font-weight: 650;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #f5f8ff !important;

    color: #1d4ed8 !important;

    border-color: #9db1e8 !important;

    box-shadow:
        0 5px 14px rgba(37, 99, 235, 0.10);

    transform: translateY(-1px);
}


/* Primary buttons */

.primary-btn button {
    background: #2563eb !important;

    color: white !important;

    border: none !important;

    font-weight: 750 !important;
}

.primary-btn button:hover {
    background: #1d4ed8 !important;

    color: white !important;
}


/* =========================================================
   METRICS
   ========================================================= */

div[data-testid="stMetric"] {
    background: #f8fafc;

    border: 1px solid #e7ebf2;

    border-radius: 13px;

    padding: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {
    color: #172033 !important;
    font-weight: 800 !important;
}


/* =========================================================
   CHAT
   ========================================================= */

div[data-testid="stChatMessage"] {
    border-radius: 16px;
}

div[data-testid="stChatInput"] {
    border-radius: 14px;
}


/* =========================================================
   TABLE
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e5eaf2;
    border-radius: 14px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    padding: 30px 0 10px;
    color: #7b8798;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv("data/smartphones.csv")


try:

    data = load_data()

except Exception as e:

    st.error("Unable to load smartphone database.")

    st.code("""
SMARTPICK AI/
│
├── app.py
├── requirements.txt
│
└── data/
    └── smartphones.csv
""")

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📱 SmartPick AI</div>',
        unsafe_allow_html=True
    )

    st.caption("AI-powered smartphone discovery")

    st.divider()

    st.markdown("### 🎯 Your preferences")

   
    budget = st.sidebar.slider(
    "Maximum Budget",
    min_value=5000,
    max_value=100000,
    value=30000,
    step=1000,
    format="₹%d"
)

    ram = st.selectbox(
        "Minimum RAM",
        ["Any", "6 GB", "8 GB"]
    )

    network = st.selectbox(
        "Network",
        ["Any", "5G"]
    )

    priority = st.selectbox(
        "Your priority",
        [
            "Overall",
            "Gaming",
            "Camera",
            "Battery"
        ]
    )

    st.divider()

    st.markdown("### 📊 Database")

    st.metric(
        "Available smartphones",
        len(data)
    )

    st.caption(
        "Use the AI assistant below for personalized questions."
    )


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<h1>Find your perfect smartphone.</h1>

<p>
SmartPick AI helps you discover the right phone based on
your budget, gaming needs, camera preferences, battery
requirements and more.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SEARCH
# ============================================================

st.subheader("🔎 Explore smartphones")

search = st.text_input(
    "Search by brand or model",
    placeholder="Try: Samsung, OnePlus, iQOO, Poco..."
)


if search:

    results = data[
        data["brand"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        data["model"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if results.empty:

        st.info(
            "No smartphones found for your search."
        )

    else:

        st.caption(
            f"{len(results)} smartphone(s) found"
        )

        cols = st.columns(3)

        for i, (_, phone) in enumerate(
            results.head(9).iterrows()
        ):

            with cols[i % 3]:

                st.markdown(
                    f"""
                    <div class="phone-card">

                    <div class="phone-brand">
                    {phone['brand']}
                    </div>

                    <div class="phone-name">
                    {phone['model']}
                    </div>

                    <br>

                    <div class="phone-price">
                    ₹{int(phone['price']):,}
                    </div>

                    <br>

                    <span class="badge">
                    {phone['ram']} GB RAM
                    </span>

                    <span class="badge">
                    {phone['storage']} GB
                    </span>

                    <br><br>

                    ⭐ {phone['rating']} &nbsp; • &nbsp;
                    {phone['network']}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def recommend_phones(
    data,
    budget,
    ram,
    network,
    priority
):

    filtered = data[
        data["price"] <= budget
    ].copy()


    if ram != "Any":

        ram_value = int(
            ram.split()[0]
        )

        filtered = filtered[
            filtered["ram"] >= ram_value
        ]


    if network != "Any":

        filtered = filtered[
            filtered["network"] == network
        ]


    if filtered.empty:

        return filtered


    if priority == "Gaming":

        filtered["score"] = (
            filtered["gaming_score"] * 0.7
            + filtered["rating"] * 20 * 0.3
        )


    elif priority == "Camera":

        filtered["score"] = (
            filtered["camera_score"] * 0.7
            + filtered["rating"] * 20 * 0.3
        )


    elif priority == "Battery":

        filtered["score"] = (
            filtered["battery_score"] * 0.7
            + filtered["rating"] * 20 * 0.3
        )


    else:

        filtered["score"] = (
            filtered["gaming_score"] * 0.25
            + filtered["camera_score"] * 0.25
            + filtered["battery_score"] * 0.25
            + filtered["rating"] * 20 * 0.25
        )


    return filtered.sort_values(
        "score",
        ascending=False
    ).head(3)


# ============================================================
# PERSONALIZED RECOMMENDATION
# ============================================================

st.divider()

st.subheader("🎯 Personalized recommendations")

st.write(
    "Set your preferences in the sidebar and let SmartPick AI "
    "find the best matches."
)


if st.button(
    "✨ Find My Best Phone",
    use_container_width=True
):

    st.session_state.recommendations = recommend_phones(
        data,
        budget,
        ram,
        network,
        priority
    )


recommendations = st.session_state.recommendations


if recommendations is not None:

    if recommendations.empty:

        st.warning(
            "No smartphones match your requirements. "
            "Try increasing your budget or changing your preferences."
        )

    else:

        st.success(
            f"SmartPick found {len(recommendations)} strong matches."
        )


        for position, (_, phone) in enumerate(
            recommendations.iterrows(),
            1
        ):

            badge = (
                "🏆 TOP PICK"
                if position == 1
                else f"#{position} MATCH"
            )


            st.markdown(
                f"""
                <div class="phone-card">

                <span class="badge badge-gold">
                {badge}
                </span>

                <br><br>

                <div class="phone-brand">
                {phone['brand']}
                </div>

                <div class="phone-name">
                {phone['model']}
                </div>

                <div class="phone-price">
                ₹{int(phone['price']):,}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "RAM",
                    f"{phone['ram']} GB"
                )

            with c2:
                st.metric(
                    "Storage",
                    f"{phone['storage']} GB"
                )

            with c3:
                st.metric(
                    "Rating",
                    f"{phone['rating']} ⭐"
                )

            with c4:
                st.metric(
                    "Network",
                    phone["network"]
                )


            with st.expander(
                f"View {phone['model']} specifications"
            ):

                left, right = st.columns(2)

                with left:

                    st.write(
                        f"**Processor:** {phone['processor']}"
                    )

                    st.write(
                        f"**Camera:** {phone['camera']}"
                    )

                    st.write(
                        f"**Battery:** {phone['battery']}"
                    )

                    st.write(
                        f"**Display:** {phone['display']}"
                    )

                with right:

                    st.write(
                        f"**Refresh rate:** {phone['refresh_rate']}"
                    )

                    st.write(
                        f"**Charging:** {phone['charging']}"
                    )

                    st.write(
                        f"**Gaming score:** {phone['gaming_score']}/100"
                    )

                    st.write(
                        f"**Camera score:** {phone['camera_score']}/100"
                    )


# ============================================================
# CATEGORY PICKS
# ============================================================

st.divider()

st.subheader("🔥 Popular picks")

category = st.selectbox(
    "Choose a category",
    [
        "Best Overall",
        "Best Gaming",
        "Best Camera",
        "Best Battery",
        "Best Value"
    ]
)


if category == "Best Gaming":

    popular = data.sort_values(
        "gaming_score",
        ascending=False
    ).head(6)


elif category == "Best Camera":

    popular = data.sort_values(
        "camera_score",
        ascending=False
    ).head(6)


elif category == "Best Battery":

    popular = data.sort_values(
        "battery_score",
        ascending=False
    ).head(6)


elif category == "Best Value":

    data_copy = data.copy()

    data_copy["value"] = (
        data_copy["gaming_score"]
        + data_copy["camera_score"]
        + data_copy["battery_score"]
    ) / data_copy["price"]

    popular = data_copy.sort_values(
        "value",
        ascending=False
    ).head(6)


else:

    data_copy = data.copy()

    data_copy["overall"] = (
        data_copy["gaming_score"]
        + data_copy["camera_score"]
        + data_copy["battery_score"]
        + data_copy["rating"] * 20
    ) / 4

    popular = data_copy.sort_values(
        "overall",
        ascending=False
    ).head(6)


cards = st.columns(3)


for i, (_, phone) in enumerate(
    popular.iterrows()
):

    with cards[i % 3]:

        st.markdown(
            f"""
            <div class="phone-card">

            <div class="phone-brand">
            {phone['brand']}
            </div>

            <div class="phone-name">
            {phone['model']}
            </div>

            <br>

            <div class="phone-price">
            ₹{int(phone['price']):,}
            </div>

            <br>

            <span class="badge">
            {phone['ram']} GB RAM
            </span>

            <span class="badge">
            {phone['storage']} GB
            </span>

            <br><br>

            ⭐ {phone['rating']}

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# COMPARE PHONES
# ============================================================

st.divider()

st.subheader("⚖️ Compare smartphones")

st.write(
    "Select two phones to compare their specifications."
)


phone_names = (
    data["brand"] + " " + data["model"]
).tolist()


compare1 = st.selectbox(
    "First smartphone",
    phone_names,
    index=0
)


compare2 = st.selectbox(
    "Second smartphone",
    phone_names,
    index=1
)


if st.button(
    "⚖️ Compare Phones",
    use_container_width=True
):

    phone1 = data[
        (data["brand"] + " " + data["model"])
        == compare1
    ].iloc[0]


    phone2 = data[
        (data["brand"] + " " + data["model"])
        == compare2
    ].iloc[0]


    comparison = pd.DataFrame({

        "Specification": [
            "Price",
            "RAM",
            "Storage",
            "Processor",
            "Camera",
            "Battery",
            "Display",
            "Refresh Rate",
            "Charging",
            "Rating",
            "Gaming Score",
            "Camera Score",
            "Battery Score"
        ],

        compare1: [
            f"₹{int(phone1['price']):,}",
            f"{phone1['ram']} GB",
            f"{phone1['storage']} GB",
            phone1["processor"],
            phone1["camera"],
            phone1["battery"],
            phone1["display"],
            phone1["refresh_rate"],
            phone1["charging"],
            f"{phone1['rating']} ⭐",
            f"{phone1['gaming_score']}/100",
            f"{phone1['camera_score']}/100",
            f"{phone1['battery_score']}/100"
        ],

        compare2: [
            f"₹{int(phone2['price']):,}",
            f"{phone2['ram']} GB",
            f"{phone2['storage']} GB",
            phone2["processor"],
            phone2["camera"],
            phone2["battery"],
            phone2["display"],
            phone2["refresh_rate"],
            phone2["charging"],
            f"{phone2['rating']} ⭐",
            f"{phone2['gaming_score']}/100",
            f"{phone2['camera_score']}/100",
            f"{phone2['battery_score']}/100"
        ]
    })


    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# AI ASSISTANT
# ============================================================

st.divider()

st.subheader("🤖 Talk to SmartPick AI")

st.write(
    "Powered by Llama 3.2. Ask questions naturally — "
    "just like talking to a smartphone expert."
)


def chatbot_response(
    question,
    data
):

    phone_data = data[
        [
            "brand",
            "model",
            "price",
            "ram",
            "storage",
            "processor",
            "camera",
            "battery",
            "display",
            "refresh_rate",
            "charging",
            "network",
            "rating",
            "gaming_score",
            "camera_score",
            "battery_score"
        ]
    ].to_string(index=False)


    system_prompt = f"""
You are SmartPick AI, a professional smartphone shopping
assistant.

Use ONLY the smartphone database below.

Rules:

1. Recommend only phones in the database.
2. Never invent phones.
3. Never invent specifications.
4. Respect the user's budget.
5. Consider gaming, camera, battery, RAM and storage.
6. Explain why your recommendation is suitable.
7. Use Indian Rupees.
8. Keep answers clear and friendly.
9. If no suitable phone exists, say so.
10. For comparisons, use only phones in the database.

DATABASE:

{phone_data}
"""


    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )


        return response["message"]["content"]


    except Exception as e:

        return (
            "⚠️ Llama 3.2 could not connect.\n\n"
            "Please make sure Ollama is running and "
            "the llama3.2 model is installed.\n\n"
            f"Error: {e}"
        )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask SmartPick AI anything..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    with st.chat_message("assistant"):

        with st.spinner(
            "SmartPick AI is thinking..."
        ):

            answer = chatbot_response(
                question,
                data
            )


        st.markdown(answer)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# EXAMPLE PROMPTS
# ============================================================

st.markdown("### 💬 Try these")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.caption("🎮 Best gaming phone under ₹22,000")

with p2:
    st.caption("📸 Best camera phone under ₹25,000")

with p3:
    st.caption("🔋 Best battery phone")

with p4:
    st.caption("⚖️ Compare iQOO Z9 and Poco X6")


# ============================================================
# DATABASE
# ============================================================

st.divider()

with st.expander("📊 Browse complete smartphone database"):

    st.write(
        f"SmartPick AI currently contains "
        f"**{len(data)} smartphones**."
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

📱 <b>SmartPick AI</b><br>

AI-powered smartphone recommendations using
Python, Streamlit, Pandas and Llama 3.2.

</div>
""", unsafe_allow_html=True)


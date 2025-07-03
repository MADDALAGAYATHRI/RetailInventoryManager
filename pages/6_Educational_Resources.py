import streamlit as st
from data.educational_content import EducationalContent

st.set_page_config(page_title="Educational Resources", page_icon="📚", layout="wide")

# Load custom CSS
def load_css():
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize educational content
educational_content = EducationalContent()

st.title("📚 Educational Resources & Coping Strategies")
st.markdown("*Learn about mental health and develop effective coping strategies*")

# Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 Understanding Mental Health", 
    "😰 Stress Management", 
    "🧘 Mindfulness & Meditation",
    "💡 Coping Strategies",
    "🆘 Crisis Resources"
])

with tab1:
    st.header("🧠 Understanding Mental Health")
    
    mental_health_content = educational_content.get_mental_health_basics()
    
    for topic in mental_health_content:
        with st.expander(f"📖 {topic['title']}"):
            st.markdown(topic['content'])
            
            if 'key_points' in topic:
                st.markdown("**Key Points:**")
                for point in topic['key_points']:
                    st.markdown(f"• {point}")
            
            if 'resources' in topic:
                st.markdown("**Additional Resources:**")
                for resource in topic['resources']:
                    st.markdown(f"• [{resource['title']}]({resource['url']})")

with tab2:
    st.header("😰 Stress Management Techniques")
    
    stress_content = educational_content.get_stress_management()
    
    # Quick stress relief section
    st.subheader("🚨 Quick Stress Relief (Use Right Now)")
    
    quick_techniques = [
        {
            'title': '4-7-8 Breathing',
            'description': 'A simple breathing technique for immediate calm',
            'steps': [
                'Exhale completely through your mouth',
                'Close your mouth and inhale through nose for 4 counts',
                'Hold your breath for 7 counts',
                'Exhale through mouth for 8 counts',
                'Repeat 3-4 times'
            ]
        },
        {
            'title': '5-4-3-2-1 Grounding',
            'description': 'Grounding technique to reduce anxiety',
            'steps': [
                'Name 5 things you can see',
                'Name 4 things you can touch',
                'Name 3 things you can hear',
                'Name 2 things you can smell',
                'Name 1 thing you can taste'
            ]
        }
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        for technique in quick_techniques:
            with st.container():
                st.markdown(f"**🎯 {technique['title']}**")
                st.markdown(technique['description'])
                st.markdown("**Steps:**")
                for step in technique['steps']:
                    st.markdown(f"• {step}")
                st.markdown("---")
    
    with col2:
        # Stress management timer
        st.markdown("**⏱️ Guided Practice Timer**")
        
        timer_duration = st.selectbox(
            "Choose practice duration:",
            ["1 minute", "3 minutes", "5 minutes", "10 minutes"]
        )
        
        if st.button("Start Guided Session"):
            duration_map = {"1 minute": 1, "3 minutes": 3, "5 minutes": 5, "10 minutes": 10}
            minutes = duration_map[timer_duration]
            
            st.success(f"🧘‍♀️ Starting {minutes}-minute session...")
            st.markdown("*Focus on your breathing. In through the nose, out through the mouth.*")
            
            # Simple progress bar simulation
            import time
            progress_bar = st.progress(0)
            for i in range(minutes * 60):
                time.sleep(1)
                progress_bar.progress((i + 1) / (minutes * 60))
            
            st.balloons()
            st.success("🎉 Great job! You completed your mindfulness session.")
    
    # Detailed stress management content
    st.subheader("📚 Comprehensive Stress Management")
    
    for topic in stress_content:
        with st.expander(f"📖 {topic['title']}"):
            st.markdown(topic['content'])
            
            if 'techniques' in topic:
                st.markdown("**Techniques:**")
                for technique in topic['techniques']:
                    st.markdown(f"• **{technique['name']}**: {technique['description']}")
            
            if 'benefits' in topic:
                st.markdown("**Benefits:**")
                for benefit in topic['benefits']:
                    st.markdown(f"• {benefit}")

with tab3:
    st.header("🧘 Mindfulness & Meditation")
    
    mindfulness_content = educational_content.get_mindfulness_content()
    
    # Guided meditation section
    st.subheader("🎵 Guided Meditations")
    
    meditation_types = [
        {
            'name': 'Body Scan Meditation',
            'duration': '10-20 minutes',
            'description': 'Progressive relaxation through body awareness',
            'script': """
            Find a comfortable position and close your eyes...
            
            Start by taking three deep breaths...
            
            Now bring your attention to the top of your head...
            Notice any sensations, tension, or relaxation...
            
            Slowly move your attention down to your forehead...
            Let any tension melt away...
            
            Continue down to your eyes, cheeks, and jaw...
            Allow each part to relax completely...
            
            Move to your neck and shoulders...
            Feel the weight of stress lifting away...
            
            [Continue this process through each part of your body]
            """
        },
        {
            'name': 'Loving-Kindness Meditation',
            'duration': '5-15 minutes',
            'description': 'Cultivate compassion for yourself and others',
            'script': """
            Sit comfortably and close your eyes...
            
            Begin by focusing on yourself...
            Repeat silently: 'May I be happy, may I be healthy, may I be at peace'...
            
            Now think of someone you love...
            Send them these wishes: 'May you be happy, may you be healthy, may you be at peace'...
            
            Think of a neutral person...
            Extend the same wishes to them...
            
            Finally, think of someone difficult...
            Try to send them these same loving wishes...
            """
        }
    ]
    
    for meditation in meditation_types:
        with st.expander(f"🧘‍♀️ {meditation['name']} ({meditation['duration']})"):
            st.markdown(f"**Description:** {meditation['description']}")
            st.markdown("**Guided Script:**")
            st.markdown(meditation['script'])
            
            if st.button(f"🎧 Start {meditation['name']}", key=f"med_{meditation['name']}"):
                st.info("🎵 Find a quiet space, get comfortable, and follow along with the script above.")
    
    # Mindfulness exercises
    st.subheader("🌟 Daily Mindfulness Exercises")
    
    daily_exercises = [
        "🍽️ **Mindful Eating**: Pay full attention to taste, texture, and smell of your food",
        "🚶‍♀️ **Walking Meditation**: Focus on each step and the sensation of your feet touching the ground",
        "🌬️ **Breath Awareness**: Spend 5 minutes just observing your natural breathing",
        "🎵 **Sound Meditation**: Listen to environmental sounds without judging or labeling them",
        "📱 **Digital Mindfulness**: Take conscious breaks from screens throughout the day"
    ]
    
    for exercise in daily_exercises:
        st.markdown(exercise)

with tab4:
    st.header("💡 Coping Strategies")
    
    coping_content = educational_content.get_coping_strategies()
    
    # Coping strategy categories
    strategy_categories = {
        "🎯 Problem-Focused Coping": [
            "Break large problems into smaller, manageable steps",
            "Create action plans with specific, achievable goals",
            "Seek practical solutions and implement them systematically",
            "Learn new skills to handle challenging situations",
            "Time management and prioritization techniques"
        ],
        "😌 Emotion-Focused Coping": [
            "Practice self-compassion and positive self-talk",
            "Use relaxation techniques like deep breathing",
            "Express emotions through journaling or creative outlets",
            "Reframe negative thoughts into more balanced perspectives",
            "Accept what you cannot change and focus on what you can"
        ],
        "👥 Social Coping": [
            "Reach out to trusted friends and family members",
            "Join support groups or community activities",
            "Share your feelings with someone who listens without judgment",
            "Ask for help when you need it",
            "Maintain social connections even during difficult times"
        ],
        "🏃‍♀️ Physical Coping": [
            "Regular exercise to reduce stress hormones",
            "Maintain consistent sleep schedules",
            "Practice progressive muscle relaxation",
            "Use physical activities as emotional outlets",
            "Spend time in nature for natural stress relief"
        ]
    }
    
    for category, strategies in strategy_categories.items():
        with st.expander(category):
            for strategy in strategies:
                st.markdown(f"• {strategy}")
            
            st.markdown("**💡 Try This:**")
            if "Problem-Focused" in category:
                st.info("Pick one current challenge and break it into 3 smaller steps you can take this week.")
            elif "Emotion-Focused" in category:
                st.info("When you feel overwhelmed, try the 4-7-8 breathing technique for 2 minutes.")
            elif "Social" in category:
                st.info("Reach out to one person today, even if it's just a brief check-in message.")
            elif "Physical" in category:
                st.info("Take a 10-minute walk outside and notice 5 things in nature.")
    
    # Cognitive restructuring tools
    st.subheader("🧠 Cognitive Restructuring Tools")
    
    with st.expander("🔄 Thought Record Exercise"):
        st.markdown("""
        **Use this exercise when you're experiencing negative thoughts:**
        
        1. **Situation**: What happened? (Just the facts)
        2. **Emotion**: What did you feel? Rate intensity 1-10
        3. **Automatic Thought**: What went through your mind?
        4. **Evidence For**: What supports this thought?
        5. **Evidence Against**: What contradicts this thought?
        6. **Balanced Thought**: What's a more balanced perspective?
        7. **New Emotion**: How do you feel now? Rate 1-10
        """)
        
        if st.button("📝 Practice Thought Record"):
            st.info("💭 Take a moment to work through these steps with a recent difficult situation.")

with tab5:
    st.header("🆘 Crisis Resources & Emergency Support")
    
    st.error("⚠️ **If you're in immediate danger or having thoughts of self-harm, please contact emergency services immediately.**")
    
    # Crisis hotlines
    st.subheader("📞 Crisis Hotlines")
    
    crisis_resources = {
        "🇺🇸 United States": [
            "**988 Suicide & Crisis Lifeline**: 988 (24/7, free)",
            "**Crisis Text Line**: Text HOME to 741741",
            "**SAMHSA National Helpline**: 1-800-662-4357",
            "**National Domestic Violence Hotline**: 1-800-799-7233"
        ],
        "🇬🇧 United Kingdom": [
            "**Samaritans**: 116 123 (free, 24/7)",
            "**SHOUT Crisis Text Line**: Text 85258",
            "**Mind Infoline**: 0300 123 3393",
            "**Papyrus (under 35)**: 0800 068 4141"
        ],
        "🇨🇦 Canada": [
            "**Talk Suicide Canada**: 1-833-456-4566",
            "**Kids Help Phone**: 1-800-668-6868",
            "**Good2Talk (post-secondary students)**: 1-866-925-5454"
        ],
        "🇦🇺 Australia": [
            "**Lifeline**: 13 11 14",
            "**Beyond Blue**: 1300 22 4636",
            "**Kids Helpline**: 1800 55 1800"
        ]
    }
    
    for country, resources in crisis_resources.items():
        with st.expander(country):
            for resource in resources:
                st.markdown(resource)
    
    st.markdown("---")
    st.subheader("🔍 Additional Support Resources")
    
    additional_resources = [
        {
            'category': '🏥 Professional Help',
            'resources': [
                "Psychology Today Therapist Directory",
                "NAMI (National Alliance on Mental Illness)",
                "Mental Health America",
                "Your healthcare provider or insurance company"
            ]
        },
        {
            'category': '📱 Mental Health Apps',
            'resources': [
                "Headspace - Meditation and mindfulness",
                "Calm - Sleep stories and relaxation",
                "Talkspace - Online therapy platform",
                "BetterHelp - Professional counseling"
            ]
        },
        {
            'category': '📚 Educational Websites',
            'resources': [
                "National Institute of Mental Health (NIMH)",
                "Mayo Clinic Mental Health Resources",
                "American Psychological Association (APA)",
                "Mental Health Foundation"
            ]
        }
    ]
    
    for resource_group in additional_resources:
        with st.expander(resource_group['category']):
            for resource in resource_group['resources']:
                st.markdown(f"• {resource}")
    
    # Warning signs
    st.subheader("⚠️ Warning Signs to Watch For")
    
    warning_signs = [
        "Persistent thoughts of death or suicide",
        "Feeling hopeless or trapped",
        "Severe anxiety or panic attacks",
        "Inability to perform daily activities",
        "Substance abuse as a coping mechanism",
        "Withdrawal from friends and activities",
        "Extreme mood swings",
        "Talking about being a burden to others"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**If you or someone you know shows these signs:**")
        for sign in warning_signs:
            st.markdown(f"• {sign}")
    
    with col2:
        st.markdown("**Take these steps:**")
        st.markdown("• Contact a crisis hotline immediately")
        st.markdown("• Don't leave the person alone")
        st.markdown("• Remove access to means of self-harm")
        st.markdown("• Get professional help")
        st.markdown("• Call emergency services if in immediate danger")

# Quick reference card
st.markdown("---")
st.subheader("📋 Quick Reference Card")

with st.expander("🆘 Emergency Quick Reference"):
    st.markdown("""
    **In Crisis:**
    - US: 988 Suicide & Crisis Lifeline
    - UK: 116 123 Samaritans
    - Canada: 1-833-456-4566 Talk Suicide Canada
    - Australia: 13 11 14 Lifeline
    
    **Immediate Stress Relief:**
    - 4-7-8 breathing technique
    - 5-4-3-2-1 grounding exercise
    - Call a trusted friend
    - Go to a safe, comfortable space
    
    **Remember:**
    - You are not alone
    - This feeling is temporary
    - Help is available
    - You matter
    """)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("🎯 Get Interventions"):
        st.switch_page("pages/4_Interventions.py")
with col3:
    if st.button("📈 Track Progress"):
        st.switch_page("pages/5_Progress_Tracking.py")

from typing import Dict, List, Any

class EducationalContent:
    """
    Provides educational content about mental health, stress management, and coping strategies.
    """
    
    def __init__(self):
        pass
    
    def get_mental_health_basics(self) -> List[Dict[str, Any]]:
        """Get educational content about mental health basics."""
        return [
            {
                'title': 'Understanding Stress and Its Impact',
                'content': """
                Stress is your body's natural response to challenges and demands. While some stress can be helpful and motivating, chronic stress can have serious impacts on both your physical and mental health.

                **What happens when you're stressed:**
                - Your brain releases stress hormones like cortisol and adrenaline
                - Your heart rate and blood pressure increase
                - Your breathing becomes faster and shallower
                - Your muscles tense up
                - Your digestive system slows down

                **Types of stress:**
                - **Acute stress**: Short-term stress from immediate pressures
                - **Chronic stress**: Long-term stress from ongoing situations
                - **Eustress**: Positive stress that motivates and energizes
                - **Distress**: Negative stress that overwhelms and harms
                """,
                'key_points': [
                    'Not all stress is bad - some stress can be motivating',
                    'Chronic stress can lead to serious health problems',
                    'Your body has a natural stress response system',
                    'Learning to manage stress is a skill that can be developed',
                    'Everyone experiences stress differently'
                ],
                'resources': [
                    {'title': 'American Psychological Association - Stress', 'url': 'https://www.apa.org/topics/stress'},
                    {'title': 'Mayo Clinic - Stress Management', 'url': 'https://www.mayoclinic.org/healthy-lifestyle/stress-management'}
                ]
            },
            {
                'title': 'The Science of Mood and Emotions',
                'content': """
                Your mood is influenced by a complex interplay of biological, psychological, and social factors. Understanding these can help you take better care of your mental health.

                **Biological factors:**
                - Neurotransmitters (serotonin, dopamine, norepinephrine)
                - Hormonal changes (cortisol, thyroid hormones, reproductive hormones)
                - Sleep patterns and circadian rhythms
                - Nutrition and blood sugar levels
                - Physical health and chronic conditions

                **Psychological factors:**
                - Thought patterns and cognitive habits
                - Coping strategies and resilience
                - Past experiences and trauma
                - Self-esteem and self-concept
                - Personality traits

                **Social factors:**
                - Relationships and social support
                - Work and financial stress
                - Cultural and societal pressures
                - Life transitions and changes
                - Environmental factors
                """,
                'key_points': [
                    'Mood is influenced by brain chemistry, but you can influence that chemistry',
                    'Lifestyle factors like sleep, exercise, and nutrition significantly impact mood',
                    'Social connections are crucial for mental health',
                    'Thoughts and emotions are connected but not the same thing',
                    'Professional help is available and effective for mood disorders'
                ]
            },
            {
                'title': 'Mental Health vs. Mental Illness',
                'content': """
                Mental health exists on a continuum, and everyone has mental health just like everyone has physical health.

                **Mental Health includes:**
                - Emotional well-being (feeling good about yourself and life)
                - Psychological well-being (feeling purpose and meaning)
                - Social well-being (having positive relationships)

                **Mental Health Challenges are common:**
                - 1 in 5 adults experience mental health issues each year
                - Mental health challenges can be temporary or ongoing
                - They can range from mild to severe
                - Most mental health conditions are treatable

                **Signs of good mental health:**
                - Ability to cope with life's stresses
                - Productive work and meaningful activities
                - Positive relationships with others
                - Realistic sense of self
                - Ability to adapt to change
                """,
                'key_points': [
                    'Mental health is not just the absence of mental illness',
                    'Everyone can work on improving their mental health',
                    'Mental health challenges are medical conditions, not personal failures',
                    'Recovery and management are possible for all mental health conditions',
                    'Seeking help is a sign of strength, not weakness'
                ]
            },
            {
                'title': 'The Mind-Body Connection',
                'content': """
                Your mental and physical health are intimately connected. What affects one will often affect the other.

                **How mental health affects physical health:**
                - Chronic stress can weaken your immune system
                - Depression can increase risk of heart disease
                - Anxiety can cause digestive issues
                - Sleep problems can affect both mental and physical health

                **How physical health affects mental health:**
                - Exercise releases mood-boosting endorphins
                - Nutrition affects brain function and mood
                - Chronic illness can contribute to depression and anxiety
                - Sleep is crucial for emotional regulation

                **Lifestyle factors that benefit both:**
                - Regular physical activity
                - Adequate sleep (7-9 hours for most adults)
                - Balanced nutrition
                - Social connections
                - Stress management practices
                - Limiting alcohol and avoiding drugs
                """,
                'key_points': [
                    'Taking care of your body helps your mind',
                    'Taking care of your mind helps your body',
                    'Small changes in lifestyle can have big impacts',
                    'Holistic approaches to health are most effective',
                    'Professional help may be needed for both mental and physical health'
                ]
            }
        ]
    
    def get_stress_management(self) -> List[Dict[str, Any]]:
        """Get comprehensive stress management content."""
        return [
            {
                'title': 'Breathing Techniques for Stress Relief',
                'content': """
                Breathing is one of the most powerful tools for managing stress because it's always available and works quickly to activate your body's relaxation response.

                **Why breathing works:**
                - Deep breathing activates the parasympathetic nervous system
                - It increases oxygen to the brain
                - It helps regulate heart rate and blood pressure
                - It gives your mind something to focus on besides stressors
                """,
                'techniques': [
                    {
                        'name': 'Diaphragmatic Breathing',
                        'description': 'Place one hand on chest, one on belly. Breathe so the belly hand moves more than the chest hand.'
                    },
                    {
                        'name': '4-7-8 Breathing',
                        'description': 'Inhale for 4, hold for 7, exhale for 8. Repeat 3-4 times.'
                    },
                    {
                        'name': 'Box Breathing',
                        'description': 'Inhale for 4, hold for 4, exhale for 4, hold for 4. Repeat.'
                    },
                    {
                        'name': 'Alternate Nostril Breathing',
                        'description': 'Use thumb to close right nostril, inhale through left. Switch and exhale through right.'
                    }
                ],
                'benefits': [
                    'Immediate stress relief',
                    'Improved focus and concentration',
                    'Better sleep quality',
                    'Reduced anxiety and panic',
                    'Lower blood pressure'
                ]
            },
            {
                'title': 'Progressive Muscle Relaxation (PMR)',
                'content': """
                PMR is a technique where you systematically tense and then relax different muscle groups in your body. This helps you become aware of physical tension and learn to release it.

                **How PMR works:**
                - Helps distinguish between tension and relaxation
                - Reduces overall muscle tension
                - Calms the nervous system
                - Improves body awareness
                - Can be done anywhere

                **Basic PMR sequence:**
                1. Start with your toes and feet
                2. Move to your legs and thighs
                3. Tense your abdomen and chest
                4. Work through your hands and arms
                5. Tense your shoulders and neck
                6. Finish with your face and scalp

                **For each muscle group:**
                - Tense for 5-7 seconds
                - Release suddenly
                - Relax for 10-15 seconds
                - Notice the difference between tension and relaxation
                """,
                'benefits': [
                    'Reduces muscle tension and pain',
                    'Improves sleep quality',
                    'Helps with anxiety and stress',
                    'Increases body awareness',
                    'Can be adapted for specific problem areas'
                ]
            },
            {
                'title': 'Cognitive Stress Management',
                'content': """
                How you think about stressful situations greatly affects how much stress you feel. Cognitive techniques help you change your thought patterns to reduce stress.

                **Common stress-inducing thought patterns:**
                - Catastrophizing (imagining the worst)
                - All-or-nothing thinking
                - Mind reading (assuming you know what others think)
                - Fortune telling (predicting negative outcomes)
                - Personalization (blaming yourself for everything)

                **Helpful cognitive strategies:**
                - Challenge negative thoughts with evidence
                - Practice realistic thinking
                - Focus on what you can control
                - Use positive self-talk
                - Practice acceptance of things you cannot change
                """,
                'techniques': [
                    {
                        'name': 'Thought Record',
                        'description': 'Write down the situation, your automatic thought, evidence for/against, and a more balanced thought.'
                    },
                    {
                        'name': 'The 3 Cs',
                        'description': 'Ask: Can I Control this? If not, Can I Change my response? Can I Cope with this?'
                    },
                    {
                        'name': 'Reframing',
                        'description': 'Look at the situation from different perspectives. What would you tell a friend?'
                    }
                ]
            },
            {
                'title': 'Time Management and Organization',
                'content': """
                Poor time management is a major source of stress. Learning to organize your time effectively can significantly reduce stress levels.

                **Common time management stressors:**
                - Procrastination
                - Overcommitment
                - Poor prioritization
                - Lack of boundaries
                - Perfectionism

                **Effective time management strategies:**
                - Use a calendar or planner
                - Break large tasks into smaller steps
                - Set realistic deadlines
                - Learn to say no
                - Build in buffer time
                - Take regular breaks
                """,
                'techniques': [
                    {
                        'name': 'Eisenhower Matrix',
                        'description': 'Categorize tasks as Urgent/Important, Important/Not Urgent, Urgent/Not Important, Neither.'
                    },
                    {
                        'name': 'Pomodoro Technique',
                        'description': 'Work for 25 minutes, then take a 5-minute break. Repeat.'
                    },
                    {
                        'name': 'Time Blocking',
                        'description': 'Schedule specific blocks of time for different activities.'
                    }
                ]
            }
        ]
    
    def get_mindfulness_content(self) -> List[Dict[str, Any]]:
        """Get mindfulness and meditation content."""
        return [
            {
                'title': 'Introduction to Mindfulness',
                'content': """
                Mindfulness is the practice of paying attention to the present moment without judgment. It's about being fully aware of what's happening right now, rather than being caught up in thoughts about the past or future.

                **Core elements of mindfulness:**
                - **Attention**: Focusing on the present moment
                - **Awareness**: Noticing thoughts, feelings, and sensations
                - **Acceptance**: Observing without trying to change or judge
                - **Non-attachment**: Not getting caught up in thoughts or emotions

                **Benefits of mindfulness practice:**
                - Reduced stress and anxiety
                - Improved emotional regulation
                - Better focus and concentration
                - Increased self-awareness
                - Enhanced relationships
                - Better sleep quality
                - Reduced symptoms of depression
                """,
                'practices': [
                    'Mindful breathing',
                    'Body scan meditation',
                    'Mindful walking',
                    'Mindful eating',
                    'Loving-kindness meditation'
                ]
            },
            {
                'title': 'Basic Meditation Techniques',
                'content': """
                Meditation is a formal practice of mindfulness. There are many different types, but they all involve training your attention and awareness.

                **Getting started with meditation:**
                - Start with just 5-10 minutes
                - Find a quiet, comfortable place
                - Sit in a comfortable position
                - Close your eyes or soften your gaze
                - Don't worry about "doing it right"
                - Be patient with yourself

                **Common meditation challenges:**
                - Racing thoughts (this is normal!)
                - Physical discomfort
                - Falling asleep
                - Feeling like you're "not good at it"
                - Lack of time
                """,
                'types': [
                    {
                        'name': 'Breath Focus Meditation',
                        'description': 'Focus attention on your breathing, noticing when your mind wanders and gently returning to the breath.'
                    },
                    {
                        'name': 'Body Scan',
                        'description': 'Systematically focus on different parts of your body, noticing sensations without trying to change them.'
                    },
                    {
                        'name': 'Loving-Kindness',
                        'description': 'Practice sending good wishes to yourself and others: "May you be happy, may you be healthy, may you be at peace."'
                    },
                    {
                        'name': 'Walking Meditation',
                        'description': 'Practice mindfulness while walking slowly, focusing on the sensations of each step.'
                    }
                ]
            }
        ]
    
    def get_coping_strategies(self) -> List[Dict[str, Any]]:
        """Get comprehensive coping strategies."""
        return [
            {
                'title': 'Problem-Focused vs. Emotion-Focused Coping',
                'content': """
                There are two main types of coping strategies, and the best approach often involves using both depending on the situation.

                **Problem-Focused Coping:**
                Use when you can change or influence the situation.
                - Identify the problem clearly
                - Brainstorm possible solutions
                - Evaluate pros and cons of each option
                - Choose and implement the best solution
                - Evaluate the results and adjust if needed

                **Emotion-Focused Coping:**
                Use when you cannot change the situation but need to manage your emotional response.
                - Accept what you cannot control
                - Use relaxation techniques
                - Seek emotional support
                - Practice self-compassion
                - Find meaning or positive aspects
                """,
                'examples': {
                    'Problem-Focused': [
                        'Creating a study schedule for an exam',
                        'Having a conversation to resolve a conflict',
                        'Learning new skills for job challenges',
                        'Setting boundaries with difficult people'
                    ],
                    'Emotion-Focused': [
                        'Practicing breathing exercises during anxiety',
                        'Talking to friends about feelings',
                        'Using mindfulness during grief',
                        'Journaling about difficult emotions'
                    ]
                }
            },
            {
                'title': 'Building Resilience',
                'content': """
                Resilience is your ability to bounce back from difficult experiences and adapt to challenges. It's not something you're born with - it can be developed.

                **Key components of resilience:**
                - **Emotional regulation**: Managing intense emotions
                - **Cognitive flexibility**: Adapting your thinking to new situations
                - **Social support**: Having people you can rely on
                - **Self-efficacy**: Believing in your ability to handle challenges
                - **Purpose and meaning**: Having something that motivates you

                **Ways to build resilience:**
                - Practice self-care regularly
                - Develop strong relationships
                - Learn from past experiences
                - Maintain perspective during difficulties
                - Take action even when you feel overwhelmed
                - Accept that change is part of life
                """,
                'daily_practices': [
                    'Practice gratitude',
                    'Connect with others',
                    'Take care of your physical health',
                    'Learn something new',
                    'Help others',
                    'Practice mindfulness'
                ]
            },
            {
                'title': 'Crisis Coping Skills',
                'content': """
                Sometimes you need immediate coping strategies for intense emotional distress. These skills can help you get through crisis moments safely.

                **TIPP for Crisis Situations:**
                - **Temperature**: Use cold water on your face or hold ice cubes
                - **Intense Exercise**: Do jumping jacks or run in place for a few minutes
                - **Paced Breathing**: Breathe out longer than you breathe in
                - **Progressive Muscle Relaxation**: Tense and release muscle groups

                **Distress Tolerance Skills:**
                - **Distraction**: Engage in activities that take your mind off the problem temporarily
                - **Self-Soothing**: Use your five senses to comfort yourself
                - **Improving the Moment**: Use imagery, prayer, or encouragement to get through
                - **Pros and Cons**: Think through the consequences of different actions
                """,
                'emergency_strategies': [
                    'Call a crisis helpline',
                    'Reach out to a trusted friend or family member',
                    'Go to a safe place',
                    'Remove yourself from harmful situations',
                    'Use grounding techniques (5-4-3-2-1)',
                    'Practice safe behaviors until the crisis passes'
                ]
            }
        ]
    
    def get_sleep_and_mental_health(self) -> Dict[str, Any]:
        """Get information about sleep and mental health connection."""
        return {
            'title': 'Sleep and Mental Health',
            'content': """
            Sleep and mental health have a bidirectional relationship - poor sleep can worsen mental health, and mental health problems can disrupt sleep.

            **How sleep affects mental health:**
            - Sleep helps process emotions and consolidate memories
            - Lack of sleep increases stress hormones
            - Poor sleep affects mood regulation
            - Sleep deprivation can worsen anxiety and depression

            **How mental health affects sleep:**
            - Anxiety can make it hard to fall asleep
            - Depression can cause early morning waking
            - Racing thoughts can keep you awake
            - Medications can affect sleep patterns
            """,
            'sleep_hygiene_tips': [
                'Keep a consistent sleep schedule',
                'Create a relaxing bedtime routine',
                'Make your bedroom dark, quiet, and cool',
                'Avoid screens for 1 hour before bed',
                'Limit caffeine after 2 PM',
                'Get natural light during the day',
                'Use your bed only for sleep and intimacy',
                'If you can\'t sleep, get up and do a quiet activity'
            ]
        }
    
    def get_nutrition_and_mood(self) -> Dict[str, Any]:
        """Get information about nutrition's impact on mood."""
        return {
            'title': 'Nutrition and Mood',
            'content': """
            What you eat directly affects your brain function and mood. A balanced diet can support mental health, while poor nutrition can worsen mental health symptoms.

            **Nutrients important for mental health:**
            - **Omega-3 fatty acids**: Found in fish, walnuts, and flaxseeds
            - **Complex carbohydrates**: Found in whole grains, vegetables
            - **Protein**: Helps produce neurotransmitters
            - **B vitamins**: Important for brain function
            - **Vitamin D**: Low levels linked to depression
            - **Magnesium**: Helps with anxiety and sleep
            """,
            'mood_supporting_foods': [
                'Fatty fish (salmon, sardines)',
                'Leafy green vegetables',
                'Berries and colorful fruits',
                'Nuts and seeds',
                'Whole grains',
                'Legumes and beans',
                'Dark chocolate (in moderation)',
                'Fermented foods (yogurt, kefir)'
            ],
            'foods_to_limit': [
                'Highly processed foods',
                'Excessive sugar',
                'Too much caffeine',
                'Alcohol',
                'Trans fats',
                'Foods high in sodium'
            ]
        }

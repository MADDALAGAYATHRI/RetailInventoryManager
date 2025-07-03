import random
from typing import Dict, List, Any
import pandas as pd

class InterventionEngine:
    """
    Provides personalized stress intervention recommendations based on user profile and current state.
    """
    
    def __init__(self):
        self.interventions_db = self._initialize_interventions()
        self.immediate_interventions_db = self._initialize_immediate_interventions()
    
    def _initialize_interventions(self) -> List[Dict[str, Any]]:
        """Initialize the interventions database."""
        return [
            # Physical Interventions
            {
                'title': 'Progressive Muscle Relaxation',
                'category': 'Physical',
                'icon': '💪',
                'duration': '10-15 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Evening',
                'description': 'Systematically tense and release muscle groups to reduce physical tension and stress.',
                'benefits': [
                    'Reduces muscle tension',
                    'Improves sleep quality',
                    'Lowers blood pressure',
                    'Increases body awareness'
                ],
                'steps': [
                    'Find a comfortable position lying down or sitting',
                    'Start with your toes - tense for 5 seconds, then release',
                    'Move up through your legs, abdomen, arms, and face',
                    'Hold each tension for 5 seconds, then relax for 10 seconds',
                    'Notice the contrast between tension and relaxation',
                    'End with 3 deep breaths'
                ],
                'conditions': {'stress_level': 'high', 'energy_level': 'any'}
            },
            {
                'title': '10-Minute Nature Walk',
                'category': 'Physical',
                'icon': '🌳',
                'duration': '10 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Anytime',
                'description': 'A short walk in nature to reset your mind and reduce stress hormones.',
                'benefits': [
                    'Reduces cortisol levels',
                    'Improves mood',
                    'Increases vitamin D',
                    'Provides fresh perspective'
                ],
                'steps': [
                    'Step outside to the nearest green space',
                    'Walk at a comfortable pace',
                    'Focus on your surroundings - trees, birds, sounds',
                    'Take deep breaths of fresh air',
                    'Notice how your body feels',
                    'Return feeling refreshed'
                ],
                'conditions': {'stress_level': 'moderate', 'exercise_minutes': 'low'}
            },
            {
                'title': 'Desk Yoga Sequence',
                'category': 'Physical',
                'icon': '🧘‍♀️',
                'duration': '5-8 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Work breaks',
                'description': 'Simple yoga stretches you can do at your desk to relieve tension.',
                'benefits': [
                    'Relieves neck and shoulder tension',
                    'Improves posture',
                    'Increases circulation',
                    'Reduces eye strain'
                ],
                'steps': [
                    'Neck rolls - slow circles in both directions',
                    'Shoulder shrugs - lift and release',
                    'Seated spinal twist - both sides',
                    'Forward fold - reach for your toes',
                    'Wrist circles and stretches',
                    'Deep breathing to finish'
                ],
                'conditions': {'work_hours': 'high', 'stress_level': 'moderate'}
            },
            
            # Mental Interventions
            {
                'title': '4-7-8 Breathing Technique',
                'category': 'Mental',
                'icon': '🌬️',
                'duration': '3-5 minutes',
                'difficulty': 'Beginner',
                'best_time': 'When stressed',
                'description': 'A powerful breathing pattern that activates the parasympathetic nervous system.',
                'benefits': [
                    'Reduces anxiety quickly',
                    'Lowers heart rate',
                    'Improves focus',
                    'Activates relaxation response'
                ],
                'steps': [
                    'Sit comfortably with your back straight',
                    'Exhale completely through your mouth',
                    'Close your mouth and inhale through nose for 4 counts',
                    'Hold your breath for 7 counts',
                    'Exhale through mouth for 8 counts',
                    'Repeat 3-4 cycles'
                ],
                'guided_script': 'Breathe in for 4... hold for 7... out for 8. Feel your body relaxing with each breath.',
                'conditions': {'stress_level': 'high', 'anxiety': 'present'}
            },
            {
                'title': 'Mindful Observation Exercise',
                'category': 'Mental',
                'icon': '👁️',
                'duration': '5-10 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Anytime',
                'description': 'Practice mindfulness by observing your environment without judgment.',
                'benefits': [
                    'Grounds you in the present',
                    'Reduces racing thoughts',
                    'Improves focus',
                    'Develops mindfulness skills'
                ],
                'steps': [
                    'Choose an object or view to observe',
                    'Look at it as if seeing it for the first time',
                    'Notice colors, textures, shapes, shadows',
                    'When your mind wanders, gently return focus',
                    'Spend 30 seconds on each detail you notice',
                    'End by appreciating what you observed'
                ],
                'conditions': {'stress_level': 'moderate', 'focus': 'low'}
            },
            {
                'title': 'Gratitude Journaling',
                'category': 'Mental',
                'icon': '📝',
                'duration': '5-10 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Evening',
                'description': 'Write down things you\'re grateful for to shift focus to positive aspects of life.',
                'benefits': [
                    'Improves mood',
                    'Increases life satisfaction',
                    'Reduces negative thinking',
                    'Enhances sleep quality'
                ],
                'steps': [
                    'Get a notebook or use your phone',
                    'Write down 3-5 things you\'re grateful for today',
                    'Be specific - instead of "family" write "my sister\'s encouraging text"',
                    'Include why you\'re grateful for each item',
                    'Notice how you feel as you write',
                    'Review previous entries occasionally'
                ],
                'conditions': {'mood_score': 'low', 'stress_level': 'moderate'}
            },
            
            # Social Interventions
            {
                'title': 'Reach Out to a Friend',
                'category': 'Social',
                'icon': '📞',
                'duration': '10-30 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Anytime',
                'description': 'Connect with someone you trust for emotional support and perspective.',
                'benefits': [
                    'Reduces feelings of isolation',
                    'Provides emotional support',
                    'Gains new perspectives',
                    'Strengthens relationships'
                ],
                'steps': [
                    'Think of someone who makes you feel better',
                    'Call, text, or video chat with them',
                    'Share what\'s on your mind if comfortable',
                    'Ask about their day too',
                    'Express gratitude for their time',
                    'Plan to connect again soon'
                ],
                'conditions': {'social_interaction': 'low', 'stress_level': 'high'}
            },
            {
                'title': 'Practice Active Listening',
                'category': 'Social',
                'icon': '👂',
                'duration': '15-20 minutes',
                'difficulty': 'Intermediate',
                'best_time': 'During conversations',
                'description': 'Focus completely on understanding someone else, which can reduce your own stress.',
                'benefits': [
                    'Strengthens relationships',
                    'Reduces self-focus',
                    'Improves empathy',
                    'Creates positive connections'
                ],
                'steps': [
                    'Choose a conversation partner',
                    'Put away distractions (phone, etc.)',
                    'Make eye contact and listen without planning your response',
                    'Ask clarifying questions',
                    'Reflect back what you heard',
                    'Thank them for sharing'
                ],
                'conditions': {'social_interaction': 'moderate', 'mood_score': 'low'}
            },
            
            # Lifestyle Interventions
            {
                'title': 'Digital Detox Hour',
                'category': 'Lifestyle',
                'icon': '📱',
                'duration': '60 minutes',
                'difficulty': 'Intermediate',
                'best_time': 'Evening',
                'description': 'Take a complete break from digital devices to reduce overstimulation.',
                'benefits': [
                    'Reduces mental overstimulation',
                    'Improves sleep preparation',
                    'Increases present-moment awareness',
                    'Reduces comparison and FOMO'
                ],
                'steps': [
                    'Turn off all digital devices',
                    'Inform others you\'ll be unavailable',
                    'Engage in analog activities (reading, drawing, etc.)',
                    'Notice urges to check devices without acting',
                    'Focus on physical sensations and environment',
                    'Reflect on how you feel afterward'
                ],
                'conditions': {'stress_level': 'high', 'work_hours': 'high'}
            },
            {
                'title': 'Create a Calming Environment',
                'category': 'Lifestyle',
                'icon': '🕯️',
                'duration': '15-20 minutes',
                'difficulty': 'Beginner',
                'best_time': 'Evening',
                'description': 'Modify your space to promote relaxation and reduce stress triggers.',
                'benefits': [
                    'Creates psychological safety',
                    'Reduces environmental stress',
                    'Improves mood',
                    'Promotes better sleep'
                ],
                'steps': [
                    'Dim harsh lighting or light candles',
                    'Play soft, calming music',
                    'Remove clutter from immediate view',
                    'Add something pleasant-smelling (tea, essential oils)',
                    'Arrange comfortable seating',
                    'Enjoy the peaceful atmosphere'
                ],
                'conditions': {'stress_level': 'moderate', 'energy_level': 'low'}
            },
            {
                'title': 'Sleep Hygiene Routine',
                'category': 'Lifestyle',
                'icon': '😴',
                'duration': '30-45 minutes',
                'difficulty': 'Intermediate',
                'best_time': 'Before bed',
                'description': 'Establish a consistent pre-sleep routine to improve sleep quality.',
                'benefits': [
                    'Improves sleep quality',
                    'Reduces next-day stress',
                    'Regulates circadian rhythm',
                    'Creates relaxing ritual'
                ],
                'steps': [
                    'Set a consistent bedtime',
                    'Turn off screens 1 hour before bed',
                    'Take a warm bath or shower',
                    'Do gentle stretching or reading',
                    'Practice gratitude or meditation',
                    'Keep bedroom cool and dark'
                ],
                'conditions': {'sleep_hours': 'low', 'stress_level': 'any'}
            }
        ]
    
    def _initialize_immediate_interventions(self) -> List[Dict[str, Any]]:
        """Initialize immediate stress relief interventions."""
        return [
            {
                'title': 'Emergency Calm Breathing',
                'duration': '2 minutes',
                'description': 'Quick breathing technique for immediate stress relief.',
                'steps': [
                    'Stop what you\'re doing and sit down',
                    'Place one hand on chest, one on belly',
                    'Breathe slowly through your nose for 4 counts',
                    'Feel your belly rise more than your chest',
                    'Exhale slowly through mouth for 6 counts',
                    'Repeat 5-10 times until you feel calmer'
                ],
                'audio_guide': 'Breathe in... 2... 3... 4... Hold... Breathe out... 2... 3... 4... 5... 6...'
            },
            {
                'title': '5-4-3-2-1 Grounding',
                'duration': '3 minutes',
                'description': 'Sensory grounding technique to manage acute anxiety.',
                'steps': [
                    'Name 5 things you can see around you',
                    'Name 4 things you can physically touch',
                    'Name 3 things you can hear right now',
                    'Name 2 things you can smell',
                    'Name 1 thing you can taste',
                    'Take three deep breaths'
                ]
            },
            {
                'title': 'Cold Water Reset',
                'duration': '1 minute',
                'description': 'Use cold water to activate the dive response and calm the nervous system.',
                'steps': [
                    'Go to the nearest sink',
                    'Run cold water over your wrists for 30 seconds',
                    'Splash cold water on your face',
                    'Hold a cold, wet towel to your neck',
                    'Take slow, deep breaths',
                    'Notice the calming effect'
                ]
            },
            {
                'title': 'Box Breathing',
                'duration': '3 minutes',
                'description': 'Structured breathing pattern used by Navy SEALs for stress management.',
                'steps': [
                    'Sit with your back straight',
                    'Exhale all air from your lungs',
                    'Inhale through nose for 4 counts',
                    'Hold breath for 4 counts',
                    'Exhale through mouth for 4 counts',
                    'Hold empty lungs for 4 counts',
                    'Repeat 4-8 cycles'
                ]
            }
        ]
    
    def get_personalized_interventions(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized interventions based on user profile."""
        try:
            suitable_interventions = []
            
            current_stress = user_profile.get('current_stress', 5)
            current_mood = user_profile.get('current_mood', 5)
            current_energy = user_profile.get('current_energy', 5)
            avg_sleep = user_profile.get('avg_sleep', 7)
            avg_exercise = user_profile.get('avg_exercise', 30)
            avg_work_hours = user_profile.get('avg_work_hours', 8)
            
            for intervention in self.interventions_db:
                score = self._calculate_intervention_score(intervention, user_profile)
                
                if score > 0.5:  # Threshold for recommendation
                    intervention_copy = intervention.copy()
                    intervention_copy['recommendation_score'] = score
                    suitable_interventions.append(intervention_copy)
            
            # Sort by recommendation score and return top interventions
            suitable_interventions.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            # Ensure we have at least one intervention from each category
            categories = ['Physical', 'Mental', 'Social', 'Lifestyle']
            balanced_interventions = []
            
            for category in categories:
                category_interventions = [i for i in suitable_interventions if i['category'] == category]
                if category_interventions:
                    balanced_interventions.append(category_interventions[0])
            
            # Add additional high-scoring interventions
            for intervention in suitable_interventions:
                if intervention not in balanced_interventions and len(balanced_interventions) < 12:
                    balanced_interventions.append(intervention)
            
            return balanced_interventions[:12]  # Return top 12 interventions
            
        except Exception as e:
            # Return default set if there's an error
            return self.interventions_db[:8]
    
    def _calculate_intervention_score(self, intervention: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """Calculate how suitable an intervention is for the user."""
        score = 0.5  # Base score
        
        current_stress = user_profile.get('current_stress', 5)
        current_mood = user_profile.get('current_mood', 5)
        current_energy = user_profile.get('current_energy', 5)
        avg_sleep = user_profile.get('avg_sleep', 7)
        avg_exercise = user_profile.get('avg_exercise', 30)
        avg_work_hours = user_profile.get('avg_work_hours', 8)
        
        conditions = intervention.get('conditions', {})
        
        # Stress level matching
        if 'stress_level' in conditions:
            if conditions['stress_level'] == 'high' and current_stress >= 7:
                score += 0.3
            elif conditions['stress_level'] == 'moderate' and 4 <= current_stress <= 6:
                score += 0.3
            elif conditions['stress_level'] == 'low' and current_stress <= 3:
                score += 0.3
            elif conditions['stress_level'] == 'any':
                score += 0.1
        
        # Energy level considerations
        if current_energy <= 3 and intervention['category'] == 'Physical' and 'walk' not in intervention['title'].lower():
            score -= 0.2  # Reduce physical interventions for very low energy
        elif current_energy >= 7 and intervention['category'] == 'Mental':
            score += 0.1  # Boost mental interventions for high energy
        
        # Sleep-related interventions
        if avg_sleep < 6 and 'sleep' in intervention['title'].lower():
            score += 0.4
        
        # Exercise-related interventions
        if avg_exercise < 30 and intervention['category'] == 'Physical':
            score += 0.2
        
        # Work stress interventions
        if avg_work_hours > 9 and ('desk' in intervention['title'].lower() or 'work' in intervention['title'].lower()):
            score += 0.3
        
        # Mood-based adjustments
        if current_mood <= 4:
            if intervention['category'] == 'Social':
                score += 0.2
            if 'gratitude' in intervention['title'].lower():
                score += 0.3
        
        # Time of day considerations (simplified)
        if intervention.get('best_time') == 'Evening':
            score += 0.1  # Slight preference for evening activities
        
        return min(1.0, score)  # Cap at 1.0
    
    def get_immediate_interventions(self, stress_level: float) -> List[Dict[str, Any]]:
        """Get immediate interventions for high stress situations."""
        if stress_level >= 8:
            # Very high stress - return all immediate interventions
            return self.immediate_interventions_db
        elif stress_level >= 6:
            # High stress - return top 3
            return self.immediate_interventions_db[:3]
        else:
            # Moderate stress - return top 2
            return self.immediate_interventions_db[:2]
    
    def get_interventions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all interventions in a specific category."""
        return [i for i in self.interventions_db if i['category'] == category]
    
    def get_intervention_by_title(self, title: str) -> Dict[str, Any]:
        """Get a specific intervention by title."""
        for intervention in self.interventions_db:
            if intervention['title'] == title:
                return intervention
        return {}
    
    def suggest_daily_intervention(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest one intervention for daily practice."""
        suitable_interventions = self.get_personalized_interventions(user_profile)
        
        if not suitable_interventions:
            return self.interventions_db[0]  # Return first intervention as fallback
        
        # Prefer shorter, easier interventions for daily practice
        daily_suitable = [
            i for i in suitable_interventions 
            if i['difficulty'] == 'Beginner' and 
            ('minute' in i['duration'] and int(i['duration'].split()[0]) <= 10)
        ]
        
        if daily_suitable:
            return random.choice(daily_suitable)
        else:
            return suitable_interventions[0]
    
    def get_emergency_contacts_info(self) -> Dict[str, List[str]]:
        """Get emergency mental health contact information."""
        return {
            'US': [
                '988 - Suicide & Crisis Lifeline',
                '741741 - Crisis Text Line (Text HOME)',
                '1-800-662-4357 - SAMHSA National Helpline'
            ],
            'UK': [
                '116 123 - Samaritans',
                '85258 - SHOUT Crisis Text Line',
                '0300 123 3393 - Mind Infoline'
            ],
            'Canada': [
                '1-833-456-4566 - Talk Suicide Canada',
                '1-800-668-6868 - Kids Help Phone'
            ],
            'Australia': [
                '13 11 14 - Lifeline',
                '1300 22 4636 - Beyond Blue'
            ]
        }

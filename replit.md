# MindGuard - Mental Health Monitoring System

## Overview

MindGuard is a privacy-first mental health monitoring application built with Streamlit that helps users track their daily mental state, analyze lifestyle patterns, and receive personalized stress intervention recommendations. The system emphasizes local data storage, user privacy, and evidence-based mental health support through AI-powered predictions and educational resources.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with multi-page architecture
- **UI Design**: Therapeutic theme with calming color palette optimized for mental health contexts
- **Navigation**: Page-based structure with sidebar navigation and tab-based content organization
- **Visualization**: Plotly.js for interactive charts and data visualization
- **Styling**: Custom CSS theme focusing on accessibility and calming user experience

### Backend Architecture
- **Data Processing**: Pandas for data manipulation and analysis
- **Machine Learning**: Scikit-learn for stress prediction models (Random Forest and Gradient Boosting)
- **Storage**: Local JSON-based file storage with privacy-first approach
- **Session Management**: Streamlit session state for user context and privacy settings

### Data Architecture
- **Storage Method**: Local file-based storage using hashed user IDs for privacy
- **Data Structure**: JSON files containing time-series mental health metrics
- **Privacy Protection**: No cloud storage, encrypted local data, anonymous user options
- **Backup Strategy**: Local backup directory structure

## Key Components

### 1. Daily Check-In System (`pages/1_Daily_Check_In.py`)
- **Purpose**: Capture daily mental health metrics
- **Features**: Mood scoring, stress levels, energy tracking, lifestyle factors
- **Data Validation**: Prevents duplicate entries, allows updates
- **Privacy**: Local storage with user session management

### 2. Lifestyle Analysis Engine (`pages/2_Lifestyle_Analysis.py`)
- **Purpose**: Analyze correlations between lifestyle factors and mental health
- **Analytics**: Multi-dimensional data visualization, pattern recognition
- **Time Periods**: 7, 30, 90-day analysis windows
- **Insights**: Automated trend detection and correlation analysis

### 3. AI Stress Prediction (`pages/3_Stress_Prediction.py`)
- **ML Models**: Random Forest and Gradient Boosting for stress level prediction
- **Features**: Sleep, exercise, work hours, mood, energy levels
- **Training**: Local model training on user's historical data
- **Predictions**: 3-day and 7-day stress level forecasts

### 4. Intervention Recommendation System (`pages/4_Interventions.py`)
- **Engine**: Rule-based intervention matching based on current state
- **Categories**: Physical, mental, breathing exercises, mindfulness
- **Personalization**: Tailored recommendations based on stress/mood levels
- **Evidence-Based**: Interventions based on clinical research

### 5. Progress Tracking Dashboard (`pages/5_Progress_Tracking.py`)
- **Metrics**: Long-term trend analysis and goal tracking
- **Visualizations**: Multi-dimensional progress charts
- **Time Ranges**: 30, 60, 90-day and all-time analysis
- **Achievement System**: Progress milestones and improvement tracking

### 6. Educational Content System (`pages/6_Educational_Resources.py`)
- **Content Areas**: Mental health basics, stress management, mindfulness, coping strategies
- **Structure**: Modular content with key points and external resources
- **Crisis Resources**: Emergency contact information and crisis intervention

### 7. Privacy Management (`pages/7_Privacy_Settings.py`)
- **Features**: Data export, deletion, privacy mode toggle
- **Transparency**: Clear data usage policies and user control
- **Compliance**: GDPR-aligned privacy controls

## Data Flow

### Input Flow
1. User completes daily check-in via Streamlit form
2. Data validation and preprocessing in DataManager
3. Local storage as encrypted JSON files with hashed user IDs
4. Session state management for real-time updates

### Analysis Flow
1. DataManager retrieves historical data for specified time periods
2. ML models process features for stress prediction
3. Intervention engine analyzes current state for recommendations
4. Visualization components render interactive charts and insights

### Privacy Flow
1. All data processing occurs locally
2. User IDs are hashed for anonymization
3. No external API calls for sensitive data
4. Optional anonymous mode for complete privacy

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Visualization
- **Plotly Express & Graph Objects**: Interactive data visualization
- **Matplotlib/Seaborn**: Static plotting (if needed)

### Machine Learning
- **Scikit-learn**: ML models and preprocessing
- **Joblib**: Model serialization

### Utilities
- **Datetime**: Time-based data handling
- **JSON**: Data serialization
- **Hashlib**: Privacy-preserving user ID hashing
- **Logging**: Application monitoring and debugging

## Deployment Strategy

### Local Development
- **Environment**: Python virtual environment with requirements.txt
- **Database**: Local file system with JSON storage
- **Configuration**: Environment variables for customization

### Production Considerations
- **Platform**: Streamlit Cloud or self-hosted deployment
- **Storage**: Maintain local storage approach for privacy
- **Scalability**: Single-user focused design, horizontal scaling through user isolation
- **Security**: HTTPS enforcement, input validation, secure file handling

### Privacy Compliance
- **Data Residency**: All data remains on user's local system or chosen deployment
- **Encryption**: At-rest encryption for sensitive data
- **Anonymization**: Hashed identifiers and optional anonymous mode
- **User Control**: Complete data ownership and deletion rights

## Changelog

```
Changelog:
- July 03, 2025. Initial setup
- July 03, 2025. Added authentication system with phone number OTP verification
  * Created AuthManager class for user authentication
  * Implemented signup and login pages with Twilio SMS OTP
  * Added authentication checks to all pages
  * Added logout functionality
  * Updated main app with user welcome and logout button
- July 03, 2025. Removed authentication system per user request
  * Deleted login and signup pages (0_Login.py, 0_Signup.py)
  * Removed auth directory and related files (utils/auth.py, utils/auth_helper.py)
  * Cleaned up authentication checks from all pages
  * Updated main app to remove auth-related functionality
  * System now works without login requirements
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```
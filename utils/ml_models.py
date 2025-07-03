import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta

class StressPredictor:
    """
    Machine learning model for predicting stress levels based on lifestyle patterns.
    Uses scikit-learn for privacy-preserving local model training.
    """
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.feature_importance = {}
        self.is_trained = False
        
        self.ensure_model_directory()
        self.setup_logging()
        
        # Define feature columns for consistency
        self.base_features = [
            'sleep_hours', 'exercise_minutes', 'work_hours', 
            'caffeine_intake', 'alcohol_intake', 'meditation_minutes',
            'mood_score', 'energy_level'
        ]
    
    def ensure_model_directory(self):
        """Create model directory if it doesn't exist."""
        os.makedirs(self.model_dir, exist_ok=True)
    
    def setup_logging(self):
        """Setup logging for ML operations."""
        logging.basicConfig(
            filename=os.path.join(self.model_dir, "ml_models.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def prepare_features(self, data: pd.Series) -> np.ndarray:
        """Prepare features from a data row for prediction."""
        try:
            features = []
            
            for feature in self.base_features:
                if feature in data.index:
                    value = data[feature]
                    # Handle missing values
                    if pd.isna(value):
                        value = self.get_default_value(feature)
                    features.append(float(value))
                else:
                    features.append(self.get_default_value(feature))
            
            # Add derived features
            derived_features = self.create_derived_features(data)
            features.extend(derived_features)
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            self.logger.error(f"Error preparing features: {str(e)}")
            return np.array([]).reshape(1, -1)
    
    def get_default_value(self, feature: str) -> float:
        """Get default value for missing features."""
        defaults = {
            'sleep_hours': 7.0,
            'exercise_minutes': 0.0,
            'work_hours': 8.0,
            'caffeine_intake': 1.0,
            'alcohol_intake': 0.0,
            'meditation_minutes': 0.0,
            'mood_score': 5.0,
            'energy_level': 5.0
        }
        return defaults.get(feature, 0.0)
    
    def create_derived_features(self, data: pd.Series) -> List[float]:
        """Create derived features from basic data."""
        try:
            derived = []
            
            # Sleep quality indicator (1 if 7-9 hours, 0 otherwise)
            sleep_hours = data.get('sleep_hours', 7.0)
            derived.append(1.0 if 7 <= sleep_hours <= 9 else 0.0)
            
            # Exercise sufficiency (1 if >= 30 minutes, 0 otherwise)
            exercise_min = data.get('exercise_minutes', 0.0)
            derived.append(1.0 if exercise_min >= 30 else 0.0)
            
            # Work-life balance indicator (1 if <= 8 hours, 0 otherwise)
            work_hours = data.get('work_hours', 8.0)
            derived.append(1.0 if work_hours <= 8 else 0.0)
            
            # Caffeine dependency indicator
            caffeine = data.get('caffeine_intake', 1.0)
            derived.append(1.0 if caffeine > 3 else 0.0)
            
            # Self-care indicator (meditation > 0)
            meditation = data.get('meditation_minutes', 0.0)
            derived.append(1.0 if meditation > 0 else 0.0)
            
            # Mood-energy interaction
            mood = data.get('mood_score', 5.0)
            energy = data.get('energy_level', 5.0)
            derived.append(mood * energy / 10.0)  # Normalized interaction
            
            return derived
            
        except Exception as e:
            self.logger.error(f"Error creating derived features: {str(e)}")
            return [0.0] * 6  # Return default values
    
    def prepare_training_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from user's historical data."""
        try:
            if len(data) < 3:
                self.logger.warning("Insufficient data for training")
                return np.array([]), np.array([])
            
            # Remove rows with missing stress_level (target variable)
            clean_data = data.dropna(subset=['stress_level']).copy()
            
            if len(clean_data) < 3:
                self.logger.warning("Insufficient clean data for training")
                return np.array([]), np.array([])
            
            # Prepare features
            X = []
            y = clean_data['stress_level'].values
            
            for idx, row in clean_data.iterrows():
                features = self.prepare_features(row).flatten()
                if len(features) > 0:
                    X.append(features)
            
            X = np.array(X)
            
            # Store feature names
            self.feature_names = (
                self.base_features + 
                ['sleep_quality', 'exercise_sufficient', 'work_life_balance', 
                 'high_caffeine', 'meditation_practice', 'mood_energy_interaction']
            )
            
            return X, y
            
        except Exception as e:
            self.logger.error(f"Error preparing training data: {str(e)}")
            return np.array([]), np.array([])
    
    def train_model(self, data: pd.DataFrame) -> bool:
        """Train the stress prediction model on user data."""
        try:
            X, y = self.prepare_training_data(data)
            
            if len(X) == 0 or len(y) == 0:
                self.logger.warning("No data available for training")
                return False
            
            # Check for sufficient variance
            if np.std(y) < 0.5:
                self.logger.warning("Insufficient variance in target variable")
                return False
            
            # Initialize scaler and model
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Use ensemble model for better predictions
            if len(X) >= 10:
                # Use Random Forest for larger datasets
                self.model = RandomForestRegressor(
                    n_estimators=50,
                    max_depth=5,
                    min_samples_split=2,
                    min_samples_leaf=1,
                    random_state=42
                )
            else:
                # Use simpler model for small datasets
                self.model = GradientBoostingRegressor(
                    n_estimators=20,
                    max_depth=3,
                    learning_rate=0.1,
                    random_state=42
                )
            
            # Train the model
            self.model.fit(X_scaled, y)
            
            # Calculate feature importance
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = dict(zip(
                    self.feature_names, 
                    self.model.feature_importances_
                ))
            
            # Evaluate model if enough data for train/test split
            if len(X) >= 6:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.3, random_state=42
                )
                
                y_pred = self.model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                self.logger.info(f"Model trained successfully. MSE: {mse:.3f}, R2: {r2:.3f}")
            else:
                self.logger.info("Model trained successfully (no validation split due to small dataset)")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict_stress(self, features: np.ndarray) -> float:
        """Predict stress level from features."""
        try:
            if not self.is_trained or self.model is None or self.scaler is None:
                self.logger.warning("Model not trained yet")
                return 5.0  # Default middle value
            
            if len(features.flatten()) != len(self.feature_names):
                self.logger.warning("Feature dimension mismatch")
                return 5.0
            
            # Scale features and predict
            features_scaled = self.scaler.transform(features)
            prediction = self.model.predict(features_scaled)[0]
            
            # Ensure prediction is within valid range (1-10)
            prediction = max(1.0, min(10.0, prediction))
            
            return round(prediction, 1)
            
        except Exception as e:
            self.logger.error(f"Error predicting stress: {str(e)}")
            return 5.0
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from trained model."""
        if not self.is_trained or not self.feature_importance:
            return {}
        
        # Sort by importance
        sorted_importance = dict(sorted(
            self.feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
        
        return sorted_importance
    
    def predict_trend(self, recent_data: pd.DataFrame, days_ahead: int = 7) -> List[float]:
        """Predict stress trend for the next few days."""
        try:
            if not self.is_trained or len(recent_data) == 0:
                return [5.0] * days_ahead
            
            predictions = []
            
            # Use rolling averages of recent data to simulate future patterns
            recent_avg = recent_data.tail(min(7, len(recent_data))).mean()
            
            for day in range(days_ahead):
                # Add some realistic variation
                variation_factor = 1 + (np.random.random() - 0.5) * 0.2  # ±10% variation
                
                # Create synthetic future data point
                future_data = recent_avg.copy()
                
                # Add weekly patterns (weekends might be different)
                if (day + 1) % 7 in [0, 6]:  # Weekend
                    future_data['work_hours'] *= 0.5  # Less work
                    future_data['exercise_minutes'] *= 1.2  # More exercise
                
                # Apply variation
                for feature in self.base_features:
                    if feature in future_data.index:
                        future_data[feature] *= variation_factor
                
                # Predict
                features = self.prepare_features(future_data)
                prediction = self.predict_stress(features)
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            self.logger.error(f"Error predicting trend: {str(e)}")
            return [5.0] * days_ahead
    
    def get_stress_factors(self, data: pd.Series) -> Dict[str, str]:
        """Analyze what factors are contributing to stress."""
        try:
            factors = {}
            
            # Sleep analysis
            sleep_hours = data.get('sleep_hours', 7.0)
            if sleep_hours < 6:
                factors['sleep'] = "Severe sleep deprivation detected"
            elif sleep_hours < 7:
                factors['sleep'] = "Mild sleep deficit"
            elif sleep_hours > 9:
                factors['sleep'] = "Possible sleep quality issues"
            else:
                factors['sleep'] = "Good sleep duration"
            
            # Work-life balance
            work_hours = data.get('work_hours', 8.0)
            if work_hours > 10:
                factors['work'] = "Excessive work hours"
            elif work_hours > 8:
                factors['work'] = "Long work hours"
            else:
                factors['work'] = "Reasonable work hours"
            
            # Exercise
            exercise_min = data.get('exercise_minutes', 0.0)
            if exercise_min == 0:
                factors['exercise'] = "No physical activity"
            elif exercise_min < 30:
                factors['exercise'] = "Low physical activity"
            else:
                factors['exercise'] = "Good exercise routine"
            
            # Caffeine
            caffeine = data.get('caffeine_intake', 1.0)
            if caffeine > 4:
                factors['caffeine'] = "High caffeine consumption"
            elif caffeine > 2:
                factors['caffeine'] = "Moderate caffeine intake"
            else:
                factors['caffeine'] = "Low caffeine intake"
            
            # Self-care
            meditation = data.get('meditation_minutes', 0.0)
            if meditation > 0:
                factors['self_care'] = "Practicing mindfulness"
            else:
                factors['self_care'] = "No mindfulness practice"
            
            return factors
            
        except Exception as e:
            self.logger.error(f"Error analyzing stress factors: {str(e)}")
            return {}
    
    def save_model(self, user_id: str) -> bool:
        """Save trained model for a user."""
        try:
            if not self.is_trained:
                return False
            
            import hashlib
            hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            model_path = os.path.join(self.model_dir, f"{hashed_id}_model.joblib")
            scaler_path = os.path.join(self.model_dir, f"{hashed_id}_scaler.joblib")
            
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            
            # Save metadata
            metadata = {
                'feature_names': self.feature_names,
                'feature_importance': self.feature_importance,
                'trained_at': datetime.now().isoformat()
            }
            
            import json
            metadata_path = os.path.join(self.model_dir, f"{hashed_id}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            return False
    
    def load_model(self, user_id: str) -> bool:
        """Load saved model for a user."""
        try:
            import hashlib
            hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            model_path = os.path.join(self.model_dir, f"{hashed_id}_model.joblib")
            scaler_path = os.path.join(self.model_dir, f"{hashed_id}_scaler.joblib")
            metadata_path = os.path.join(self.model_dir, f"{hashed_id}_metadata.json")
            
            if not all(os.path.exists(p) for p in [model_path, scaler_path, metadata_path]):
                return False
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.feature_names = metadata['feature_names']
            self.feature_importance = metadata['feature_importance']
            self.is_trained = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            return False


class MoodPredictor(StressPredictor):
    """
    Specialized model for mood prediction.
    Inherits from StressPredictor with mood-specific modifications.
    """
    
    def __init__(self, model_dir: str = "models"):
        super().__init__(model_dir)
        self.target_variable = 'mood_score'
    
    def prepare_training_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for mood prediction."""
        try:
            if len(data) < 3:
                return np.array([]), np.array([])
            
            # Use mood_score as target instead of stress_level
            clean_data = data.dropna(subset=['mood_score']).copy()
            
            if len(clean_data) < 3:
                return np.array([]), np.array([])
            
            X = []
            y = clean_data['mood_score'].values
            
            for idx, row in clean_data.iterrows():
                # Modify features to exclude mood_score (since it's the target)
                modified_features = self.base_features.copy()
                if 'mood_score' in modified_features:
                    modified_features.remove('mood_score')
                
                features = []
                for feature in modified_features:
                    if feature in row.index:
                        value = row[feature]
                        if pd.isna(value):
                            value = self.get_default_value(feature)
                        features.append(float(value))
                    else:
                        features.append(self.get_default_value(feature))
                
                # Add derived features (excluding mood-energy interaction)
                derived = self.create_derived_features(row)
                features.extend(derived[:-1])  # Exclude mood-energy interaction
                
                X.append(features)
            
            return np.array(X), y
            
        except Exception as e:
            self.logger.error(f"Error preparing mood training data: {str(e)}")
            return np.array([]), np.array([])

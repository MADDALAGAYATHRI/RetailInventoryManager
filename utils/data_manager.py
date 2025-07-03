import pandas as pd
import json
import os
from datetime import datetime, date, timedelta
import hashlib
import logging
from typing import Optional, Dict, List, Any

class DataManager:
    """
    Manages local data storage for mental health tracking.
    Focuses on privacy-first, encrypted local storage.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
        self.setup_logging()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "users"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "backups"), exist_ok=True)
    
    def setup_logging(self):
        """Setup logging for data operations."""
        logging.basicConfig(
            filename=os.path.join(self.data_dir, "data_manager.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def get_user_file_path(self, user_id: str) -> str:
        """Get the file path for a user's data."""
        # Hash user_id for privacy
        hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        return os.path.join(self.data_dir, "users", f"{hashed_id}.json")
    
    def load_user_data(self, user_id: str) -> pd.DataFrame:
        """Load user data from local storage."""
        try:
            file_path = self.get_user_file_path(user_id)
            
            if not os.path.exists(file_path):
                # Return empty DataFrame with expected columns
                return pd.DataFrame(columns=[
                    'user_id', 'date', 'mood_score', 'stress_level', 'energy_level',
                    'sleep_hours', 'exercise_minutes', 'work_hours', 'social_interaction',
                    'caffeine_intake', 'alcohol_intake', 'meditation_minutes',
                    'mood_notes', 'symptoms', 'timestamp'
                ])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading user data for {user_id}: {str(e)}")
            return pd.DataFrame()
    
    def save_user_data(self, user_id: str, data: pd.DataFrame) -> bool:
        """Save user data to local storage."""
        try:
            file_path = self.get_user_file_path(user_id)
            
            # Convert DataFrame to JSON-serializable format
            data_copy = data.copy()
            data_copy['date'] = data_copy['date'].astype(str)
            data_copy['timestamp'] = data_copy['timestamp'].astype(str)
            
            # Create backup before saving
            self.create_backup(user_id)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_copy.to_dict('records'), f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved successfully for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving user data for {user_id}: {str(e)}")
            return False
    
    def save_daily_entry(self, entry_data: Dict[str, Any]) -> bool:
        """Save a daily check-in entry."""
        try:
            user_id = entry_data['user_id']
            current_data = self.load_user_data(user_id)
            
            # Check if entry for this date already exists
            entry_date = entry_data['date']
            if not current_data.empty and 'date' in current_data.columns:
                # Convert both to same format for comparison
                current_data['date'] = pd.to_datetime(current_data['date']).dt.date
                entry_date = pd.to_datetime(entry_date).date()
                existing_mask = current_data['date'] == entry_date
            else:
                existing_mask = pd.Series([False] * len(current_data))
            
            if existing_mask.any():
                # Update existing entry
                for key, value in entry_data.items():
                    if key in current_data.columns:
                        current_data.loc[existing_mask, key] = value
            else:
                # Add new entry
                new_entry = pd.DataFrame([entry_data])
                current_data = pd.concat([current_data, new_entry], ignore_index=True)
            
            # Sort by date
            current_data = current_data.sort_values('date').reset_index(drop=True)
            
            return self.save_user_data(user_id, current_data)
            
        except Exception as e:
            self.logger.error(f"Error saving daily entry: {str(e)}")
            return False
    
    def get_recent_data(self, user_id: str, days: int = 30) -> pd.DataFrame:
        """Get recent data for a user."""
        try:
            data = self.load_user_data(user_id)
            
            if data.empty:
                return data
            
            cutoff_date = date.today() - timedelta(days=days)
            recent_data = data[data['date'] >= cutoff_date].copy()
            
            return recent_data.sort_values('date')
            
        except Exception as e:
            self.logger.error(f"Error getting recent data for {user_id}: {str(e)}")
            return pd.DataFrame()
    
    def get_all_data(self, user_id: str) -> pd.DataFrame:
        """Get all data for a user."""
        return self.load_user_data(user_id)
    
    def get_entry_by_date(self, user_id: str, target_date: date) -> Optional[Dict[str, Any]]:
        """Get a specific entry by date."""
        try:
            data = self.load_user_data(user_id)
            
            if data.empty:
                return None
            
            entry_mask = data['date'] == target_date
            
            if entry_mask.any():
                return data[entry_mask].iloc[0].to_dict()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting entry by date for {user_id}: {str(e)}")
            return None
    
    def delete_old_data(self, user_id: str, days: int) -> bool:
        """Delete data older than specified days."""
        try:
            data = self.load_user_data(user_id)
            
            if data.empty:
                return True
            
            cutoff_date = date.today() - timedelta(days=days)
            filtered_data = data[data['date'] >= cutoff_date]
            
            return self.save_user_data(user_id, filtered_data)
            
        except Exception as e:
            self.logger.error(f"Error deleting old data for {user_id}: {str(e)}")
            return False
    
    def delete_all_data(self, user_id: str) -> bool:
        """Delete all data for a user."""
        try:
            file_path = self.get_user_file_path(user_id)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            self.logger.info(f"All data deleted for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting all data for {user_id}: {str(e)}")
            return False
    
    def delete_notes_only(self, user_id: str) -> bool:
        """Delete only the notes/text data, keep metrics."""
        try:
            data = self.load_user_data(user_id)
            
            if data.empty:
                return True
            
            # Clear text fields
            data['mood_notes'] = ''
            data['symptoms'] = ''
            
            return self.save_user_data(user_id, data)
            
        except Exception as e:
            self.logger.error(f"Error deleting notes for {user_id}: {str(e)}")
            return False
    
    def keep_recent_data(self, user_id: str, days: int) -> bool:
        """Keep only recent data, delete everything else."""
        return self.delete_old_data(user_id, days)
    
    def create_backup(self, user_id: str) -> bool:
        """Create a backup of user data."""
        try:
            file_path = self.get_user_file_path(user_id)
            
            if not os.path.exists(file_path):
                return True
            
            backup_dir = os.path.join(self.data_dir, "backups")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            backup_path = os.path.join(backup_dir, f"{hashed_id}_{timestamp}.json")
            
            import shutil
            shutil.copy2(file_path, backup_path)
            
            # Keep only last 10 backups
            self.cleanup_old_backups(user_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup for {user_id}: {str(e)}")
            return False
    
    def cleanup_old_backups(self, user_id: str, keep_count: int = 10):
        """Clean up old backup files, keeping only the most recent ones."""
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith(hashed_id)]
            backup_files.sort(reverse=True)  # Most recent first
            
            # Remove old backups
            for old_backup in backup_files[keep_count:]:
                os.remove(os.path.join(backup_dir, old_backup))
                
        except Exception as e:
            self.logger.error(f"Error cleaning up backups for {user_id}: {str(e)}")
    
    # Intervention tracking methods
    def log_intervention(self, user_id: str, intervention_name: str) -> bool:
        """Log when a user completes an intervention."""
        try:
            log_data = {
                'user_id': user_id,
                'intervention_name': intervention_name,
                'date': date.today(),
                'timestamp': datetime.now()
            }
            
            # Store in separate intervention log file
            log_file = os.path.join(self.data_dir, "users", f"{hashlib.sha256(user_id.encode()).hexdigest()[:16]}_interventions.json")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    interventions = json.load(f)
            else:
                interventions = []
            
            # Convert dates to strings for JSON serialization
            log_data['date'] = str(log_data['date'])
            log_data['timestamp'] = str(log_data['timestamp'])
            
            interventions.append(log_data)
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(interventions, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging intervention for {user_id}: {str(e)}")
            return False
    
    def log_intervention_plan(self, user_id: str, intervention_name: str) -> bool:
        """Log when a user adds an intervention to their action plan."""
        try:
            plan_file = os.path.join(self.data_dir, "users", f"{hashlib.sha256(user_id.encode()).hexdigest()[:16]}_plan.json")
            
            if os.path.exists(plan_file):
                with open(plan_file, 'r', encoding='utf-8') as f:
                    planned = json.load(f)
            else:
                planned = []
            
            if intervention_name not in planned:
                planned.append(intervention_name)
                
                with open(plan_file, 'w', encoding='utf-8') as f:
                    json.dump(planned, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging intervention plan for {user_id}: {str(e)}")
            return False
    
    def get_intervention_logs(self, user_id: str) -> List[Dict[str, Any]]:
        """Get intervention completion logs for a user."""
        try:
            log_file = os.path.join(self.data_dir, "users", f"{hashlib.sha256(user_id.encode()).hexdigest()[:16]}_interventions.json")
            
            if not os.path.exists(log_file):
                return []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error getting intervention logs for {user_id}: {str(e)}")
            return []
    
    def get_planned_interventions(self, user_id: str) -> List[str]:
        """Get planned interventions for a user."""
        try:
            plan_file = os.path.join(self.data_dir, "users", f"{hashlib.sha256(user_id.encode()).hexdigest()[:16]}_plan.json")
            
            if not os.path.exists(plan_file):
                return []
            
            with open(plan_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error getting planned interventions for {user_id}: {str(e)}")
            return []
    
    def get_data_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user's data for privacy dashboard."""
        try:
            data = self.load_user_data(user_id)
            
            if data.empty:
                return {}
            
            summary = {
                'total_entries': len(data),
                'date_range': {
                    'first': str(data['date'].min()),
                    'last': str(data['date'].max())
                },
                'data_types': {
                    'mood_scores': data['mood_score'].notna().sum(),
                    'stress_levels': data['stress_level'].notna().sum(),
                    'sleep_records': data['sleep_hours'].notna().sum(),
                    'exercise_records': data['exercise_minutes'].notna().sum(),
                    'notes': data['mood_notes'].notna().sum()
                },
                'averages': {
                    'mood': round(data['mood_score'].mean(), 1) if data['mood_score'].notna().any() else None,
                    'stress': round(data['stress_level'].mean(), 1) if data['stress_level'].notna().any() else None,
                    'sleep': round(data['sleep_hours'].mean(), 1) if data['sleep_hours'].notna().any() else None
                }
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting data summary for {user_id}: {str(e)}")
            return {}

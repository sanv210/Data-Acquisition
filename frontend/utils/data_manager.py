"""
Data Manager for storing and retrieving form data across pages
"""

class DataManager:
    """Singleton class to manage data across all pages"""
    _instance = None
    _data = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._data = {
                'analytical_condition': {},
                'attenuator_information': {}
            }
        return cls._instance
    
    def save_analytical_condition(self, data):
        """Save analytical condition page data"""
        self._data['analytical_condition'] = data
    
    def get_analytical_condition(self):
        """Get analytical condition page data"""
        return self._data.get('analytical_condition', {})
    
    def save_attenuator_information(self, data):
        """Save attenuator information page data"""
        self._data['attenuator_information'] = data
    
    def get_attenuator_information(self):
        """Get attenuator information page data"""
        return self._data.get('attenuator_information', {})
    
    def clear_all(self):
        """Clear all stored data"""
        self._data = {
            'analytical_condition': {},
            'attenuator_information': {}
        }
    
    def get_all_data(self):
        """Get all stored data"""
        return self._data.copy()

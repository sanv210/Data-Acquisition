"""
Data Manager for storing and retrieving form data across pages
"""
import requests
import json
from typing import Optional, Dict, Any, List
import os

class DataManager:
    """Singleton class to manage data across all pages and handle API communication"""
    _instance = None
    _data = {}
    
    # Backend API base URL
    API_BASE_URL = "http://localhost:8000/api"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._data = {
                'analytical_condition': {},
                'element_information': {},
                'channel_information': {},
                'attenuator_information': {}
            }
        return cls._instance
    
    # ========================================================================
    # Local Storage Methods (for in-memory caching)
    # ========================================================================
    
    def save_analytical_condition(self, data):
        """Save analytical condition page data"""
        self._data['analytical_condition'] = data
    
    def get_analytical_condition(self):
        """Get analytical condition page data"""
        return self._data.get('analytical_condition', {})
    
    def save_element_information(self, data):
        """Save element information page data"""
        self._data['element_information'] = data
    
    def get_element_information(self):
        """Get element information page data"""
        return self._data.get('element_information', {})
    
    def save_channel_information(self, data):
        """Save channel information page data"""
        self._data['channel_information'] = data
    
    def get_channel_information(self):
        """Get channel information page data"""
        return self._data.get('channel_information', {})
    
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
            'element_information': {},
            'channel_information': {},
            'attenuator_information': {}
        }
    
    def get_all_data(self):
        """Get all stored data"""
        return self._data.copy()
    
    # ========================================================================
    # API Integration Methods
    # ========================================================================
    
    def upload_analytical_condition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload analytical condition data to backend API
        
        Args:
            data: Single analytical condition record
            
        Returns:
            API response with created record including ID and timestamps
        """
        try:
            # Wrap single record in bulk format
            bulk_data = {"records": [data]}
            
            response = requests.post(
                f"{self.API_BASE_URL}/analytical-conditions/bulk",
                json=bulk_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def upload_element_information(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload element information data to backend API
        
        Args:
            data: Single element information record
            
        Returns:
            API response with created record
        """
        try:
            bulk_data = {"records": [data]}
            
            response = requests.post(
                f"{self.API_BASE_URL}/element-information/bulk",
                json=bulk_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def upload_channel_information(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload channel information data to backend API
        
        Args:
            data: Single channel information record
            
        Returns:
            API response with created record
        """
        try:
            bulk_data = {"records": [data]}
            
            response = requests.post(
                f"{self.API_BASE_URL}/channel-information/bulk",
                json=bulk_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def upload_attenuator_information(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload attenuator information data to backend API
        
        Args:
            data: Single attenuator information record
            
        Returns:
            API response with created record
        """
        try:
            bulk_data = {"records": [data]}
            
            response = requests.post(
                f"{self.API_BASE_URL}/attenuator-information/bulk",
                json=bulk_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def fetch_analytical_conditions(self, analytical_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch analytical condition records from backend API
        
        Args:
            analytical_group: Optional filter by analytical group
            
        Returns:
            List of analytical condition records
        """
        try:
            params = {}
            if analytical_group:
                params['analytical_group'] = analytical_group
            
            response = requests.get(
                f"{self.API_BASE_URL}/analytical-conditions/bulk",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('records', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def fetch_element_information(self, analytical_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch element information records from backend API"""
        try:
            params = {}
            if analytical_group:
                params['analytical_group'] = analytical_group
            
            response = requests.get(
                f"{self.API_BASE_URL}/element-information/bulk",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('records', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def fetch_channel_information(self, analytical_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch channel information records from backend API"""
        try:
            params = {}
            if analytical_group:
                params['analytical_group'] = analytical_group
            
            response = requests.get(
                f"{self.API_BASE_URL}/channel-information/bulk",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('records', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def fetch_attenuator_information(self, analytical_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch attenuator information records from backend API"""
        try:
            params = {}
            if analytical_group:
                params['analytical_group'] = analytical_group
            
            response = requests.get(
                f"{self.API_BASE_URL}/attenuator-information/bulk",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('records', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    def save_measurement_mode(self, data):
        """Save Measurement Mode data locally"""
        try:
            path = os.path.join(os.path.dirname(__file__), "../data/measurement_mode.json")
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "w") as f:
                json.dump(data, f, indent=2)

            print("Measurement Mode data saved successfully")

        except Exception as e:
            print(f"Error saving measurement mode: {e}")

    def save_recalibration_information(self, data):
        path = os.path.join(os.path.dirname(__file__), "../data/recalibration_information.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def save_100_correction(self, data):
        path = os.path.join(os.path.dirname(__file__), "../data/100_correction.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path,"w") as f:
            json.dump(data,f,indent=2)
    
    def save_standard_information(self, data):
        path=os.path.join(os.path.dirname(__file__),"../data/standard_information.json")
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as f:
            json.dump(data,f,indent=2)

    def save_display_and_printout_format(self,data):
        path=os.path.join(os.path.dirname(__file__),"../data/display_and_printout_format.json")
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as f:
            json.dump(data,f,indent=2)  
    
    def save_master_curve_information(self,data):
        path=os.path.join(os.path.dirname(__file__),"../data/master_curve_information.json")
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as f:
            json.dump(data,f,indent=2)
    def save_analytical_mode(self,data):
        path=os.path.join(os.path.dirname(__file__),"../data/analytical_mode.json")
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as f:
            json.dump(data,f,indent=2)
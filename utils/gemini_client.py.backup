"""
Gemini API Client for IT-Insight
Handles all interactions with Google Gemini API
"""

import google.generativeai as genai
from PIL import Image
import json
from typing import Dict, Any, Optional
import os

class GeminiError(Exception):
    """Custom exception for Gemini-related errors"""
    pass

class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini client
        
        Args:
            api_key: Google Gemini API key
            
        Raises:
            GeminiError: If API key is invalid or missing
        """
        if not api_key:
            raise GeminiError("API key is required")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise GeminiError(f"Failed to initialize Gemini client: {str(e)}")
    
    def analyze_hardware(
        self,
        image: Image.Image,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> Dict[str, Any]:
        """
        Analyze hardware image and extract structured information
        
        Args:
            image: PIL Image object to analyze
            temperature: Model temperature (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Dictionary containing hardware information
            
        Raises:
            GeminiError: If analysis fails
        """
        try:
            # Validate image
            if not isinstance(image, Image.Image):
                raise GeminiError("Invalid image format. Please provide a PIL Image.")
            
            # Prepare the prompt
            prompt = """
            You are an expert IT hardware analyst. Analyze the IT hardware in this image and provide the following information in a structured JSON format:

            1. Hardware Name: The specific name/model of the hardware
            2. Primary Function: What this hardware does (e.g., "Graphics Processing", "Data Storage", "Network Routing")
            3. Compatibility: What systems/interfaces it's compatible with
            4. Key Features: List of 3-5 main features as an array
            5. Recommendations: Suggestions for use, installation tips, or cautions

            Return ONLY a JSON object with these exact keys:
            {
                "Hardware Name": "",
                "Primary Function": "",
                "Compatibility": "",
                "Key Features": [],
                "Recommendations": ""
            }
            """
            
            # Generate response
            response = self.model.generate_content(
                [prompt, image],
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "top_p": 0.95,
                    "top_k": 40
                }
            )
            
            # Parse response
            if not response.text:
                raise GeminiError("Empty response from Gemini API")
            
            # Extract JSON from response
            result = self._extract_json(response.text)
            
            # Validate required fields
            required_fields = [
                "Hardware Name",
                "Primary Function",
                "Compatibility",
                "Key Features",
                "Recommendations"
            ]
            
            for field in required_fields:
                if field not in result:
                    result[field] = "N/A"
            
            # Ensure Key Features is a list
            if not isinstance(result["Key Features"], list):
                if isinstance(result["Key Features"], str):
                    # Try to parse as list if it's a string
                    try:
                        features = json.loads(result["Key Features"])
                        if isinstance(features, list):
                            result["Key Features"] = features
                        else:
                            result["Key Features"] = [result["Key Features"]]
                    except:
                        result["Key Features"] = [result["Key Features"]]
                else:
                    result["Key Features"] = ["N/A"]
            
            return result
            
        except genai.types.generation_types.BlockedPromptException:
            raise GeminiError("The prompt was blocked by Gemini's safety filters")
        except Exception as e:
            raise GeminiError(f"Analysis failed: {str(e)}")
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from response text
        
        Args:
            text: Raw response text from Gemini
            
        Returns:
            Parsed dictionary
        """
        try:
            # Try to parse the entire text as JSON
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON block in the text
            import re
            json_pattern = r'\{[^{}]*\}'
            matches = re.findall(json_pattern, text)
            
            if matches:
                for match in matches:
                    try:
                        return json.loads(match)
                    except:
                        continue
            
            # If no JSON found, return a basic structure
            return {
                "Hardware Name": "Unable to parse",
                "Primary Function": text[:200],  # Truncate if too long
                "Compatibility": "N/A",
                "Key Features": ["N/A"],
                "Recommendations": "Please try again with a clearer image"
            }
    
    def health_check(self) -> bool:
        """
        Check if the API connection is working
        
        Returns:
            True if connection is successful
        """
        try:
            # Simple test query
            response = self.model.generate_content("Respond with 'OK'")
            return "OK" in response.text
        except:
            return False

"""
Service for interacting with Google Gemini API to parse resume text.
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def test_gemini_api_key() -> bool:
    """
    Test if the Gemini API key is valid by making a simple API call.
    
    Returns:
        True if API key is valid, False otherwise
    """
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_KEY or GEMINI_API_KEY not found")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Make a simple test call
        response = model.generate_content("Say 'API key is valid' if you can read this.")
        logger.info(f"API key test successful: {response.text}")
        return True
        
    except Exception as e:
        logger.error(f"API key test failed: {str(e)}")
        return False


def parse_resume_with_gemini(text: str) -> Optional[Dict[str, Any]]:
    """
    Send resume text to Gemini API and get structured JSON response.
    
    Args:
        text: Extracted text from resume
        
    Returns:
        Dict with parsed resume data, or None if parsing fails
    """
    if not text or not text.strip():
        logger.warning("Empty text provided to Gemini")
        return None
    
    try:
        import google.generativeai as genai
        
        # Get API key from environment (check both GEMINI_KEY and GEMINI_API_KEY)
        api_key = os.getenv('GEMINI_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_KEY or GEMINI_API_KEY not found in environment variables")
            return None
        
        # Validate API key format (should start with AIza)
        if not api_key.startswith('AIza'):
            logger.warning(f"API key format looks unusual (doesn't start with 'AIza'): {api_key[:10]}...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try different model names (gemini-1.5-pro, gemini-1.5-flash, gemini-pro)
        # Start with gemini-1.5-flash as it's faster and cheaper
        model_name = 'gemini-1.5-flash'
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as e:
            logger.warning(f"Failed to use {model_name}, trying gemini-1.5-pro: {str(e)}")
            model_name = 'gemini-1.5-pro'
            try:
                model = genai.GenerativeModel(model_name)
            except Exception as e2:
                logger.warning(f"Failed to use {model_name}, trying gemini-pro: {str(e2)}")
                model_name = 'gemini-pro'
                model = genai.GenerativeModel(model_name)
        
        logger.info(f"Using Gemini model: {model_name}")
        
        # Create the prompt for structured JSON extraction
        prompt = f"""Extract the following information from this resume text and return ONLY valid JSON. 
If a section is not found, use an empty array [] or null.

Resume text:
{text}

Return a JSON object with this exact structure:
{{
    "experiences": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "start_date": "YYYY-MM-DD or null",
            "end_date": "YYYY-MM-DD or null",
            "description": "Job description",
            "achievements": "Key achievements"
        }}
    ],
    "educations": [
        {{
            "institution": "School/University Name",
            "degree": "Degree Name",
            "start_date": "YYYY-MM-DD or null",
            "end_date": "YYYY-MM-DD or null",
            "description": "Additional details"
        }}
    ],
    "skills": [
        "Skill 1",
        "Skill 2"
    ],
    "languages": [
        {{
            "language": "Language Name",
            "level": "Proficiency Level (e.g., Native, Fluent, B2, etc.)"
        }}
    ],
    "certifications": [
        {{
            "name": "Certification Name",
            "issuer": "Issuing Organization",
            "date_obtained": "YYYY-MM-DD or null"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Project description",
            "start_date": "YYYY-MM-DD or null",
            "end_date": "YYYY-MM-DD or null",
            "url": "Project URL or empty string",
            "technologies": "Technologies used",
            "role": "Role in project",
            "achievements": "Project achievements"
        }}
    ]
}}

Return ONLY the JSON object, no markdown, no code blocks, no explanations."""

        # Generate response
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        parsed_data = json.loads(response_text)
        
        logger.info("Successfully parsed resume with Gemini")
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Gemini response: {str(e)}")
        if 'response_text' in locals():
            logger.error(f"Response text: {response_text[:500]}")  # Log first 500 chars
        return None
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error calling Gemini API: {error_msg}")
        
        # Check if it's an API key error
        if 'API key' in error_msg or 'API_KEY' in error_msg or 'API_KEY_INVALID' in error_msg:
            logger.error("=" * 60)
            logger.error("GEMINI API KEY ERROR - ACTION REQUIRED")
            logger.error("=" * 60)
            logger.error("Your API key is being read but Google says it's invalid.")
            logger.error("")
            logger.error("SOLUTIONS:")
            logger.error("1. Enable Generative Language API:")
            logger.error("   - Go to: https://console.cloud.google.com/apis/library")
            logger.error("   - Search: 'Generative Language API'")
            logger.error("   - Click 'Enable'")
            logger.error("")
            logger.error("2. Check API key restrictions:")
            logger.error("   - Go to: https://console.cloud.google.com/apis/credentials")
            logger.error("   - Edit your API key")
            logger.error("   - Make sure 'Generative Language API' is allowed")
            logger.error("")
            logger.error("3. Regenerate API key:")
            logger.error("   - Go to: https://makersuite.google.com/app/apikey")
            logger.error("   - Create new key and update .env file")
            logger.error("")
            logger.error(f"Current API key (first 20 chars): {api_key[:20]}...")
            logger.error("=" * 60)
        
        return None


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse date string to datetime object.
    Handles various date formats.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        datetime object or None
    """
    if not date_str or date_str.lower() in ['null', 'none', '']:
        return None
    
    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%B %Y',  # "January 2020"
        '%b %Y',  # "Jan 2020"
        '%Y',     # Just year
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date: {date_str}")
    return None


"""
Service to populate resume-related models from Gemini parsed data.
"""
import logging
from django.db import transaction
from . import models
from .gemini_service import parse_resume_with_gemini, parse_date

logger = logging.getLogger(__name__)


def populate_resume_data(resume: models.Resume, parsed_data: dict) -> bool:
    """
    Populate all related models from parsed Gemini data.
    
    Args:
        resume: Resume instance
        parsed_data: Dictionary with parsed data from Gemini
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with transaction.atomic():
            # Populate Experiences
            if parsed_data.get('experiences'):
                for exp_data in parsed_data['experiences']:
                    models.Experience.objects.create(
                        resume=resume,
                        title=exp_data.get('title', ''),
                        company=exp_data.get('company', ''),
                        start_date=parse_date(exp_data.get('start_date')),
                        end_date=parse_date(exp_data.get('end_date')),
                        description=exp_data.get('description', ''),
                        achievements=exp_data.get('achievements', '')
                    )
                logger.info(f"Created {len(parsed_data['experiences'])} experiences")
            
            # Populate Educations
            if parsed_data.get('educations'):
                for edu_data in parsed_data['educations']:
                    models.Education.objects.create(
                        resume=resume,
                        institution=edu_data.get('institution', ''),
                        degree=edu_data.get('degree', ''),
                        start_date=parse_date(edu_data.get('start_date')),
                        end_date=parse_date(edu_data.get('end_date')),
                        description=edu_data.get('description', '')
                    )
                logger.info(f"Created {len(parsed_data['educations'])} educations")
            
            # Populate Skills
            if parsed_data.get('skills'):
                for skill_name in parsed_data['skills']:
                    if skill_name and skill_name.strip():
                        models.Skill.objects.create(
                            resume=resume,
                            name=skill_name.strip()
                        )
                logger.info(f"Created {len(parsed_data['skills'])} skills")
            
            # Populate Languages
            if parsed_data.get('languages'):
                for lang_data in parsed_data['languages']:
                    models.LanguageProficiency.objects.create(
                        resume=resume,
                        language=lang_data.get('language', ''),
                        level=lang_data.get('level', '')
                    )
                logger.info(f"Created {len(parsed_data['languages'])} languages")
            
            # Populate Certifications
            if parsed_data.get('certifications'):
                for cert_data in parsed_data['certifications']:
                    models.Certification.objects.create(
                        resume=resume,
                        name=cert_data.get('name', ''),
                        issuer=cert_data.get('issuer', ''),
                        date_obtained=parse_date(cert_data.get('date_obtained'))
                    )
                logger.info(f"Created {len(parsed_data['certifications'])} certifications")
            
            # Populate Projects
            if parsed_data.get('projects'):
                for proj_data in parsed_data['projects']:
                    models.Project.objects.create(
                        resume=resume,
                        name=proj_data.get('name', ''),
                        description=proj_data.get('description', ''),
                        start_date=parse_date(proj_data.get('start_date')),
                        end_date=parse_date(proj_data.get('end_date')),
                        url=proj_data.get('url', ''),
                        technologies=proj_data.get('technologies', ''),
                        role=proj_data.get('role', ''),
                        achievements=proj_data.get('achievements', '')
                    )
                logger.info(f"Created {len(parsed_data['projects'])} projects")
            
            logger.info(f"Successfully populated all data for resume {resume.id}")
            return True
            
    except Exception as e:
        logger.error(f"Error populating resume data: {str(e)}")
        return False


def process_resume_with_gemini(resume: models.Resume) -> bool:
    """
    Complete workflow: Send text to Gemini, parse response, and populate models.
    
    Args:
        resume: Resume instance with text_extracted field populated
        
    Returns:
        True if successful, False otherwise
    """
    if not resume.text_extracted or not resume.text_extracted.strip():
        logger.warning(f"Resume {resume.id} has no extracted text, skipping Gemini processing")
        return False
    
    # Parse with Gemini
    parsed_data = parse_resume_with_gemini(resume.text_extracted)
    
    if not parsed_data:
        logger.warning(f"Failed to parse resume {resume.id} with Gemini")
        return False
    
    # Populate models
    return populate_resume_data(resume, parsed_data)


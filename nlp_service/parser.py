import re
import json

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_name(text):
    # Fallback to simple heuristic: first non-empty line could be the name
    # or look for 2-3 capitalized words
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        return lines[0] # Often the first line is the name in simple CVs
    return None

def extract_skills(text):
    # predefined list of skills for demonstration
    skill_list = ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", "Machine Learning", "NLP", "FastAPI", "Express"]
    
    extracted_skills = set()
    text_lower = text.lower()
    
    # Tokenize simply by non-alphanumeric characters
    tokens = re.split(r'\W+', text_lower)
    
    for token in tokens:
        for skill in skill_list:
            if token == skill.lower():
                extracted_skills.add(skill)
                
    # Also check full skills containing spaces
    for skill in skill_list:
        if skill.lower() in text_lower:
            extracted_skills.add(skill)
            
    return list(extracted_skills)

def extract_education(text):
    # Basic keyword extraction for education
    education_keywords = ["bachelor", "master", "phd", "b.sc", "m.sc", "b.a", "m.a", "university", "college", "institute", "degree"]
    
    lines = text.split('\n')
    education_lines = []
    
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            education_lines.append(line.strip())
            
    return education_lines

def extract_experience(text):
    # Basic keyword extraction for experience
    experience_keywords = ["experience", "work", "job", "role", "developer", "engineer", "manager", "intern"]
    
    lines = text.split('\n')
    experience_lines = []
    
    for line in lines:
        if any(keyword in line.lower() for keyword in experience_keywords):
            experience_lines.append(line.strip())
            
    return experience_lines

def parse_cv(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }

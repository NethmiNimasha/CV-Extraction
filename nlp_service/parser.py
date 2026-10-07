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
    experience_headers = ["experience", "work experience", "employment", "employment history", "professional experience"]
    other_headers = ["education", "skills", "projects", "certifications", "languages", "summary", "profile", "achievements", "references"]
    
    lines = text.split('\n')
    experience_lines = []
    in_experience_section = False
    
    for line in lines:
        line_clean = line.strip().lower()
        
        # Check if this line is a section header (exact match or with colon)
        if any(header == line_clean or header + ":" == line_clean for header in experience_headers):
            in_experience_section = True
            continue
            
        # Check if we hit another section header, meaning experience section is over
        if in_experience_section and any(header == line_clean or header + ":" == line_clean for header in other_headers):
            in_experience_section = False
            break
            
        if in_experience_section and line.strip():
            experience_lines.append(line.strip())
            
    # If a structured section was found, return it
    if experience_lines:
        return experience_lines
        
    # Fallback: Look for lines with a year (e.g. 2019, 2020) and a job title keyword
    import re
    fallback_lines = []
    for line in lines:
        if re.search(r'(20\d{2}|19\d{2})', line) and any(kw in line.lower() for kw in ["developer", "engineer", "manager", "analyst", "intern", "consultant", "director", "lead"]):
            fallback_lines.append(line.strip())
            
    return fallback_lines

def parse_cv(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }

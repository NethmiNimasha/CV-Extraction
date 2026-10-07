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
    education_headers = ["education", "academic background", "academic history", "qualifications"]
    other_headers = ["experience", "work experience", "employment", "skills", "projects", "certifications", "languages", "summary", "profile", "achievements", "references"]
    
    lines = text.split('\n')
    education_lines = []
    in_education_section = False
    
    def is_contact_info(line):
        line_lower = line.lower()
        # Ignore emails
        if "@" in line and "." in line:
            return True
        # Ignore phone numbers (heuristics: 8+ digits with spaces/dashes)
        import re
        if re.search(r'[\+\(]?[0-9][0-9 .\-\(\)]{7,}[0-9]', line):
            return True
        # Ignore addresses with street keywords
        address_keywords = ['street', ' st.', ' st,', 'avenue', ' ave.', ' ave,', 'road', ' rd.', ' rd,', 'boulevard', 'blvd', 'lane', ' ln.', ' ln,', 'drive', ' dr.', ' dr,', 'apartment', 'apt.', 'po box', 'p.o. box', 'suite', 'highway', 'hwy']
        if any(kw in line_lower for kw in address_keywords) and any(char.isdigit() for char in line):
            return True
            
        # Ignore lines that are very short and contain common address patterns (e.g. "City, State Zip" or "City, Country")
        # Example: "New York, NY 10001", "Colombo, Sri Lanka", "London, UK"
        # If the line is under 40 characters, contains a comma, and doesn't contain education degree keywords
        degree_kws = ['bachelor', 'master', 'phd', 'b.sc', 'm.sc', 'b.a', 'm.a', 'degree']
        if len(line.strip()) < 40 and ',' in line and not any(dk in line_lower for dk in degree_kws):
            # Check if it looks like a location (words separated by commas, maybe numbers)
            # This is aggressive but usually effective for removing random address lines like "Kandy, Central Province"
            return True
            
        return False
    
    for line in lines:
        line_clean = line.strip().lower()
        
        # Check if this line is a section header
        if any(header == line_clean or header + ":" == line_clean for header in education_headers):
            in_education_section = True
            continue
            
        # Check if we hit another section header
        if in_education_section and any(header == line_clean or header + ":" == line_clean for header in other_headers):
            in_education_section = False
            break
            
        if in_education_section and line.strip():
            if is_contact_info(line):
                continue
            education_lines.append(line.strip())
            
    # If a structured section was found, return it
    if education_lines:
        return education_lines
        
    # Fallback: Basic keyword extraction, but strictly ignore contact info
    education_keywords = ["bachelor", "master", "phd", "b.sc", "m.sc", "b.a", "m.a", "university", "college", "institute", "degree"]
    fallback_lines = []
    
    for line in lines:
        if is_contact_info(line):
            continue
        if any(keyword in line.lower() for keyword in education_keywords):
            fallback_lines.append(line.strip())
            
    return fallback_lines

def extract_experience(text):
    experience_headers = ["experience", "work experience", "employment", "employment history", "professional experience", "intern"]
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

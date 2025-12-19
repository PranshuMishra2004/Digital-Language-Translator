from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import json
import os
from werkzeug.utils import secure_filename
import pdfplumber
from PIL import Image
import pytesseract

# For Windows users: If Tesseract is not in PATH, uncomment and set the path below:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
CORS(app)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Common ATS keywords across different domains
ATS_KEYWORDS = {
    'technical': ['python', 'javascript', 'java', 'react', 'node.js', 'sql', 'git', 'docker', 
                  'aws', 'machine learning', 'data analysis', 'api', 'rest', 'agile', 'scrum'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
                   'collaboration', 'time management', 'adaptability'],
    'education': ['bachelor', 'master', 'degree', 'certification', 'diploma', 'gpa'],
    'experience': ['experience', 'years', 'internship', 'project', 'achievement', 'result']
}

# Role definitions with required skills
ROLE_SKILLS = {
    'Software Developer': {
        'skills': ['programming', 'coding', 'software', 'development', 'python', 'javascript', 'java', 'git'],
        'experience_level': 'entry'
    },
    'Data Analyst': {
        'skills': ['data', 'analysis', 'excel', 'sql', 'python', 'statistics', 'visualization'],
        'experience_level': 'entry'
    },
    'Frontend Developer': {
        'skills': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'ui', 'ux', 'frontend'],
        'experience_level': 'entry'
    },
    'Backend Developer': {
        'skills': ['backend', 'server', 'api', 'database', 'node.js', 'python', 'java', 'sql'],
        'experience_level': 'entry'
    },
    'Full Stack Developer': {
        'skills': ['frontend', 'backend', 'full stack', 'react', 'node.js', 'database', 'api'],
        'experience_level': 'entry'
    },
    'Machine Learning Engineer': {
        'skills': ['machine learning', 'ml', 'python', 'tensorflow', 'pytorch', 'data science', 'ai'],
        'experience_level': 'mid'
    },
    'DevOps Engineer': {
        'skills': ['devops', 'docker', 'kubernetes', 'ci/cd', 'aws', 'cloud', 'linux'],
        'experience_level': 'mid'
    },
    'Product Manager': {
        'skills': ['product', 'management', 'strategy', 'agile', 'scrum', 'stakeholder', 'roadmap'],
        'experience_level': 'mid'
    },
    'Business Analyst': {
        'skills': ['business', 'analysis', 'requirements', 'documentation', 'sql', 'excel'],
        'experience_level': 'entry'
    },
    'UI/UX Designer': {
        'skills': ['ui', 'ux', 'design', 'figma', 'prototyping', 'wireframe', 'user research'],
        'experience_level': 'entry'
    }
}

# Salary ranges in INR (for India, entry-level)
SALARY_RANGES = {
    'Software Developer': {'min': 300000, 'max': 600000, 'remote_usd': {'min': 30000, 'max': 50000}},
    'Data Analyst': {'min': 250000, 'max': 500000, 'remote_usd': {'min': 25000, 'max': 45000}},
    'Frontend Developer': {'min': 300000, 'max': 600000, 'remote_usd': {'min': 30000, 'max': 50000}},
    'Backend Developer': {'min': 350000, 'max': 700000, 'remote_usd': {'min': 35000, 'max': 60000}},
    'Full Stack Developer': {'min': 400000, 'max': 800000, 'remote_usd': {'min': 40000, 'max': 70000}},
    'Machine Learning Engineer': {'min': 500000, 'max': 1000000, 'remote_usd': {'min': 50000, 'max': 90000}},
    'DevOps Engineer': {'min': 400000, 'max': 800000, 'remote_usd': {'min': 40000, 'max': 70000}},
    'Product Manager': {'min': 600000, 'max': 1200000, 'remote_usd': {'min': 60000, 'max': 100000}},
    'Business Analyst': {'min': 300000, 'max': 600000, 'remote_usd': {'min': 30000, 'max': 50000}},
    'UI/UX Designer': {'min': 250000, 'max': 550000, 'remote_usd': {'min': 25000, 'max': 50000}}
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_image(file_path):
    """Extract text from image using OCR"""
    try:
        image = Image.open(file_path)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

def extract_text_from_file(file):
    """Extract text from uploaded file (PDF or image)"""
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Save file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        if file_ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif file_ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
            text = extract_text_from_image(file_path)
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
        
        return text
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

def calculate_ats_score(resume_text):
    """Calculate ATS compatibility score (0-100)"""
    score = 0
    max_score = 100
    
    # Normalize text
    text_lower = resume_text.lower()
    
    # Check for sections (40 points)
    sections = ['education', 'experience', 'skills', 'projects', 'summary', 'objective']
    found_sections = sum(1 for section in sections if section in text_lower)
    score += (found_sections / len(sections)) * 40
    
    # Check for keywords (30 points)
    all_keywords = []
    for category in ATS_KEYWORDS.values():
        all_keywords.extend(category)
    
    found_keywords = sum(1 for keyword in all_keywords if keyword in text_lower)
    keyword_score = min(found_keywords / 10, 1.0) * 30  # Normalize to max 10 keywords
    score += keyword_score
    
    # Check formatting issues (30 points)
    formatting_score = 30
    
    # Check for tables (bad for ATS)
    if '|' in resume_text or '\t' in resume_text:
        formatting_score -= 5
    
    # Check for very long bullet points (bad for ATS)
    lines = resume_text.split('\n')
    long_bullets = sum(1 for line in lines if len(line) > 150)
    if long_bullets > 3:
        formatting_score -= 5
    
    # Check for proper structure
    if len(resume_text) < 200:
        formatting_score -= 10  # Too short
    
    if len(resume_text) > 2000:
        formatting_score -= 5  # Too long
    
    score += formatting_score
    
    return max(0, min(100, int(score)))

def find_missing_keywords(resume_text):
    """Find missing important keywords"""
    text_lower = resume_text.lower()
    missing = []
    
    # Check for essential keywords
    essential_keywords = ['experience', 'education', 'skills', 'project']
    for keyword in essential_keywords:
        if keyword not in text_lower:
            missing.append(keyword)
    
    # Check for technical keywords
    found_tech = [kw for kw in ATS_KEYWORDS['technical'] if kw in text_lower]
    if len(found_tech) < 3:
        missing.extend([kw for kw in ATS_KEYWORDS['technical'][:5] if kw not in text_lower][:3])
    
    return missing[:10]  # Return top 10 missing keywords

def suggest_roles(resume_text):
    """Suggest job roles based on skills match"""
    text_lower = resume_text.lower()
    role_matches = []
    
    for role, data in ROLE_SKILLS.items():
        required_skills = data['skills']
        matched_skills = sum(1 for skill in required_skills if skill in text_lower)
        match_percentage = int((matched_skills / len(required_skills)) * 100)
        
        if match_percentage > 20:  # Only suggest if at least 20% match
            role_matches.append({
                'name': role,
                'match': min(100, match_percentage)
            })
    
    # Sort by match percentage (descending)
    role_matches.sort(key=lambda x: x['match'], reverse=True)
    return role_matches[:5]  # Return top 5 matches

def estimate_salary(role_name, is_fresher=True):
    """Estimate salary range for a role"""
    if role_name not in SALARY_RANGES:
        return "Salary data not available for this role"
    
    salary_data = SALARY_RANGES[role_name]
    min_salary = salary_data['min']
    max_salary = salary_data['max']
    
    # Adjust for fresher (reduce by 20%)
    if is_fresher:
        min_salary = int(min_salary * 0.8)
        max_salary = int(max_salary * 0.9)
    
    usd_range = salary_data['remote_usd']
    
    return f"₹{min_salary:,} - ₹{max_salary:,} INR (India) | ${usd_range['min']:,} - ${usd_range['max']:,} USD (Remote)"

def recommend_company_level(resume_text, ats_score, top_role_match):
    """Recommend company level based on resume strength"""
    text_lower = resume_text.lower()
    
    # Calculate resume strength
    strength_score = ats_score
    
    # Check for experience indicators
    experience_keywords = ['years', 'experience', 'internship', 'worked', 'developed']
    experience_count = sum(1 for kw in experience_keywords if kw in text_lower)
    strength_score += min(experience_count * 5, 20)
    
    # Check for achievements
    achievement_keywords = ['achieved', 'improved', 'increased', 'reduced', 'led', 'managed']
    achievement_count = sum(1 for kw in achievement_keywords if kw in text_lower)
    strength_score += min(achievement_count * 3, 15)
    
    # Determine company level
    if strength_score >= 80:
        return {
            'level': 'MNC',
            'justification': 'Strong resume with good ATS score, experience indicators, and achievements. Suitable for large multinational companies.'
        }
    elif strength_score >= 60:
        return {
            'level': 'Mid-size',
            'justification': 'Good resume with decent ATS score. Mid-size companies offer good growth opportunities.'
        }
    else:
        return {
            'level': 'Startup',
            'justification': 'Resume shows potential but needs improvement. Startups offer great learning opportunities and faster growth.'
        }

def analyze_skill_gaps(resume_text, top_role):
    """Identify missing skills for the top suggested role"""
    if not top_role or top_role not in ROLE_SKILLS:
        return []
    
    text_lower = resume_text.lower()
    required_skills = ROLE_SKILLS[top_role]['skills']
    missing_skills = [skill for skill in required_skills if skill not in text_lower]
    
    # Add learning path recommendations
    skill_gaps = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        skill_gaps.append({
            'skill': skill,
            'recommendation': f"Learn {skill} through online courses, projects, or certifications"
        })
    
    return skill_gaps

def improve_bullet_points(resume_text):
    """Suggest improvements for resume bullet points"""
    suggestions = []
    lines = resume_text.split('\n')
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Check for weak bullet points
        if line_stripped.startswith(('-', '•', '*')) and len(line_stripped) > 10:
            # Check if it lacks quantifiable results
            if not any(char.isdigit() for char in line_stripped):
                suggestions.append({
                    'line': line_stripped[:50] + '...' if len(line_stripped) > 50 else line_stripped,
                    'suggestion': 'Add quantifiable metrics (numbers, percentages) to make this bullet point more impactful'
                })
            
            # Check if it's too long
            if len(line_stripped) > 100:
                suggestions.append({
                    'line': line_stripped[:50] + '...' if len(line_stripped) > 50 else line_stripped,
                    'suggestion': 'Consider breaking this into multiple shorter bullet points for better readability'
                })
    
    return suggestions[:5]  # Return top 5 suggestions

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or image (PNG, JPG, JPEG, GIF, BMP)'}), 400
        
        # Extract text from file
        try:
            resume_text = extract_text_from_file(file)
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 400
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract enough text from the file. Please ensure the file contains readable text.'}), 400
        
        # Calculate ATS score
        ats_score = calculate_ats_score(resume_text)
        
        # Find missing keywords
        missing_keywords = find_missing_keywords(resume_text)
        
        # Suggest roles
        roles = suggest_roles(resume_text)
        
        # Estimate salary for top role
        salary_estimation = ""
        if roles:
            salary_estimation = estimate_salary(roles[0]['name'], is_fresher=True)
        
        # Recommend company level
        company_level_data = recommend_company_level(resume_text, ats_score, roles[0]['name'] if roles else None)
        
        # Analyze skill gaps
        skill_gaps = []
        if roles:
            skill_gaps = analyze_skill_gaps(resume_text, roles[0]['name'])
        
        # Bonus: Bullet point improvements
        bullet_improvements = improve_bullet_points(resume_text)
        
        # Prepare response
        response = {
            'ats_score': ats_score,
            'missing_keywords': missing_keywords,
            'roles': roles,
            'salary_estimation': salary_estimation,
            'company_level': company_level_data['level'],
            'company_level_justification': company_level_data['justification'],
            'skill_gaps': skill_gaps,
            'bullet_improvements': bullet_improvements,
            'extracted_text_preview': resume_text[:200] + '...' if len(resume_text) > 200 else resume_text  # Preview of extracted text
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

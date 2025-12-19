# AI Resume Reviewer

A comprehensive web application that analyzes resumes and provides detailed feedback on ATS compatibility, role suggestions, salary estimates, company recommendations, and skill gap analysis.

## Features

### 🎯 Core Features

1. **ATS Resume Checker**
   - Calculates ATS compatibility score (0-100)
   - Detects missing keywords
   - Identifies formatting issues

2. **Role Suggestion Engine**
   - Suggests best-fit job roles based on skills
   - Provides match percentage for each role

3. **Salary Estimation**
   - Estimates salary ranges for India (INR)
   - Provides remote USD salary ranges
   - Adjusted for entry-level/fresher positions

4. **Company Level Recommendation**
   - Suggests suitable company types (Startup, Mid-size, MNC)
   - Provides justification based on resume strength

5. **Skill Gap Analysis**
   - Identifies missing skills for top suggested role
   - Recommends learning paths

### ✨ Bonus Features

- Resume bullet point improvement suggestions
- Download analysis report as JSON

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python with Flask
- **Communication**: REST API with JSON
- **CORS**: Enabled for cross-origin requests

## Project Structure

```
AI Resume Reviewer/
├── app.py                 # Flask backend application
├── index.html            # Frontend HTML
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Frontend JavaScript
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Tesseract OCR (for image text extraction)
  - **Windows**: Download from [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
  - **Mac**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`

### Step 1: Install Tesseract OCR

**Windows:**
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default location: `C:\Program Files\Tesseract-OCR`)
3. Add to PATH or update `app.py` line 9 with: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Backend Server

Start the Flask server:

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Open the Frontend

1. Open `index.html` in your web browser
   - You can double-click the file, or
   - Right-click and select "Open with" → Your browser

2. Alternatively, if you have a local server, you can serve it:
   ```bash
   # Using Python's built-in server
   python -m http.server 8000
   ```
   Then open `http://localhost:8000` in your browser

## Usage

1. **Upload Resume**: Click the upload area or drag and drop your resume file (PDF or Image)
2. **Click Analyze**: Click the "Analyze Resume" button
3. **View Results**: The analysis results will appear below, including:
   - ATS compatibility score
   - Missing keywords
   - Suggested job roles with match percentages
   - Salary estimation
   - Company level recommendation
   - Skill gaps and learning recommendations
   - Resume improvement suggestions
4. **Download Report**: Click "Download Report (JSON)" to save the analysis as a JSON file

## API Endpoint

### POST /analyze

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: FormData with 'file' field containing PDF or image file

**Response:**
```json
{
  "ats_score": 75,
  "missing_keywords": ["python", "git", "agile"],
  "roles": [
    {"name": "Software Developer", "match": 85},
    {"name": "Full Stack Developer", "match": 70}
  ],
  "salary_estimation": "₹240,000 - ₹540,000 INR (India) | $30,000 - $50,000 USD (Remote)",
  "company_level": "Mid-size",
  "company_level_justification": "Good resume with decent ATS score...",
  "skill_gaps": [
    {
      "skill": "docker",
      "recommendation": "Learn docker through online courses, projects, or certifications"
    }
  ],
            "bullet_improvements": [
    {
      "line": "- Developed web application",
      "suggestion": "Add quantifiable metrics (numbers, percentages) to make this bullet point more impactful"
    }
  ],
  "extracted_text_preview": "Preview of extracted text from the uploaded file..."
}
```

## How It Works

### ATS Scoring Algorithm

- **Sections Check (40 points)**: Verifies presence of key sections (Education, Experience, Skills, Projects, Summary, Objective)
- **Keywords Check (30 points)**: Matches resume against common ATS keywords
- **Formatting Check (30 points)**: Detects formatting issues like tables, overly long bullet points, etc.

### Role Matching

- Compares resume text against predefined role skill sets
- Calculates match percentage based on skill overlap
- Returns top 5 matching roles sorted by match percentage

### Salary Estimation

- Based on role-specific salary ranges for India
- Adjusted for entry-level positions (20% reduction)
- Includes remote USD equivalents

### Company Level Recommendation

- Analyzes resume strength based on:
  - ATS score
  - Experience indicators
  - Achievement keywords
- Recommends Startup, Mid-size, or MNC accordingly

## Customization

You can customize the application by modifying:

- **Role Definitions**: Edit `ROLE_SKILLS` dictionary in `app.py`
- **Salary Ranges**: Update `SALARY_RANGES` dictionary in `app.py`
- **ATS Keywords**: Modify `ATS_KEYWORDS` dictionary in `app.py`
- **Styling**: Edit `static/style.css`
- **UI**: Modify `index.html` and `static/script.js`

## Troubleshooting

### Backend not starting
- Ensure Python 3.7+ is installed
- Check if port 5000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Make sure Tesseract OCR is installed and accessible

### OCR/Image processing errors
- Ensure Tesseract OCR is installed on your system
- On Windows, you may need to specify the Tesseract path in `app.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- For PDF processing, ensure pdfplumber is installed correctly

### CORS errors
- Make sure Flask-CORS is installed
- Check that the backend is running on port 5000
- Verify the API_URL in `static/script.js` matches your backend URL

### No results showing
- Check browser console for errors (F12)
- Verify backend is running and accessible
- Ensure resume text is at least 50 characters

## Future Enhancements

- More sophisticated NLP-based analysis
- Industry-specific role suggestions
- Resume templates and examples
- Historical analysis tracking
- Multi-language support

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or modify the application to suit your needs.

---

**Note**: This application uses rule-based and keyword matching algorithms. For production use, consider integrating more advanced NLP models or APIs.


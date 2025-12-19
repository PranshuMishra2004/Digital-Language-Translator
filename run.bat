@echo off
echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Trying alternative Python command...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Python not found. Please install Python 3.7+ from https://www.python.org/
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask server...
echo Server will run on http://localhost:5000
echo.
echo Open index.html in your browser to use the application.
echo Press Ctrl+C to stop the server.
echo.

python app.py
if errorlevel 1 (
    py app.py
)

pause


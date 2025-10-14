@echo off
echo Starting Bookstore Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run setup script
echo Running setup script...
python setup.py

REM Start the application
echo Starting FastAPI application...
echo.
echo Application will be available at:
echo - API: http://localhost:8000
echo - Docs: http://localhost:8000/docs
echo - Frontend: http://localhost:8000/index
echo.
echo Press Ctrl+C to stop the application
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

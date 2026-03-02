@echo off
echo ========================================
echo Auto Push to New Public GitHub Repository
echo ========================================
echo.

REM Check if git is available
"C:\Program Files\Git\bin\git.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is available
echo.

REM Get repository name
set /p REPO_NAME="Enter new repository name (default: quiznjoy): "
if "%REPO_NAME%"=="" set REPO_NAME=quiznjoy

echo.
echo ========================================
echo IMPORTANT: Create Repository First!
echo ========================================
echo.
echo 1. Open this URL in your browser:
echo    https://github.com/new
echo.
echo 2. Repository name: %REPO_NAME%
echo 3. Description: Django Quiz Platform - QuizNjoy
echo 4. Visibility: PUBLIC
echo 5. DO NOT initialize with README
echo 6. Click "Create repository"
echo.
pause

echo.
echo [STEP 1] Updating remote URL...
"C:\Program Files\Git\bin\git.exe" remote set-url origin https://github.com/dhruvpd77/%REPO_NAME%.git
if %errorlevel% neq 0 (
    echo [ERROR] Failed to update remote
    pause
    exit /b 1
)
echo [OK] Remote updated to: https://github.com/dhruvpd77/%REPO_NAME%.git
echo.

echo [STEP 2] Creating main branch...
"C:\Program Files\Git\bin\git.exe" checkout -b main 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Already on main or branch exists
    "C:\Program Files\Git\bin\git.exe" checkout main 2>nul
)
echo [OK] On main branch
echo.

echo [STEP 3] Pushing to GitHub...
echo.
echo NOTE: You may be prompted for credentials.
echo Username: dhruvpd77
echo Password: Use Personal Access Token (not your GitHub password)
echo.
"C:\Program Files\Git\bin\git.exe" push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Your public repository:
    echo https://github.com/dhruvpd77/%REPO_NAME%
    echo.
    echo Next: Make sure repository is set to Public
    echo Go to: https://github.com/dhruvpd77/%REPO_NAME%/settings
    echo.
) else (
    echo.
    echo ========================================
    echo Push failed!
    echo ========================================
    echo.
    echo Possible issues:
    echo 1. Repository not created yet - create it first
    echo 2. Authentication required - use Personal Access Token
    echo 3. Network issues - check internet connection
    echo.
    echo Alternative: Use manual upload via GitHub web interface
    echo.
)

pause


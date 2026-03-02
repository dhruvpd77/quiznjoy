#!/bin/bash
# Quick deployment script for PythonAnywhere
# Run this in your PythonAnywhere Bash console

echo "========================================="
echo "QuizNjoy - PythonAnywhere Deployment"
echo "========================================="
echo ""

# Get PythonAnywhere username
read -p "Enter your PythonAnywhere username: " PA_USERNAME

# Clone repository
echo ""
echo "Step 1: Cloning repository..."
cd ~
if [ -d "B4-QUIZ" ]; then
    echo "Directory exists, pulling latest changes..."
    cd B4-QUIZ
    git pull origin quiznjoyfinal
else
    git clone https://github.com/dhruvpd77/quiznjoy.git B4-QUIZ
    cd B4-QUIZ
    git checkout quiznjoyfinal
fi

# Create virtual environment
echo ""
echo "Step 2: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3.10 -m venv venv
fi
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 3: Installing dependencies..."
pip install --user -r requirements.txt

# Run migrations
echo ""
echo "Step 4: Running database migrations..."
python manage.py migrate

# Collect static files
echo ""
echo "Step 5: Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "Deployment setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Go to Web tab in PythonAnywhere dashboard"
echo "2. Configure WSGI file (see PYTHONANYWHERE_DEPLOYMENT.md)"
echo "3. Add static files mapping:"
echo "   URL: /static/"
echo "   Directory: /home/$PA_USERNAME/B4-QUIZ/staticfiles"
echo "4. Add media files mapping:"
echo "   URL: /media/"
echo "   Directory: /home/$PA_USERNAME/B4-QUIZ/media"
echo "5. Click Reload button"
echo ""
echo "Your site will be at: https://$PA_USERNAME.pythonanywhere.com"
echo ""


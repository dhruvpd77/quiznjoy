#!/bin/bash
# Script to push to a new public GitHub repository

echo "========================================="
echo "Setting up new public GitHub repository"
echo "========================================="
echo ""

# Get repository name
read -p "Enter new repository name (e.g., quiznjoy): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="quiznjoy"
    echo "Using default name: quiznjoy"
fi

echo ""
echo "Step 1: Create the repository on GitHub first!"
echo "Go to: https://github.com/new"
echo "Repository name: $REPO_NAME"
echo "Visibility: Public"
echo "DO NOT initialize with README"
echo ""
read -p "Press Enter after you've created the repository..."

# Update remote URL
echo ""
echo "Step 2: Updating remote URL..."
git remote set-url origin git@github.com:dhruvpd77/$REPO_NAME.git

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Ask which branch to push
echo ""
read -p "Push to 'main' branch? (y/n): " PUSH_MAIN

if [ "$PUSH_MAIN" = "y" ] || [ "$PUSH_MAIN" = "Y" ]; then
    # Create main branch if it doesn't exist
    if ! git show-ref --verify --quiet refs/heads/main; then
        git checkout -b main
    else
        git checkout main
    fi
    BRANCH_TO_PUSH="main"
else
    BRANCH_TO_PUSH=$CURRENT_BRANCH
fi

# Push to GitHub
echo ""
echo "Step 3: Pushing to GitHub..."
git push -u origin $BRANCH_TO_PUSH

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "SUCCESS! Repository pushed!"
    echo "========================================="
    echo ""
    echo "Your public repository:"
    echo "https://github.com/dhruvpd77/$REPO_NAME"
    echo ""
else
    echo ""
    echo "Push failed. Try manual upload via GitHub web interface."
    echo "See CREATE_NEW_REPO.md for instructions."
fi


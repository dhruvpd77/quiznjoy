# Automated Setup Instructions

I've created an automated script to help you push to a new public repository.

## 🚀 Quick Start

### Step 1: Run the Automated Script

Double-click: `auto_push_to_new_repo.bat`

OR run in Command Prompt:
```cmd
auto_push_to_new_repo.bat
```

### Step 2: Follow the Prompts

The script will:
1. Ask for repository name (default: `quiznjoy`)
2. Prompt you to create the repository on GitHub
3. Update your git remote
4. Create main branch
5. Push all your code

### Step 3: Create Repository on GitHub

When prompted, the script will open instructions. Do this:

1. **Go to**: https://github.com/new
2. **Repository name**: `quiznjoy` (or your choice)
3. **Description**: "Django Quiz Platform - QuizNjoy"
4. **Visibility**: ✅ **Public**
5. **DO NOT** check "Add a README file"
6. **DO NOT** add .gitignore or license
7. Click **"Create repository"**
8. Return to the script and press any key to continue

### Step 4: Authentication

If asked for credentials:
- **Username**: `dhruvpd77`
- **Password**: Use a **Personal Access Token**

**To create a token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "QuizNjoy Project"
4. Select scope: `repo` (full control)
5. Generate and copy the token
6. Use it as your password

### Step 5: Verify Repository is Public

After pushing:
1. Go to: https://github.com/dhruvpd77/quiznjoy
2. Check it shows "Public" badge
3. If "Private", go to Settings → Change visibility → Make public

---

## ✅ Success!

Your public repository will be at:
**https://github.com/dhruvpd77/quiznjoy**

---

## 🔧 Troubleshooting

### Script doesn't run?
- Make sure Git is installed
- Try running as Administrator

### Push fails?
- Make sure repository is created first
- Check internet connection
- Use Personal Access Token for password

### Still having issues?
- Use manual upload: Go to GitHub → Upload files → Drag and drop your project

---

**The script handles everything automatically! Just follow the prompts.**


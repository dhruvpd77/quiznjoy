# Push QuizNjoy to GitHub – QUINJOY-UPDATED

Your project is ready in the **first-version** branch with the database included.

## 1. Create the repository on GitHub

1. Go to [https://github.com/new](https://github.com/new)
2. **Repository name:** `QUINJOY-UPDATED`
3. Choose **Public** (or Private if you prefer)
4. **Do not** add a README, .gitignore, or license (the project already has them)
5. Click **Create repository**

## 2. Add remote and push (from project folder)

Open **PowerShell** or **Command Prompt**, then run:

```powershell
cd "c:\Users\DARSHAN SHARMA\Desktop\DHRUV-QuizWebsite\DHRUV-main"

# Replace YOUR_GITHUB_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/QUINJOY-UPDATED.git

# Push the first-version branch (and set upstream)
git push -u origin first-version
```

If you use **SSH** instead of HTTPS:

```powershell
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/QUINJOY-UPDATED.git
git push -u origin first-version
```

## 3. Optional: set first-version as default branch on GitHub

After the first push, on GitHub:

- Go to **Settings** → **General**
- Under **Default branch**, switch to **first-version** and save (so the repo opens on that branch).

---

**Included in this repo:** full project code, `db.sqlite3`, static files, templates, and migrations.  
**Branch:** `first-version`

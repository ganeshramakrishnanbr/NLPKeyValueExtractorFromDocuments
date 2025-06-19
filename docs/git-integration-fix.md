# Fix Git Integration Issues in Replit

## Current Problem
Replit has git lock files preventing command-line operations. Your repository URL needs fixing and you need proper integration.

## Solution Steps

### Step 1: Use Replit's Git Panel (Immediate Fix)
1. **Click the Source Control icon** in the left sidebar (looks like a branch symbol)
2. **Initialize Repository** if needed by clicking "Initialize Repository" 
3. **Set Remote URL**: In the git panel, click the gear icon and set:
   ```
   https://github.com/ganeshramakrishnanbr/NLPKeyValueExtractorFromDocuments.git
   ```

### Step 2: Alternative - Use Shell Tab
1. **Open new Shell tab**: Click "+" next to Console, select "Shell"
2. **Fix remote URL**:
   ```bash
   git remote set-url origin https://github.com/ganeshramakrishnanbr/NLPKeyValueExtractorFromDocuments.git
   ```
3. **Test connection**:
   ```bash
   git remote -v
   ```

### Step 3: Manual Commit Process
If automation scripts don't work due to locks:

```bash
# In Shell tab
git add .
git commit -m "Add git automation system and documentation"
git push origin main
```

### Step 4: Replit Connect to GitHub
1. **Go to Replit Account Settings**
2. **Connected Services** → **GitHub**
3. **Authorize** Replit to access your repositories
4. **Import/Connect** your existing repository

## Files Ready to Commit
- `autocommit.sh` - Full automation script
- `quick-commit.sh` - Quick commit tool  
- `setup-git-automation.sh` - Setup script
- `README.md` - Complete documentation
- `replit-git-guide.md` - Git usage guide
- `git-integration-fix.md` - This troubleshooting guide

## After Fixing Connection
Once git is working, you can use the automation:
```bash
./autocommit.sh "Initial commit with automation system"
```

## Troubleshooting
- **Lock files**: Use Replit's GUI instead of command line
- **Permission denied**: Check GitHub authentication in Replit settings
- **Wrong remote**: Use the Shell tab to fix the URL
- **Sync issues**: Use "Pull" in Replit's git panel first

The automation system is ready - we just need to establish the proper git connection first.
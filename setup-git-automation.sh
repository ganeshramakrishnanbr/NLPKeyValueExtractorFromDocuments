#!/bin/bash

# Git Automation Setup Script for NLP Key Value Extractor
# Run this once to set up all git automation features

echo "🔧 Setting up git automation for NLP Key Value Extractor..."

# Set up git aliases
echo "📝 Creating git aliases..."
git config --global alias.ac '!f() { git add . && git commit -m "$1" && git push; }; f'
git config --global alias.qc '!f() { git add . && git commit -m "$1" && git push && echo "✅ Committed: $1"; }; f'
git config --global alias.acp '!git add . && git commit -m "Auto-commit $(date)" && git push'

# Make scripts executable
chmod +x autocommit.sh
chmod +x quick-commit.sh

# Create shell aliases (add to .bashrc or .zshrc)
echo ""
echo "📋 Add these aliases to your shell profile (.bashrc or .zshrc):"
echo "alias ac='git ac'"
echo "alias qc='git qc'"
echo "alias autocommit='./autocommit.sh'"
echo "alias quick-commit='./quick-commit.sh'"

echo ""
echo "✅ Git automation setup complete!"
echo ""
echo "🚀 Available commands:"
echo "  ./autocommit.sh \"message\"     - Full auto-commit with custom message"
echo "  ./autocommit.sh               - Auto-commit with timestamp"
echo "  ./quick-commit.sh \"message\"   - Quick commit and push"
echo "  git ac \"message\"              - Git alias for quick commit"
echo "  git qc \"message\"              - Git alias with success confirmation"
echo "  git acp                       - Auto-commit with timestamp"
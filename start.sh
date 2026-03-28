#!/bin/bash
if [ ! -d "$HOME/.cache/ms-playwright" ] || [ -z "$(ls -A $HOME/.cache/ms-playwright 2>/dev/null)" ]; then
    echo "Installing Playwright browsers..."
    python -m playwright install chromium
    python -m playwright install-deps chromium
else
    echo "Playwright browsers already installed, skipping..."
fi
echo "Starting bot..."
python bot_start.py

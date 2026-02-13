"""Fix emoji encoding issues in Python files"""
import re
import os

# Emoji replacements
REPLACEMENTS = {
    '⚡': '[CALL]',
    '✅': '[OK]',
    '⚠️': '[WARN]',
    '🔄': '[RETRY]',
    '❌': '[ERROR]',
    '🔃': '[REFRESH]',
    '📈': '[CHART]',
    '💱': '[FOREX]',
    '🪙': '[CRYPTO]',
    '🎯': '[TARGET]',
    '🇮🇳': '[INDIA]',
    '📊': '[DATA]',
    '🔎': '[SEARCH]',
    '🔍': '[FIND]',
    '🔧': '[FIX]',
    '📰': '[NEWS]',
    '🚨': '[ALERT]',
    'ℹ️': '[INFO]',
}

def fix_emojis_in_file(filepath):
    """Remove emojis from a file."""
    print(f"Processing: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        for emoji, replacement in REPLACEMENTS.items():
            content = content.replace(emoji, replacement)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [FIXED] Replaced emojis in {filepath}")
            return True
        else:
            print(f"  [SKIP] No emojis found in {filepath}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to process {filepath}: {e}")
        return False

# Fix specific files
files_to_fix = [
    'app/agents/base.py',
    'app/orchestrator.py',
    'app/agents/scout.py',
]

print("="*80)
print("EMOJI REMOVER FOR WINDOWS COMPATIBILITY")
print("="*80)

fixed_count = 0
for filepath in files_to_fix:
    if os.path.exists(filepath):
        if fix_emojis_in_file(filepath):
            fixed_count += 1
    else:
        print(f"  [SKIP] File not found: {filepath}")

print(f"\n{'='*80}")
print(f"COMPLETE: Fixed {fixed_count} files")
print(f"{'='*80}")

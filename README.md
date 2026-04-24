# EPUB to Audiobook Converter

A lightweight Python script that converts EPUB e-books into chapter-by-chapter MP3 audiobooks using Microsoft Edge's free neural text-to-speech voices (via `edge-tts`).

## Features

- **Resume-friendly** — Skips already-generated chapters and can start from any chapter number
- **Smart filtering** — Ignores title pages, copyright pages, and TOC; only processes real chapters (>300 chars)
- **Mac-optimized paths** — Automatically checks iCloud Desktop first, falls back to local Desktop
- **Rate-limit safe** — Built-in 5-second pause between chapters to avoid Microsoft TTS blocks

## Requirements

```bash
pip install ebooklib beautifulsoup4 edge-tts
```

## Setup

1. Place your EPUB file on your Desktop and name it **`book.epub`**
2. Run the script:

```bash
python script.py
```

## Output

MP3 files are saved to:
```
~/Desktop/Audiobook_Chapters/
Chapter_01.mp3
Chapter_02.mp3
...
```

## Usage

### Start from Chapter 18 (default)
The script is pre-configured to start from Chapter 18:

```python
asyncio.run(resume_conversion(start_chapter=18))
```

### Start from a different chapter
Edit the last line of the script:

```python
asyncio.run(resume_conversion(start_chapter=9))
```

Or run directly in Python:

```python
import asyncio
from audiobook_converter import resume_conversion
asyncio.run(resume_conversion(start_chapter=5))
```

## How It Works

| Step | Action |
|------|--------|
| 1 | Scans `~/Desktop/book.epub` (or iCloud Desktop) |
| 2 | Extracts all HTML documents from the EPUB |
| 3 | Filters out short/non-chapter content (< 300 characters) |
| 4 | Loops from your `start_chapter` to the end |
| 5 | Skips any MP3s that already exist |
| 6 | Generates audio using `en-US-AvaMultilingualNeural` |
| 7 | Pauses 5 seconds between requests |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `book.epub not found` | Ensure the file is named exactly `book.epub` and is on your Desktop |
| Microsoft blocks requests | Increase the `asyncio.sleep(5)` value or run fewer chapters per session |
| Wrong chapter count | Some EPUBs split chapters into multiple HTML files; the 300-char filter usually handles this, but you may need to inspect `all_content` manually |
| Missing chapters in output | Check that the EPUB's chapter documents are of type `ITEM_DOCUMENT` and not images or stylesheets |

## Notes

- **Voice:** Uses `en-US-AvaMultilingualNeural`. To change voices, see [edge-tts voice list](https://github.com/rany2/edge-tts).
- **Speed:** Large chapters can take several minutes each. The script runs synchronously per chapter to respect rate limits.
- **Resume:** If the script stops mid-way, simply re-run it. It will skip completed files and continue where it left off.

## License

MIT / Personal use. `edge-tts` is an unofficial wrapper around Microsoft's Edge Read Aloud service.

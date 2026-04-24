import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import asyncio
import edge_tts
from pathlib import Path

async def resume_conversion(start_chapter=22):
    # 1. Path Setup
    desktop = Path.home() / "Desktop"
    icloud = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Desktop"
    input_path = icloud / "book.epub" if (icloud / "book.epub").exists() else desktop / "book.epub"
    output_folder = desktop / "Audiobook_Chapters"
    output_folder.mkdir(exist_ok=True)

    if not input_path.exists():
        print("❌ Error: 'book.epub' not found on your Desktop.")
        return

    # 2. Extract Chapters
    print("📖 Filtering chapters...")
    book = epub.read_epub(str(input_path))
    all_content = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text = BeautifulSoup(item.get_content(), 'html.parser').get_text().strip()
        if len(text) > 300:  # Only count actual chapters, not title pages
            all_content.append(text)

    # 3. Start Loop from Chapter 18
    start_index = start_chapter - 1  # Convert to zero-based index

    for i in range(start_index, len(all_content)):
        chapter_num = i + 1
        filename = f"Chapter_{chapter_num:02d}.mp3"
        target_path = output_folder / filename

        # Double check to see if we already have this one
        if target_path.exists():
            print(f"⏩ Skipping {filename} (exists)")
            continue

        print(f"🎙️ Narrating {filename} with Ava...")
        try:
            communicate = edge_tts.Communicate(all_content[i], "en-US-AvaMultilingualNeural")
            await communicate.save(str(target_path))
            print(f"✅ Finished {filename}")
            # Pause 5 seconds so Microsoft doesn't block you again
            await asyncio.sleep(5)
        except Exception as e:
            print(f"⚠️ Stopped at Chapter {chapter_num}: {e}")
            break

    print("🏁 Process complete!")

if __name__ == "__main__":
    asyncio.run(resume_conversion(start_chapter=18))

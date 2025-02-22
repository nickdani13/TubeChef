import os
import dotenv
import re
from datetime import datetime
from typing import List, Tuple, Dict, Optional

from composio_llamaindex import ComposioToolSet, Action
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.llms.gemini import Gemini
from googleapiclient.discovery import build

# Load environment variables from .env file
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PARENT_ID = os.getenv("NOTION_PAGE_ID")

# Initialize tools and LLM
toolset = ComposioToolSet()
tools = toolset.get_tools(actions=[
    Action.YOUTUBE_SEARCH_YOU_TUBE,
    Action.YOUTUBE_VIDEO_DETAILS,
    Action.NOTION_CREATE_NOTION_PAGE,
    Action.NOTION_ADD_PAGE_CONTENT
])

llm = Gemini(model="models/gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
loader = YoutubeTranscriptReader()

def extract_video_links(text_response: str) -> Tuple[List[str], List[str]]:
    """
    Extracts video links and titles from the given response text.
    """
    video_links, titles = [], []
    pattern = r'\*\*Title:\*\* (.*?)\n\s*\*\*Link:\*\* (https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, text_response)
    
    for title, video_url in matches:
        video_links.append(video_url)
        titles.append(title)
    
    return video_links, titles

def search_youtube_videos_api(query: str, max_results: int = 3) -> List[str]:
    """
    Searches YouTube videos using the YouTube API and returns video URLs.
    """
    youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)
    
    try:
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            relevanceLanguage="en"
        ).execute()
    except Exception as e:
        print(f"❌ YouTube API request failed: {e}")
        return []

    videos = [
        f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        for item in search_response.get("items", [])
    ]
    return videos

def get_video_transcripts(video_urls: List[str]) -> Dict[str, str]:
    """
    Fetches transcripts for the given list of YouTube video URLs.
    """
    transcripts = {}
    for url in video_urls:
        try:
            documents = loader.load_data(ytlinks=[url])
            transcript_text = ''.join(doc.text for doc in documents)
            transcripts[url] = transcript_text
        except Exception as e:
            print(f"⚠️ Failed to fetch transcript for {url}: {e}")
    return transcripts

def select_best_recipe(transcripts: Dict[str, str]) -> Optional[str]:
    """
    Analyzes the transcripts and selects the best recipe based on simplicity and clarity.
    """
    if not transcripts:
        print("❌ No transcripts available for analysis.")
        return None

    system_instruction = (
        "You are a world-class chef and expert in analyzing recipes. Given a transcript from a "
        "cooking video, your goal is to select the best recipe based on the shortest cooking time "
        "and least complexity. Once selected, generate a structured and easy-to-follow recipe, "
        "ensuring it remains concise (under 2000 characters). The recipe should include clear steps, "
        "ingredients, and cooking instructions in a logical sequence. At the end of the recipe, provide "
        "a reference to the original video."
    )
    
    combined_transcripts = "\n\n".join([f"Video: {url}\n{transcripts[url]}" for url in transcripts])
    response = llm.complete(f"{system_instruction}\n\n{combined_transcripts}")
    
    return response.text if response else None

def create_notion_page(recipe_name: str, recipe_content: str):
    """
    Creates a Notion page with the given recipe name and content.
    """
    today_date = datetime.today().strftime('%Y-%m-%d')
    notion_title = f"Dinner on {today_date}: {recipe_name}"
    page_response = toolset.execute_action(
        action=Action.NOTION_CREATE_NOTION_PAGE,
        params={"parent_id": NOTION_PARENT_ID, "title": notion_title}
    )
    page_id = page_response.get("data", {}).get("data", {}).get("id")
    if not page_id:
        print(f"❌ Failed to create Notion page. Response: {page_response}")
        return
    
    content_response = toolset.execute_action(
        action=Action.NOTION_ADD_PAGE_CONTENT,
        params={
            "parent_block_id": page_id,
            "content_block": {'content': recipe_content}
        }
    )
    
    if content_response.get("successfull") is True:
        print(f"✅ Recipe '{recipe_name}' saved in Notion!")
    else:
        print(f"❌ Failed to add content. Response: {content_response}")

def main():
    """
    Main function to search for YouTube cooking videos, extract recipes, and save to Notion.
    """
    recipe_name = input("Enter the dish you want to make: ")
    print(f"🔍 Searching for YouTube videos on '{recipe_name}'...")
    
    video_urls = search_youtube_videos_api(recipe_name)
    if not video_urls:
        print("❌ No videos found.")
        return
    
    print("📜 Extracting transcripts...")
    transcripts = get_video_transcripts(video_urls)
    
    print("🍽️ Selecting the best recipe...")
    best_recipe = select_best_recipe(transcripts)
    
    if not best_recipe:
        print("❌ No suitable recipe found.")
        return
    print("📝 Saving to Notion...")
    create_notion_page(recipe_name, best_recipe)
    print("✅ Process completed!")

if __name__ == "__main__":
    main()

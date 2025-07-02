#!/usr/bin/env python3
"""
YouTube Transcript Summarizer

A module that generates AI-powered summaries of YouTube transcripts using OpenAI's API.
Based on the implementation from youtube-summarizer project.
"""

import os
import re
import textwrap
from typing import List, Dict, Optional
from openai import OpenAI


class TranscriptSummarizer:
    """Handles transcript summarization using OpenAI's API"""
    
    def __init__(self):
        """Initialize the summarizer with OpenAI client and configuration"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '100000'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        
        # Initialize client lazily to avoid proxy conflicts during import
        if self.api_key:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client with proper error handling"""
        if self.client is not None:
            return
        
        try:
            # Simple initialization with latest OpenAI version
            self.client = OpenAI(api_key=self.api_key)
            print("OpenAI client initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def format_text_for_readability(self, text: str) -> str:
        """Format text for better readability"""
        # Split text into lines
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Handle list items
            if line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
                formatted_lines.append(line)
            # Handle headers (markdown style)
            elif line.startswith('#'):
                formatted_lines.append(line)
            # Wrap long paragraphs
            else:
                wrapped = textwrap.fill(line, width=80, 
                                      break_long_words=False, 
                                      break_on_hyphens=False)
                formatted_lines.append(wrapped)
        
        return '\n'.join(formatted_lines)
    
    def create_summary_prompt(self, transcript_content: str, chapters: Optional[List[Dict]] = None) -> str:
        """Create a detailed prompt for summarization"""
        prompt = f"""Please provide a comprehensive summary of this YouTube video transcript. Structure your response with the following sections:

## Overview
Provide a brief 2-3 sentence overview of what this video is about.

## Main Topics Covered
List the primary topics or themes discussed in the video.

## Key Takeaways & Insights
Highlight the most important points, insights, or conclusions from the video.

## Actionable Strategies
If applicable, list any practical advice, strategies, or steps mentioned.

## Specific Details & Examples
Include important specific details, examples, statistics, or case studies mentioned.

## Warnings & Common Mistakes
If the video mentions any warnings, pitfalls, or common mistakes to avoid.

## Resources & Next Steps
Any resources, tools, or next steps mentioned in the video.

Here is the transcript to summarize:

{transcript_content}
"""
        
        if chapters:
            chapter_info = "\n".join([f"- {ch.get('title', 'Chapter')} ({ch.get('time', 'Unknown time')})" for ch in chapters])
            prompt += f"\n\nChapter structure:\n{chapter_info}\n"
        
        return prompt
    
    def summarize_transcript(self, transcript: List[Dict]) -> str:
        """
        Summarize a transcript using OpenAI's API
        
        Args:
            transcript: List of transcript entries with 'text', 'time', etc.
            
        Returns:
            Formatted summary string
        """
        # Convert transcript to text
        transcript_text = "\n".join([f"[{entry.get('formatted_time', entry.get('time', '00:00'))}] {entry['text']}" 
                                   for entry in transcript])
        
        # Check if transcript is too long and truncate if needed
        # Based on error: context limit is 16,385 tokens, need to be conservative
        max_chars = 40000  # Conservative limit to stay within 16k token context window
        if len(transcript_text) > max_chars:
            transcript_text = transcript_text[:max_chars] + "\n\n[Transcript truncated due to length...]"
        
        return self.summarize_with_openai(transcript_text)
    
    def summarize_with_openai(self, transcript_content: str, chapters: Optional[List[Dict]] = None, video_id: str = None, video_info: Optional[Dict] = None) -> str:
        """Generate summary using OpenAI's chat completion API"""
        # Ensure client is initialized
        if not self.client:
            self._initialize_client()
        
        if not self.client:
            raise Exception("OpenAI API key not configured or client initialization failed")
            
        prompt = self.create_summary_prompt(transcript_content, chapters)
        
        try:
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that creates clear, comprehensive summaries of educational video transcripts. Focus on extracting key insights, actionable advice, and important details while maintaining readability."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature
            }
            
            # Only add max_tokens if it's reasonable (less than context limit)
            if self.max_tokens and self.max_tokens < 16000:
                api_params["max_tokens"] = self.max_tokens
            
            response = self.client.chat.completions.create(**api_params)
            
            summary = response.choices[0].message.content.strip()
            formatted_summary = self.format_text_for_readability(summary)
            
            # Add video info section if video_info and video_id are provided
            prefix_sections = []
            if video_info and video_id:
                video_info_section = self._create_video_info_section(video_info, video_id)
                prefix_sections.append(video_info_section)
            
            # Add clickable chapters section if chapters and video_id are provided
            if chapters and video_id:
                chapters_section = self._create_clickable_chapters_section(chapters, video_id)
                prefix_sections.append(chapters_section)
            
            if prefix_sections:
                formatted_summary = "".join(prefix_sections) + formatted_summary
            
            return formatted_summary
            
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
    
    def _create_clickable_chapters_section(self, chapters: List[Dict], video_id: str) -> str:
        """Create a clickable chapters section for the summary"""
        chapters_html = "📚 Video Chapters ({} chapters):\n\n".format(len(chapters))
        
        for chapter in chapters:
            title = chapter.get('title', 'Chapter')
            time_seconds = chapter.get('time', 0)
            
            # Format timestamp
            hours = int(time_seconds // 3600)
            minutes = int((time_seconds % 3600) // 60)
            seconds = int(time_seconds % 60)
            
            if hours > 0:
                timestamp = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                timestamp = f"{minutes}:{seconds:02d}"
            
            # Create YouTube URL with timestamp
            youtube_url = f"https://www.youtube.com/watch?v={video_id}&t={int(time_seconds)}s"
            
            # Format as clickable link (HTML will be rendered in the summary)
            chapters_html += f"• [{title}]({youtube_url}) - {timestamp}\n"
        
        return chapters_html
    
    def _create_video_info_section(self, video_info: Dict, video_id: str) -> str:
        """Create a video info section with clickable channel link"""
        info_html = ""
        
        title = video_info.get('title')
        uploader = video_info.get('uploader')
        duration = video_info.get('duration')
        
        if title:
            info_html += f"🎥 **{title}**\n\n"
        
        if uploader:
            # Create YouTube channel search URL (since we don't have direct channel URL)
            channel_search_url = f"https://www.youtube.com/results?search_query={uploader.replace(' ', '+')}"
            info_html += f"👤 Channel: [{uploader}]({channel_search_url})\n"
        
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            info_html += f"⏱️ Duration: {minutes}:{seconds:02d}\n"
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        info_html += f"🔗 [Watch on YouTube]({video_url})\n\n"
        
        return info_html
    
    def is_configured(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(self.api_key)


def format_transcript_for_display(transcript: List[Dict]) -> str:
    """Format transcript entries for display"""
    formatted_lines = []
    for entry in transcript:
        time_str = entry.get('formatted_time', f"{int(entry.get('time', 0) // 60):02d}:{int(entry.get('time', 0) % 60):02d}")
        formatted_lines.append(f"[{time_str}] {entry['text']}")
    
    return "\n".join(formatted_lines)


def format_transcript_for_readability(transcript: List[Dict], chapters: Optional[List[Dict]] = None) -> str:
    """
    Format transcript for improved readability with paragraph grouping and chapter organization
    Based on youtube-summarizer post-processing logic
    """
    if not transcript:
        return ""
    
    # Group transcript entries into sentences and paragraphs
    formatted_text = _group_transcript_into_paragraphs(transcript)
    
    # If chapters are available, organize by chapters
    if chapters:
        formatted_text = _organize_transcript_by_chapters(transcript, chapters)
    
    return formatted_text


def _group_transcript_into_paragraphs(transcript: List[Dict], sentences_per_paragraph: int = 5) -> str:
    """
    Group transcript entries into readable paragraphs
    """
    import re
    
    # Combine all transcript text
    full_text = " ".join([entry['text'] for entry in transcript])
    
    # Split into sentences using common sentence endings
    sentence_endings = r'[.!?]+(?:\s|$)'
    sentences = re.split(sentence_endings, full_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Group sentences into paragraphs
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        current_paragraph.append(sentence)
        
        # Create paragraph when we have enough sentences or reach the end
        if len(current_paragraph) >= sentences_per_paragraph or i == len(sentences) - 1:
            paragraph_text = ". ".join(current_paragraph)
            if paragraph_text and not paragraph_text.endswith('.'):
                paragraph_text += "."
            
            # Wrap lines to improve readability
            wrapped_paragraph = textwrap.fill(
                paragraph_text, 
                width=100, 
                break_long_words=False, 
                break_on_hyphens=False
            )
            paragraphs.append(wrapped_paragraph)
            current_paragraph = []
    
    return "\n\n".join(paragraphs)


def _organize_transcript_by_chapters(transcript: List[Dict], chapters: List[Dict]) -> str:
    """
    Organize transcript content by video chapters for better structure
    """
    if not chapters:
        return _group_transcript_into_paragraphs(transcript)
    
    organized_sections = []
    
    for i, chapter in enumerate(chapters):
        chapter_start = chapter.get('time', 0)
        chapter_end = chapters[i + 1].get('time', float('inf')) if i + 1 < len(chapters) else float('inf')
        
        # Filter transcript entries for this chapter
        chapter_entries = [
            entry for entry in transcript 
            if chapter_start <= entry.get('time', 0) < chapter_end
        ]
        
        if chapter_entries:
            # Format chapter header with anchor
            chapter_title = chapter.get('title', f'Chapter {i + 1}')
            chapter_time = _format_timestamp(chapter_start)
            chapter_id = f"chapter-{int(chapter_start)}"
            header = f"\n<a id='{chapter_id}'></a>## {chapter_title} [{chapter_time}]\n"
            
            # Format chapter content
            chapter_content = _group_transcript_into_paragraphs(chapter_entries, sentences_per_paragraph=4)
            
            organized_sections.append(header + chapter_content)
    
    return "\n\n".join(organized_sections)


def _format_timestamp(seconds: float) -> str:
    """Format timestamp in MM:SS or HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def extract_video_info(video_id: str) -> Dict[str, any]:
    """
    Extract video information including title and chapters using yt-dlp Python module
    Returns dict with title, chapters, and other video metadata
    """
    try:
        import yt_dlp
        import os
        print(f"yt_dlp imported successfully for video {video_id}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Add proxy configuration if available
        proxy = os.getenv('YOUTUBE_PROXY')
        if proxy:
            ydl_opts['proxy'] = f'http://{proxy}'
            print(f"Using proxy for video info extraction: {proxy}")
        else:
            print("No proxy configured for video info extraction")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(
                f'https://www.youtube.com/watch?v={video_id}', 
                download=False
            )
            
            # Extract title
            title = video_info.get('title', 'Unknown Title')
            
            # Extract chapters
            chapters = video_info.get('chapters', [])
            formatted_chapters = None
            
            if chapters:
                formatted_chapters = []
                for chapter in chapters:
                    formatted_chapters.append({
                        'title': chapter.get('title', 'Unknown Chapter'),
                        'time': chapter.get('start_time', 0)
                    })
            
            return {
                'title': title,
                'chapters': formatted_chapters,
                'duration': video_info.get('duration'),
                'uploader': video_info.get('uploader'),
                'upload_date': video_info.get('upload_date')
            }
        
    except (ImportError, Exception) as e:
        # Silently fail if yt-dlp is not available or video info extraction fails
        print(f"Video info extraction failed for video {video_id}: {e}")
        import traceback
        traceback.print_exc()
        pass
    
    return {
        'title': None,
        'chapters': None,
        'duration': None,
        'uploader': None,
        'upload_date': None
    }


def extract_video_chapters(video_id: str) -> Optional[List[Dict]]:
    """
    Extract only chapter information (for backward compatibility)
    """
    video_info = extract_video_info(video_id)
    return video_info.get('chapters')
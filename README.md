# YouTube Deep Summary

A comprehensive toolkit for downloading YouTube transcripts with multiple implementation approaches, AI-powered summarization, and persistent database storage capabilities.

## Features

### Core Functionality
- **Multiple Transcript Methods**: `youtube-transcript-api`, `yt-dlp`, and manual web scraping
- **Network Resilience**: Proxy support for cloud environments and restricted networks
- **Format Flexibility**: Accepts video IDs, full URLs, or short URLs

### Web Application
- **Clean Web Interface**: Responsive UI for viewing transcripts with mobile optimization
- **AI-Powered Summarization**: OpenAI GPT-4.1 integration with proper markdown formatting
- **Automatic Video Import**: `/watch?v=VIDEO_ID` URLs automatically import videos and redirect to SEO-friendly URLs
- **Clickable Channel Navigation**: Channel names on video pages link directly to channel overview pages
- **Channel Management**: Dedicated channel overview pages with clean handle-based routing (/@channelname)
- **Channel Overview Pages**: Comprehensive channel hubs with statistics, navigation, and recent videos
- **RESTful API**: JSON endpoints for programmatic access with auto-import capabilities
- **Real-time Processing**: AJAX-based summarization without page reloads
- **Chapter Organization**: Automatic video chapter detection and structured display
- **Dual View Modes**: Toggle between readable paragraphs and detailed timestamps
- **Video Import Settings**: Configurable import strategies and processing options via Settings page

### Advanced Features
- **Persistent Database Storage**: Supabase integration with tables for videos, transcripts, chapters, summaries, and memory snippets
- **Channel Video Import**: Import latest videos from YouTube channels with automatic transcript and AI summary generation
- **Memory Snippets**: Save and organize insights from AI summaries with formatting preservation and tagging
- **Video Metadata**: Automatic extraction of titles, thumbnails, duration, and uploader info
- **Chapter Support**: Organized transcript display by video chapters when available
- **Mobile Responsive**: Optimized interface for mobile devices with reduced padding
- **Proxy Support**: Configurable proxy settings for restricted network environments

### Summarization Features
- **Structured Summaries**: Organized sections including overview, key takeaways, and actionable strategies
- **GPT-4.1 Integration**: Latest OpenAI model with improved instruction following and context understanding
- **Proper Markdown Formatting**: Server-side conversion of markdown to HTML with bullet point processing
- **Consistent Display**: Unified formatting across video pages and channel summary pages
- **Efficient Processing**: Uses pre-formatted transcript data to avoid redundant API calls
- **Consolidated Import Logic**: Unified `process_video_complete()` function ensures consistent behavior
- **Error Handling**: Graceful fallbacks when summarization fails

## Setup

### Dependencies

Install all dependencies using the requirements file:

```bash
pip install -r requirements.txt
```

Or install individual packages:
```bash
pip install flask youtube-transcript-api openai python-dotenv yt-dlp supabase markdown google-api-python-client
```

### Environment Configuration

Create a `.env` file or set environment variables:

```bash
# Required for AI summarization
OPENAI_API_KEY=your_openai_api_key

# Required for database storage
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Required for importing channel videos (YouTube Data API v3)
YOUTUBE_API_KEY=your_youtube_api_key

# Optional OpenAI configuration
OPENAI_MODEL=gpt-4.1
OPENAI_MAX_TOKENS=100000
OPENAI_TEMPERATURE=0.7

# Optional proxy configuration
YOUTUBE_PROXY=proxy_ip:8080

# Optional Flask configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=33079
FLASK_DEBUG=True
```

### Database Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Copy your project URL and anon key to the `.env` file
3. Run the SQL commands from `sql/create_tables.sql` in your Supabase SQL editor to create the required tables

### Starting the Application

```bash
# Web application
python3 app.py

# OR using start script
./start_server.sh
```

## Development

### Modular Architecture
The application follows a clean modular design with Flask blueprints:

- **Configuration**: Centralized environment management in `src/config.py`
- **Route Organization**: Separated into logical blueprints in `src/routes/`
- **Business Logic**: Core functionality in dedicated modules (`src/video_processing.py`, `src/youtube_api.py`, etc.)
- **Utilities**: Helper functions in `src/utils/`
- **Database**: Single source of truth with `src/database_storage.py`

### Adding New Features
1. **New Routes**: Add to appropriate blueprint in `src/routes/`
2. **New Business Logic**: Create new modules in `src/` or extend existing ones
3. **New Utilities**: Add helper functions to `src/utils/helpers.py`
4. **Configuration**: Add environment variables to `src/config.py`

### Testing
```bash
# Test module imports
python3 -c "from app import create_app; app = create_app(); print('✓ App created successfully')"

# Test specific modules
python3 -c "from src.video_processing import video_processor; print('✓ Video processor available')"
python3 -c "from src.youtube_api import youtube_api; print('✓ YouTube API available')"
```

## Usage

### Command Line Scripts

```bash
# Main implementation with proxy support
python3 tools/download_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" [proxy_ip]

# yt-dlp alternative
python3 tools/simple_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Manual web scraping fallback
python3 tools/download_transcript_manual.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Web Interface

- **Home**: `http://localhost:33079/`
- **Transcript**: `http://localhost:33079/watch?v=VIDEO_ID` *(auto-imports and redirects to SEO-friendly URL)*
- **SEO-Friendly Video**: `http://localhost:33079/@channelhandle/video-title-slug`
- **Memory Snippets**: `http://localhost:33079/memory-snippets`
- **Channels**: `http://localhost:33079/channels`
- **Channel Overview**: `http://localhost:33079/@channelhandle`
- **Channel Videos**: `http://localhost:33079/@channelhandle/videos`
- **Channel Summaries**: `http://localhost:33079/@channelhandle/summaries`
- **Channel Snippets**: `http://localhost:33079/@channelhandle/snippets`
- **Videos**: `http://localhost:33079/videos`

**Recent Improvements**:
- **Auto-import functionality**: `/watch?v=VIDEO_ID` now automatically imports videos if not found and redirects to clean URLs
- **Clickable channel names**: Channel names on video pages are now clickable links to channel overview pages
- **Proper summary formatting**: AI summaries display with correct markdown formatting (headers, bullet points, links)

### API Endpoints

- **Transcript JSON**: `http://localhost:33079/api/transcript/VIDEO_ID` *(auto-imports if not found)*
- **Summary with Data**: `POST http://localhost:33079/api/summary` (with transcript data in body)
- **Memory Snippets**: `GET/POST/DELETE http://localhost:33079/api/memory-snippets`
- **Channel Import**: `POST http://localhost:33079/api/@channelhandle/import`
- **Storage Stats**: `http://localhost:33079/api/storage/stats`

**Import Logic**: All video import operations now use the unified `process_video_complete()` function for consistent behavior across all endpoints.

### Examples

```bash
# Command line usage
python3 download_transcript.py "https://www.youtube.com/watch?v=FjHtZnjNEBU"

# Web interface (summary generated via AJAX)
http://localhost:33079/watch?v=FjHtZnjNEBU

# API endpoints
curl http://localhost:33079/api/transcript/FjHtZnjNEBU
curl http://localhost:33079/api/storage/stats

# AJAX summary request (made automatically by web interface)
curl -X POST http://localhost:33079/api/summary \
  -H "Content-Type: application/json" \
  -d '{"video_id": "FjHtZnjNEBU", "formatted_transcript": "..."}'

# Memory snippets API
curl http://localhost:33079/api/memory-snippets
curl -X POST http://localhost:33079/api/memory-snippets \
  -H "Content-Type: application/json" \
  -d '{"video_id": "FjHtZnjNEBU", "snippet_text": "Important insight", "tags": ["key-point"]}'

# Channel video import API
curl -X POST http://localhost:33079/api/@techchannel/import \
  -H "Content-Type: application/json" \
  -d '{"max_results": 5}'
```

### Supported Input Formats

- Video ID: `FjHtZnjNEBU`
- Full URL: `https://www.youtube.com/watch?v=FjHtZnjNEBU`
- Short URL: `https://youtu.be/FjHtZnjNEBU`

## Project Structure

### Command-Line Tools (`/tools`)
- **`tools/download_transcript.py`** - Main implementation using `youtube-transcript-api` with proxy support
- **`tools/simple_transcript.py`** - Alternative using `yt-dlp` for broader compatibility  
- **`tools/download_transcript_manual.py`** - Manual web scraping fallback

### Web Application
- **`app.py`** - Main Flask application entry point with modular blueprint architecture

### Core Modules (`/src`)
The application follows a clean modular architecture with all source code organized in the `/src` directory:

#### Configuration & Infrastructure
- **`src/config.py`** - Centralized configuration management with environment variables
- **`src/database_storage.py`** - Supabase database integration for persistent storage
- **`src/legacy_file_storage.py`** - Legacy file-based storage (deprecated, replaced by database)

#### Business Logic
- **`src/transcript_summarizer.py`** - OpenAI GPT-4.1 powered summarization with chapter support
- **`src/video_processing.py`** - Complete video processing pipeline: transcript extraction, formatting, AI summarization
- **`src/youtube_api.py`** - YouTube Data API integration for channel and video information

#### Web Interface (`/src/routes`)
- **`src/routes/main.py`** - Main routes: home page, `/watch` redirects, favicon
- **`src/routes/api.py`** - RESTful API endpoints for transcript data, summaries, and video operations
- **`src/routes/channels.py`** - Channel management: overview, videos, summaries with handle-based routing
- **`src/routes/videos.py`** - Video display and transcript viewing with SEO-friendly URLs
- **`src/routes/snippets.py`** - Memory snippets management and display

#### Utilities
- **`src/utils/helpers.py`** - Utility functions: video ID extraction, markdown conversion, URL parsing

### Frontend & Assets
- **`templates/`** - HTML templates for responsive web interface
- **`static/`** - CSS, JavaScript, and static assets

### Database & SQL
- **`sql/create_tables.sql`** - Database schema for Supabase setup
- **`sql/create_memory_snippets_table.sql`** - Memory snippets table creation
- **`sql/migration_*.sql`** - Database migration scripts
- **`sql/add_*.sql`** - Column addition scripts
- **`sql/fix_*.sql`** - Database fixes and corrections

### Utility Scripts (`/scripts`)
- **`scripts/update_channel_handles.py`** - Update YouTube channel handles in database

### Testing (`/tests`)
- **`tests/test_chapters.py`** - Test script for debugging chapter extraction

### Configuration & Documentation
- **`.env`** - Environment variables (create from examples above)
- **`CLAUDE.md`** - Development guidelines and project documentation
- **`README.md`** - Project overview and setup instructions

## AI Summarization Structure

The AI summarization feature provides structured summaries with the following sections:

- **Overview** - Brief 2-3 sentence summary of the video content
- **Main Topics Covered** - Primary themes and subjects discussed
- **Key Takeaways & Insights** - Most important points and conclusions
- **Actionable Strategies** - Practical advice and implementable steps
- **Specific Details & Examples** - Important statistics, case studies, and examples
- **Warnings & Common Mistakes** - Pitfalls and errors to avoid
- **Resources & Next Steps** - Tools, links, and recommended follow-up actions

## Channel Overview Pages

The Channel Overview feature provides dedicated pages for each YouTube channel, serving as a central hub for all channel-related content.

### Features
- **Comprehensive Channel Information**: Channel name, handle (@channelname), description, and thumbnail
- **Statistics Dashboard**: Video count, AI summaries count, and memory snippets count with color-coded cards
- **Navigation Hub**: Direct links to videos, summaries, and snippets with descriptions
- **Recent Videos Grid**: Visual display of latest 6 videos with thumbnails and metadata
- **Channel Actions**: Import latest videos and visit YouTube channel directly
- **Handle-Based URLs**: Clean URLs using channel handles (e.g., `/@markrober`)
- **Breadcrumb Navigation**: Easy navigation back to channel overview from sub-pages
- **Responsive Design**: Mobile-optimized layout with proper breakpoints

### URL Structure
```
/@channelhandle              → Channel Overview (main hub)
/@channelhandle/videos       → All Videos List  
/@channelhandle/summaries    → AI Summaries
/@channelhandle/snippets     → Memory Snippets
```

### Navigation Flow
1. **Channels Page** (`/channels`) - Browse all channels
2. **Channel Overview** (`/@handle`) - Channel hub with stats and navigation
3. **Sub-pages** - Videos, summaries, or snippets with breadcrumb navigation back to overview
4. **Individual Content** - Specific videos, summaries, or snippets

### Features by Section
- **Header**: Gradient background with channel thumbnail, name, handle, and description
- **Statistics Cards**: Large numbers showing video count, summaries, and snippets
- **Navigation Cards**: Interactive cards with hover effects linking to different content types
- **Recent Videos**: Grid layout showing latest videos with thumbnails and quick access
- **Actions**: Import videos, visit YouTube channel, browse all channels

## Channel Video Import

The Channel Video Import feature allows you to automatically fetch the latest videos from any YouTube channel and process them with transcripts and AI summaries.

### Import Settings Configuration

The application provides comprehensive configuration options for video imports through the Settings page (`/settings` → Video Imports tab):

#### Basic Settings
- **Default Max Results**: Number of videos to import per channel (default: 20)
- **Default Days Back**: Time range in days to look back for videos (default: 30)
- **Max Results Limit**: Maximum videos that can be imported in one request (default: 50)
- **Import Timeout**: Timeout in seconds for import operations (default: 300)

#### Processing Options
- **Enable Auto Summary**: Automatically generate AI summaries for imported videos
- **Enable Transcript Extraction**: Extract transcripts for imported videos
- **Enable Chapter Extraction**: Extract video chapters for imported videos
- **Skip Existing Videos**: Skip videos that already exist in the database

#### Import Strategy
- **Primary Strategy**: Choose between `uploads_playlist`, `activities_api`, or `search_api`
- **Fallback Strategies**: Comma-separated list of fallback strategies to try

#### Advanced Settings
- **Batch Processing**: Process videos in batches for better performance
- **Batch Size**: Number of videos to process in each batch (default: 5)
- **Retry Failed Imports**: Retry failed video imports
- **Max Retry Attempts**: Maximum retry attempts for failed imports (default: 3)
- **Enable Progress Tracking**: Show progress updates during import operations
- **Log Import Operations**: Log detailed information about import operations

### Features
- **Automatic Discovery**: Import up to 20 latest videos from any YouTube channel
- **Smart Channel Matching**: Handles various channel URL formats and name variations
- **Complete Processing**: Each imported video gets transcript extraction and AI summary generation
- **Duplicate Prevention**: Skips videos that are already in your database
- **Progress Tracking**: Real-time feedback showing processed, skipped, and error counts
- **URL Decoding**: Properly handles URL-encoded channel names

### Usage
1. **Navigate to Channels page** at `/channels`
2. **Click "Import Latest Videos"** on any existing channel card
3. **Wait for processing** - the system will fetch and process each video
4. **View results** - notification shows how many videos were processed/skipped/errors
5. **Page refresh** - automatically updates to show new video counts

### API Usage
```bash
# Import 5 latest videos from a channel
curl -X POST http://localhost:33079/api/@techchannel/import \
  -H "Content-Type: application/json" \
  -d '{"max_results": 5}'

# Response includes detailed results
{
  "success": true,
  "channel_name": "TechChannel",
  "total_videos": 5,
  "processed": 3,
  "skipped": 2,
  "errors": 0,
  "results": [...]
}
```

### Requirements
- **YouTube Data API v3 Key**: Required for channel video discovery
- **OpenAI API Key**: Optional, for AI summary generation
- **Channel Must Exist**: The channel must have at least one video already in your database for optimal matching

## Memory Snippets

The Memory Snippets feature allows you to save and organize key insights from AI summaries and transcripts, creating a personal knowledge base.

### Features
- **Text Selection**: Select any text from AI summaries or transcripts to save as a snippet
- **Formatting Preservation**: HTML formatting (headers, bullet points, bold text, links) is preserved from AI summaries
- **Tagging System**: Add custom tags to organize and categorize snippets
- **Video Grouping**: Snippets are automatically grouped by video for better organization
- **Context Preservation**: Saves surrounding text context for better understanding
- **Search & Browse**: View all snippets organized by video with visual thumbnails

### Usage
1. **Generate an AI Summary** for any video
2. **Select text** from the summary or transcript that you want to save
3. **Click the "💾 Save as Memory Snippet" button** that appears
4. **Add optional tags** to categorize the snippet
5. **Save the snippet** to your personal knowledge base
6. **Browse snippets** at `/memory-snippets` grouped by video

### Database Structure
Memory snippets are stored in the `memory_snippets` table with:
- **snippet_text**: The selected text with preserved HTML formatting
- **context_before/after**: Surrounding text for context
- **tags**: Array of custom tags for organization
- **video_id**: Link to the source video
- **timestamps**: Creation and update times

## Performance & Storage

### Database Storage System
- **Persistent Storage**: Supabase database with five main tables (videos, transcripts, chapters, summaries, memory_snippets)
- **Automatic Relationships**: Foreign keys linking videos, transcripts, chapters, summaries, and memory snippets
- **Performance Indexes**: Optimized queries for video_id, timestamps, and memory snippet tags
- **Storage Statistics**: Monitor database performance via API endpoints
- **Memory Snippets**: Personal knowledge base with text selection, formatting preservation, and tagging

### Network Considerations
- **Cloud provider IPs** are commonly blocked by YouTube
- **Proxy support** available for restricted environments via `YOUTUBE_PROXY` env var
- **Multiple fallback methods** for different network conditions
- **Reduced API calls** through database storage and caching

### Performance Optimizations
- **AJAX summarization**: No page reloads for AI summary generation
- **Efficient transcript processing**: Uses formatted text for summarization
- **Database caching**: Persistent storage eliminates redundant API calls
- **Mobile-optimized UI**: Reduced padding and responsive design
- **Chapter organization**: Structured content display for better readability

## Deployment

### Docker Deployment

Build and run using Docker:

```bash
# Build Docker image
docker build -t youtube-deep-search .

# Run with environment variables
docker run -p 33079:33079 \
  -e OPENAI_API_KEY=your_openai_key \
  -e SUPABASE_URL=your_supabase_url \
  -e SUPABASE_KEY=your_supabase_key \
  youtube-deep-search
```

### Manual Deployment

```bash
# Clone repository
git clone <repository-url>
cd youtube-deep-search

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
# Run sql/create_tables.sql in your Supabase SQL editor

# Start application
python3 app.py
```
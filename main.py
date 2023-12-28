# main.py
import os
from reddit_video_generator.reddit_video_generator import RedditVideoGenerator
from settings import YouTubeChannelConfig, Theme

# Example Configuration for two YouTube channels
ttsvibelounge_config = YouTubeChannelConfig(
    channel_name="TTSVibeLounge",
    client_secret_file="client_secret_TTSVibeLounge.json",
    credentials_storage_file="credentials_TTSVibeLounge.storage",
    subreddit_name='askreddit+antiwork+AskMen+ChoosingBeggars+hatemyjob+NoStupidQuestions+pettyrevenge+Showerthoughts+TooAfraidToAsk+TwoXChromosomes+unpopularopinion+confessions+confession',
)

AussieBanterReddit_config = YouTubeChannelConfig(
    channel_name="Aussie Banter Reddit",
    client_secret_file="client_secret_AussieBanterReddit.json",
    credentials_storage_file="credentials_AussieBanterReddit.storage",
    subreddit_name='adelaide+askanaustralian+ausfinance+australia+brisbane+melbourne+perth+queensland+sydney+westernaustralia',
    background_video_path='aussiebanter.mp4'
)

YoutubeChannels = [ttsvibelounge_config, AussieBanterReddit_config]

def process_video_for_channel(RedditVideo):
    subreddit_name = RedditVideo.config.subreddit_name
    print(f"Processing channel : {RedditVideo.config.channel_name}")
    desired_video_count = RedditVideo.config.desired_video_count
    comment_limit = RedditVideo.config.comment_limit

    top_posts = RedditVideo.get_top_posts(limit=RedditVideo.config.post_limit)

    os.makedirs(RedditVideo.config.output_directory, exist_ok=True)

    generated_video_count = 0

    print(f"Comment limit set to: {comment_limit}")

    for i, post in enumerate(top_posts, start=1):
        if generated_video_count >= desired_video_count:
            break

        output_path = os.path.join(RedditVideo.config.output_directory, f"{post.slugified_title}.mp4")
        if os.path.exists(output_path):
            print(f"Skipping Already Exists: {post.title}")
            continue
        else:
            RedditVideo.generate_video(post)
            generated_video_count += 1

if __name__ == "__main__":
    for YoutubeChannel in YoutubeChannels:
        RedditVideo = RedditVideoGenerator(YoutubeChannel)
        process_video_for_channel(RedditVideo)

    print("Video processing complete.")

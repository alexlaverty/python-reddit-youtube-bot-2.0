# Reddit Video Generator

> This repository is still a work in progress! 

## Overview

New repository I've created to rewrite the Python Reddit Youtube Bot but this time would like to make the code tidier, optimised and more performant. The old repo is messy and a bit out of control, was getting to hard to maintain.

The Reddit Video Generator is a Python script that creates videos from Reddit posts, including selftext and top comments. It utilizes text-to-speech technology to convert text content into audio, generating an engaging video for a given Reddit post.

## Features

- Creates videos from Reddit posts with selftext and top comments.
- Utilizes text-to-speech for audio narration.
- Allows customization of video settings and speech engine.

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:alexlaverty/python-reddit-youtube-bot-2.0.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Reddit API credentials:

   Create an `auth.py` file in the project root with the following content:

   ```python
   REDDIT_AUTH = {
      'client_id': '',
      'client_secret': '',
      'user_agent': '',
      'username': '',
      'password': ''
   }
   ```

   Replace with your actual Reddit API credentials and Reddit username and password.

4. Customize settings:

   Edit the `settings.py` file to customize video, comment, and other settings according to your preferences.

5. Run the script:

   ```bash
   python main.py
   ```

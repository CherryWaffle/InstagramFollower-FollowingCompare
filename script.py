from instagrapi import Client
import time
import os
import logging

logging.basicConfig(level=logging.INFO)

def login_instagram(username, password, session_file):
    cl = Client()
    try:
        if os.path.exists(session_file):
            logging.info("Loading session from file...")
            cl.load_settings(session_file)
            cl.login(username, password)
        else:
            logging.info("Logging in for the first time...")
            cl.login(username, password)
            cl.dump_settings(session_file)
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        raise e
    return cl

def get_followers(client, target_username):
    try:
        user_id = client.user_id_from_username(target_username)
        followers = client.user_followers(user_id)
        return [follower.username for follower in followers.values()]
    except Exception as e:
        logging.error(f"An error occurred while fetching followers: {e}")
        raise e

def get_following(client, target_username):
    try:
        user_id = client.user_id_from_username(target_username)
        following = client.user_following(user_id)
        return [follow.username for follow in following.values()]
    except Exception as e:
        logging.error(f"An error occurred while fetching following: {e}")
        raise e

def save_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item}\n")
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"An error occurred while saving data to file: {e}")
        raise e

def compare_followers_and_following(followers, following):
    not_following_back = [user for user in following if user not in followers]
    return not_following_back

def main():
    # Replace these with your Instagram credentials
    username = "your_instagram_username"
    password = "your_instagram_password"
    
    # The target account to scrape followers and following from
    target_username = "target_account_username"
    
    # Session file to store login session
    session_file = f"{username}_session.json"

    try:
        client = login_instagram(username, password, session_file)
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return

    try:
        print(f"Scraping followers of {target_username}...")
        followers = get_followers(client, target_username)
        print(f"Total followers: {len(followers)}")
        save_to_file(followers, f"{target_username}_followers.txt")
        print("Followers saved to file.")
    except Exception as e:
        logging.error(f"Failed to scrape followers: {e}")
        return

    # Wait for a bit to avoid hitting Instagram's rate limits
    time.sleep(10)

    try:
        print(f"Scraping following of {target_username}...")
        following = get_following(client, target_username)
        print(f"Total following: {len(following)}")
        save_to_file(following, f"{target_username}_following.txt")
        print("Following saved to file.")
    except Exception as e:
        logging.error(f"Failed to scrape following: {e}")
        return

    # Compare followers and following to find users who are not following back
    try:
        not_following_back = compare_followers_and_following(followers, following)
        save_to_file(not_following_back, f"{target_username}_not_following_back.txt")
        print("Users not following back saved to file.")
    except Exception as e:
        logging.error(f"Failed to compare followers and following: {e}")

if __name__ == "__main__":
    main()
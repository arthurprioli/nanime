import requests

base_url = "https://api.jikan.moe/v4/"
anime_id = 1
anime_url = f"{base_url}anime/{anime_id}"

response = requests.get(anime_url)

if response.status_code == 200:
    anime_data = response.json()
    name = anime_data['data']['title']
    print(name)

    # Process the anime data as needed
else:
    print(f"Error: {response.status_code}")


anime_url_streaming = f"{base_url}anime/{anime_id}/streaming"

response = requests.get(anime_url_streaming)

if response.status_code == 200:
    anime_data = response.json()['data']
    for streaming in anime_data:
        print(streaming['name'])
    # name = anime_data['name']
    # print(name)

else:
    print(f"Error: {response.status_code}")
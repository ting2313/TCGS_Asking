import requests
import json
import string

url = 'https://graph.facebook.com/v3.2/289195411286102?fields=posts.limit(100)&access_token=EAAD9ZB7nRKsYBAPBkFeCp3QFhj41WxEjP9GEbkgZBrkvO4SzRk8ZAIlM6IDyZCj5nEcs31FKbGH8K2Y0NwAROQ7rafkfAZA1XdXzlQVf3aQZBlqyxceFQH1jIXKAI5KfJUFZBGMgAhTMhvlsPvdrMj9sZBfgf9nZB5wSjyhBlXs5ZCArhqCXnO4DMdQqiZC3OA2sAAZD'
response = requests.get(url)
html = json.loads(response.text)
count = 0
upper = 2
for i in range(len(html['posts']['data'])):
	message = html['posts']['data'][i]['message']
	if message.find('宿舍')>0:
		count = count+1
		print(message)
	if count==upper:
		break
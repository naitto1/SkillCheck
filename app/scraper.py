import requests
import json

url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"
output_json_path = "../dataset/rapid_api.json"

querystring = {"keywords":"data analyst","locationId":"92000000","datePosted":"anyTime","sort":"mostRelevant"}

headers = {
	"x-rapidapi-key": "dafbd23b61msh01359a39b982dccp1237f3jsn7a976318b834",
	"x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

with open(f"{output_json_path}", "w") as f:
	json.dump(response.json(), f, indent=4)


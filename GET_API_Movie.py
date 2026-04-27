import requests

url = "https://movie-database-alternative.p.rapidapi.com/"

querystring = {"s":"Avengers Endgame","r":"json","page":"1"}

headers = {
	"x-rapidapi-host": "movie-database-alternative.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
import requests 


MOVIE_URL = 'https://api.themoviedb.org/3/search/movie'
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZmM1N2NiMzg4NTliNWIwMjZmZDAyMWU4MGQyMDczZSIsInN1YiI6IjY1NWI0OTA1ZWE4NGM3MTA5NWEwMmFjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ludFPXgX_UARSBOuLK9_mDQzcBIUk-4R-SoJUzRNg2Q"
}

movie_to_find = 'the matrix'
response = requests.get(MOVIE_URL, headers=headers, params={"query": movie_to_find})
print(response.raise_for_status)
data = response.json()['results']
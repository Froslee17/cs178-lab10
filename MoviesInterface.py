# name: YOUR NAME HERE
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    """
    Prompt user for a Movie Title.
    Add the movie to the database with the title and an empty Ratings list.
    """
    print("creating a movie")

def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    genre = movie.get("Genre", "Unknown Genre")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genre: {genre}")


def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def update_rating():
    """
    Prompt user for a Movie Title.
    Prompt user for a rating (integer).
    Append the rating to the movie's Ratings list in the database.
    """
    print("updating rating")

def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    print("deleting movie")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()

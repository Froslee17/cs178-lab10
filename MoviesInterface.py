# name: Alex Froslee
# date: 3/5/26
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')
REGION = "us-east-1"
TABLE_NAME = "Movies"

def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def create_movie():
    title = input("Enter movie title: ")

    year_input = input("Enter movie year (optional): ")
    ratings_input = input("Enter starting rating (out of 100) (optional): ")

    movie = {
        "Title": title
    }

    if year_input:
        movie["Year"] = int(year_input)

    if ratings_input:
        movie["Ratings"] = [float(ratings_input)]
    else:
        movie["Ratings"] = []

    table.put_item(Item=movie)

    print("Movie added successfully!")

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
    title = input("What is the movie title? ")

    try:
        rating = int(input("What is the rating (integer): "))
    except ValueError:
        print("error in updating movie rating")
        return

    response = table.get_item(Key={"Title": title})

    if "Item" not in response:
        print("error in updating movie rating")
        return

    table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Ratings = list_append(Ratings, :r)",
        ExpressionAttributeValues={":r": [rating]}
    )

    print("Rating added successfully!")

def delete_movie():
    title = input("Enter movie title to delete: ")

    table.delete_item(
        Key={
            "Title": title
        }
    )

    print("Movie deleted (if it existed).")

def query_movie():
    title = input("Enter movie title: ")

    response = table.get_item(Key={"Title": title})
    movie = response.get("Item")

    if movie is None:
        print("movie not found")
        return

    ratings = movie.get("Ratings", [])

    if len(ratings) == 0:
        print("movie has no ratings")
        return

    avg = sum(ratings) / len(ratings)

    print(f"Average rating for {title}: {avg}")

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

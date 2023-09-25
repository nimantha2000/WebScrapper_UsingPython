import requests
import bs4
import datetime
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Define the path to your dataset file
dataset_file = "dataset.txt"  # Replace with the actual file path

# Define the path to the log file
log_file = "unanswered_questions.log"

# Read the dataset into a dictionary
qa_dict = {}
with open(dataset_file, "r") as file:
    lines = file.readlines()
    for line in lines:
        question, answer = line.strip().split("\t")  # Assuming questions and answers are tab-separated
        qa_dict[question.lower()] = answer  # Convert questions to lowercase for case-insensitive matching

# Function to find the answer for a given question
def find_answer_local(user_question, qa_dict):
    user_question = user_question.lower()  # Convert user's question to lowercase

    # Iterate over dataset questions and find the closest match using fuzzy string matching
    best_match = None
    best_score = -1
    for question in qa_dict:
        score = fuzz.partial_ratio(user_question, question.lower())
        if score > best_score:
            best_score = score
            best_match = question

    # If the match score is above a certain threshold, return the answer
    if best_score >= 80:  # Adjust the threshold as needed
        return qa_dict[best_match]

    return None

# Define a function to remove stopwords and return a list of keywords from a question
def extract_keywords(question):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(question.lower())
    keywords = [word for word in words if word not in stop_words]
    return keywords

# Function to find the answer by searching on the internet
def find_answer_internet(question):
    websites = [
        "https://en.wikipedia.org/wiki/Ceylon_Electricity_Board",
        "https://www.ceb.lk/"
    ]

    keywords = extract_keywords(question)

    for website in websites:
        try:
            response = requests.get(website)
            response.raise_for_status()  # Raise an exception for bad HTTP responses
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {website}: {e}")
            continue  # Continue to the next website on error

        soup = bs4.BeautifulSoup(response.content, "html.parser")

        for paragraph in soup.find_all("p"):
            paragraph_text = paragraph.text.lower()
            if all(keyword in paragraph_text for keyword in keywords):
                return paragraph.text

    return None

def find_answer_google(question):
    # Define a User-Agent header to mimic a real web browser
    headers = {
        'User-Agent': 'Your User-Agent String Here',
    }

    # Construct the search URL
    search_url = "https://www.google.com/search?q=" + "+".join(question.split())

    try:
        # Make the request with the User-Agent header
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad HTTP responses
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Google search: {e}")
        return None

    soup = bs4.BeautifulSoup(response.content, "html.parser")
      # Find and extract the first search result
    search_result = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
    if search_result:
        return search_result.text

    return None
def log_unanswered_question(question):
    with open(log_file, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - Unanswered Question: {question}\n")


def main():
    question = input("What is your question?")

    # First, try to find an answer locally
    local_answer = find_answer_local(question, qa_dict)

    # If an answer is found locally, print it
    if local_answer:
        print(local_answer)
    else:
        # If no answer is found locally, search on the internet
        internet_answer = find_answer_internet(question)

        # If an answer is found on the internet, print it
        if internet_answer:
            print(internet_answer)
        else:
            google_answer = find_answer_google(question) 
            if google_answer:
                print(google_answer)
            else:
                print("I couldn't find an answer to your question. Please contact CEB via 1987")
                log_unanswered_question(question)  # Log the unanswered question    

if __name__ == "__main__":
    
    while True:
        main()

import requests
import bs4
import datetime  # Import the datetime module

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
    return qa_dict.get(user_question)

def find_answer_internet(question):
    websites = [
        "https://en.wikipedia.org/wiki/Ccccd",
        "https://www.cecb.lk/"#,
        #"https://another-example.com"
    ]

    user_question_lower = question.lower()

    for website in websites:
        try:
            response = requests.get(website)
            response.raise_for_status()  # Raise an exception for bad HTTP responses
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {website}: {e}")
            continue  # Continue to the next website on error

        soup = bs4.BeautifulSoup(response.content, "html.parser")

        for paragraph in soup.find_all("p"):
            if user_question_lower in paragraph.text.lower():
                return paragraph.text

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
            print("I couldn't find an answer to your question.")
            log_unanswered_question(question)  # Log the unanswered question

if __name__ == "__main__":
    while True:
        main()

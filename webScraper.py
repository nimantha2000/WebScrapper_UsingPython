import requests
import bs4

# Define the path to your dataset file
dataset_file = "dataset.txt"  # Replace with the actual file path

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
    return qa_dict.get(user_question, "I don't know the answer to that question.")


def find_answer(question, website):
    response = requests.get(website)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    for paragraph in soup.find_all("p"):
        if question in paragraph.text:
            return paragraph.text

    return None

def main():
    question = input("What is your question? ")
    website = "https://en.wikipedia.org/wiki/Ceylon_Electricity_Board"


    answer = find_answer(question, website)

    if answer is not None:
        print(answer)
    elif answer is None:
        answer = find_answer_local(question , qa_dict)
        print(answer)
    else:
        print("I couldn't find an answer to your question.")



if __name__ == "__main__":
    main()

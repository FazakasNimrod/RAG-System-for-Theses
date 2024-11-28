import json
from sentence_transformers import SentenceTransformer

# Load a pre-trained Sentence Transformers model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Data for the theses
theses = [
    {
        "author": "Bacs Bernat",
        "year": 2023,
        "abstract": (
            "This thesis presents the implementation of a smart home control system. The system mainly performs home automation tasks such as temperature control, "
            "watering of plants and automatic movement of shutter, thus facilitating the user's daily life. Nowadays, IoT devices are playing an increasingly "
            "important role for people, and we can't imagine our lives without them. Since most people have an internet connection at home, building such an IoT system is easier, "
            "cheaper and more efficient because there is no need for wires to communicate between devices. The system I developed and built consists of a central computer "
            "with a touch screen display connected to it, where you can follow and intervene in the automation processes, you can see statistics about the temperature in the room, "
            "for example. Several sensors are connected to this central part via Bluetooth or MQTT communication protocols, which provide data and perform the automation tasks. "
            "In my thesis I document the design and construction of this system in detail, illustrating each part with diagrams."
        ),
        "keywords": ["IoT", "Home-automation", "Raspberry Pi", "MQTT"]
    },
    {
        "author": "Kovacs Anna",
        "year": 2022,
        "abstract": (
            "This thesis explores the development of a machine learning model for predicting stock prices. The model uses historical stock data and various technical indicators "
            "to make predictions. The goal is to provide investors with a tool that can help them make more informed decisions. The thesis covers the data collection process, "
            "feature engineering, model selection, and evaluation. The results show that the model can achieve a reasonable level of accuracy, although there are limitations "
            "due to the inherent unpredictability of the stock market."
        ),
        "keywords": ["Machine Learning", "Stock Prediction", "Data Science", "Python"]
    },
    {
        "author": "Nagy Peter",
        "year": 2021,
        "abstract": (
            "This thesis investigates the use of blockchain technology in supply chain management. The study focuses on how blockchain can enhance transparency, security, and "
            "efficiency in supply chains. The research includes a detailed analysis of existing supply chain issues and how blockchain can address these problems. A prototype "
            "blockchain-based supply chain system is developed and tested to demonstrate the potential benefits. The findings suggest that blockchain can significantly improve "
            "supply chain operations, although there are challenges related to scalability and integration with existing systems."
        ),
        "keywords": ["Blockchain", "Supply Chain", "Transparency", "Security"]
    },
    {
        "author": "Szabo Maria",
        "year": 2020,
        "abstract": (
            "This thesis examines the impact of social media on mental health. The research aims to understand how different aspects of social media usage, such as time spent online "
            "and the type of content consumed, affect mental well-being. The study involves a survey of social media users and an analysis of the collected data. The results indicate "
            "that excessive use of social media can lead to negative mental health outcomes, such as anxiety and depression. The thesis also discusses potential strategies for mitigating "
            "these effects, including digital detox and promoting positive online interactions."
        ),
        "keywords": ["Social Media", "Mental Health", "Anxiety", "Depression"]
    }
]

# Add embeddings to each thesis
for thesis in theses:
    abstract = thesis["abstract"]
    embedding = model.encode(abstract).tolist()  # Generate the embedding vector and convert to list
    thesis["embedding"] = embedding  # Add the embedding to the thesis dictionary

# Save to a JSON file
with open("theses_with_embeddings.json", "w") as json_file:
    json.dump(theses, json_file, indent=4)

print("Theses with embeddings saved to 'theses_with_embeddings.json'.")

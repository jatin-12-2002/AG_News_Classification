# AG News Classification

# Introduction

This project showcases the creation of an **end-to-end MLOps pipeline** for **AG News Classification**, a task that involves categorizing news articles into four predefined categories: **World, Sports, Business, and Sci/Tech**. The primary objective was to design a scalable, automated system for machine learning model development and deployment, ensuring high performance and real-world applicability.

We employed a robust MLOps framework that integrates state-of-the-art transformer models, including **BERT, ALBERT, SBERT, XLNet, and RoBERTa**, achieving the **highest accuracy of 94.53% with RoBERTa**. The system is complemented by a user-friendly **frontend developed using HTML, CSS, and JavaScript**, with a **backend powered by FastAPI** for real-time predictions.

To ensure reliability and scalability, we addressed server response timeouts using **Redis and Celery** for **asynchronous task handling**. Deployment was achieved using **AWS EC2, and the CI/CD pipeline was automated using CircleCI**, providing a streamlined workflow from development to production.

## Overview of the MLOps Pipeline

The **MLOps pipeline** incorporates all critical stages of machine learning development in a cohesive workflow. The process begins with **data ingestion**, where the **AG News dataset** is collected and preprocessed. This is followed by **data validation** to ensure data quality and integrity. Next, the **data transformation** stage prepares the text data through tokenization and vectorization for downstream tasks.

**Model training** leverages advanced transformer models to classify news articles into the four AG News categories, with **RoBERTa** achieving the **highest accuracy of 94.53%**. **Model evaluation** identifies the best-performing model based on metrics like **accuracy and F1 score**. Finally, the **Model deployment** stage hosts the best model for real-time inference using **AWS infrastructure**. This pipeline exemplifies the integration of machine learning best practices to solve a real-world text classification problem.

## Deployment and CI/CD Integration

The deployment of the **MLOps pipeline** was achieved using **AWS EC2**, providing a scalable and reliable environment for hosting the trained models and backend services. The system ensures that the best model is continuously deployed, allowing for real-time predictions via the **FastAPI** backend. To automate the integration and deployment processes, we implemented a **CI/CD pipeline using CircleCI**. This pipeline automates tasks such as testing, building **Docker** images, pushing them to an **AWS Elastic Container Registry (ECR)**, and deploying updates to the **EC2 instance**. The use of **CircleCI** ensures rapid and error-free deployment, enabling seamless updates and monitoring of the pipeline.

## Addressing Server Response Timeout

A critical challenge in deploying real-time prediction services is managing **server response times**. To address the **1-minute response timeout limitation**, we implemented **Redis and Celery** for asynchronous task handling. Redis serves as the message broker, while **Celery** handles task execution in the background, allowing the server to handle predictions without timeouts. This architecture ensures that users receive timely responses, even under high-load conditions, enhancing the system's robustness.

## Frontend Integration

The project includes a user-friendly **frontend** developed using **HTML, CSS, and JavaScript**. This interface interacts with the backend **FastAPI** services, allowing users to upload news articles and receive predicted categories in real time. The frontend design emphasizes simplicity and responsiveness, ensuring accessibility across devices. Its seamless integration with the backend leverages REST APIs to handle prediction requests, providing a cohesive user experience.

## Tech Stack Used
- **Language**: Python
- **Deep Learning Framework**: PyTorch
- **NLP Library**: Hugging Face Transformers (e.g., BERT, Roberta)
- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Task Management**: Celery
- **Message Queue**: Redis

## Infrastructure
- **Containerization**: DockerHub
- **Deployment**: AWS Elastic Container Registry (ECR)
- **Version Control**: GitHub
- **CI/CD Pipeline**: CircleCI (CI/CD)

## System Design
![image](./assets/SystemDesign.jpg)

## Dataset

The **AG News Topic Classification Dataset** is a benchmark dataset for text classification tasks. It comprises news articles sourced from over **2,000 outlets**, originally gathered by the academic search engine ComeToMyHead, active since 2004. Designed for research in fields like data mining, information retrieval, and text classification, this dataset is widely utilized in academic and experimental studies.

You can download an existing dataset. Here is the Dataset [Link](https://www.kaggle.com/datasets/amananandrai/ag-news-classification-dataset/data)

## Dataset Information

This dataset, curated by Xiang Zhang, includes four major news categories extracted from the original AG corpus. Each category is balanced with:

- **Training samples**: 30,000 per class (total: 120,000 samples)
- **Testing samples**: 1,900 per class (total: 7,600 samples)

### The four categories are:

1) **World**
2) **Sports**
3) **Business**
4) **Science/Technology**

### Files Structure

- **classes.txt**: Lists the four categories.

- **train.csv and test.csv**: Contain labeled news articles with columns for the class index (1–4), title, and description.

- **Formatting**: Titles and descriptions are enclosed in double quotes (") with internal double quote is escaped by 2 double quotes (""). Line breaks are represented as \n.


#### Dataset Details<a id='dataset-details'></a>
<pre>
Dataset Name            : CoNLL-2003
Number of Class         : 2
Number/Size of Images   : Total      : 47960 (4.8 MB)
                          Training   : 47960
                          Testing    : 2000
                          Validation : 2000 

</pre>
## Results<a id='results-'></a>
We have achieved following results with BERT based pretrained model named ***bert-base-cased***.

<pre>
<b>Performance Metrics </b>
Training Accuracy                                 : 86.7%
Testing Accuracy                                  : 85.48%
</pre>

## Installation
    
The Code is written in Python 3.8.19. If you don't have Python installed you can find it here. If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip.

## Run Locally

### Step 1: Clone the repository
```bash
git clone https://github.com/jatin-12-2002/Name_Entity_Recognition_Project
```
### Step 2- Create a conda environment after opening the repository
```bash
conda create -p env python=3.8 -y
```
```bash
source activate ./env
```
### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Create AWS IAM user with following Permissions Enabled

* **AdministratorAccess**
* **AmazonEC2ContainerRegistryFullAccess**
* **AmazonEC2FullAccess**


### Step 5 - Configure your AWS
```bash
aws configure
```

### Step 6 - Enter your AWS Credentials of IAM User
```bash
AWS_SECRET_ACCESS_KEY = ""
AWS_ACCESS_KEY_ID = ""
AWS_REGION = "us-east-1"
AWS_FOLDER = Press Enter and move on
```

### Step 7 - Prepare your Dataset zip file named archive.zip
Your Zip file should contain following folders and files in this order:
```bash
archive.zip
â”‚
â”œâ”€â”€ ner.csv
```

* **Here is my Datset Zip: [LINK](data/archive.zip)**

### Step 8 - Upload the Dataset zip file to your S3 Bucket
```bash
aws s3 cp path/to/your/archive.zip s3://your-bucket-name/archive.zip
```

### Step 9 - Run the application server
```bash
python app.py
```

### Step 10 - Prediction application
```bash
http://localhost:8080/docs

```

### Step 11 - If model is not trained and not present in your S3 bucket
```bash
Run the training Pipeline by clicking on train button in FastAPI UI
```

celery -A celery_app worker --loglevel=info


uvicorn app:app --host 0.0.0.0 --port 8080


aws s3 cp /path/to/local_folder s3://your-bucket-name/your-folder-name --recursive

022499021177.dkr.ecr.us-east-1.amazonaws.com/agnews

b82aebe36b9b8e6069e58ebd040d5d868f7380f2fc642d9dbc47a47446da78f766d4b587a262ebd4
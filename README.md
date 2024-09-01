# Overview
The HealthAdvisorCrew project is a system designed to analyze blood test reports, search for relevant health-related articles, generate health recommendations, and send an email with the results. It utilizes CrewAI to manage agents and tasks, and integrates various tools for document handling, web searching, and email communication.

# Approach and Methodology


 --for the analysis i used gemini-pro model

## Agent Configuration:

blood_test_analyzer: Analyzes the blood test report, identifies abnormalities, and provides a detailed summary.
web_searcher: Searches for health-related articles based on the blood test analysis.
health_recommender: Provides health recommendations based on the articles found.
email_sender: Sends an email with the analysis, articles, and recommendations.


## Task Definitions:

Analyze_Blood_Test: Analyzes the text of a blood test report to identify and explain abnormalities.
search_health_articles_task: Uses online search tools to find relevant health-related articles.
generate_health_recommendations_task: Generates recommendations based on the articles found.
send_email_task: Sends an email containing the results and recommendations.


## Execution Flow:

Extract text from a PDF blood report.
Run the analysis using the HealthAdvisorCrew class.
Generate PDFs for the analysis and recommendations.
Send an email with the PDFs attached.


# Setup Instructions

## Prerequisites:

   -- python
   -- SMTP server credentials for sending emails

## Environment Configuration:

  -- Create a .env file in the root directory with the following content desscribed in .env.example file

## File Setup

-- Place crew.py in the blood_analyst_crew/ directory.
-- Place agents.yaml and tasks.yaml in the config/ directory.
-- Ensure the .env file is in the root directory of the project.

## Installing Dependencies

-- Install the required packages using pip by using command:
-- pip install -r requirements.txt


## Running the Project

-- Extract text from a blood report PDF using the main.py script. Ensure you have a sample PDF file available at the specified path.
-- Run the main.py script to start the process

## Error Handling

-- Ensure that all API keys and environment variables are correctly set in the .env file.
-- Check the email configuration if emails are not being sent.
-- Review the logs and error messages for troubleshooting.


# File Descriptions

-- crew.py: Defines the HealthAdvisorCrew class with agents, tasks, and email functionality.
-- main.py: Extracts text from a PDF, runs the CrewAI process, and generates/sends emails with the results.
-- agents.yaml: Contains configurations for the agents used in CrewAI.
-- tasks.yaml: Defines the tasks for analyzing blood tests, searching articles, generating recommendations, and sending emails.
-- .env: Stores environment variables and API keys.
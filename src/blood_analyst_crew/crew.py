from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.llms import Ollama
from langchain_ollama import ChatOllama
from langchain_community.llms import Ollama

os.environ["SERPER_API_KEY"] = "1c4bb01bc4691aeb1f1a82b33fd3772ae7396eed"
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"]='http://localhost:11434'
os.environ["OPENAI_MODEL_NAME"]='llama2'  # Adjust based on available model



search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

llm = ChatOllama(
    model = "llama3.1",
    base_url = "http://localhost:11434")



@CrewBase
class HealthAdvisorCrew():
    """HealthAdvisorCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def blood_test_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['blood_test_analyzer'],
            llm = llm

           
            
        )
    
    @agent
    def web_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_searcher'],
            
            tools=[search_tool, web_search_tool],
            llm = llm
           
        )
    
    @agent
    def health_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['health_recommender'],
            llm = llm
           
            
        )
    
    @agent
    def email_sender(self) -> Agent:
        return Agent(
            config=self.agents_config['email_sender'],
            llm = llm
            
            
        )
    
    @task
    def Analyze_Blood_Test(self) -> Task:
        return Task(
            config=self.tasks_config['Analyze_Blood_Test'],
            agent=self.blood_test_analyzer()
        )
    
    @task
    def search_health_articles_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_health_articles_task'],
            agent=self.web_searcher()
        )
    
    @task
    def generate_health_recommendations_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_health_recommendations_task'],
            agent=self.health_recommender()
        )
    
    @task
    def send_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['send_email_task'],
            agent=self.email_sender()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the HealthAdvisorCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose= True
        )

    
    
    






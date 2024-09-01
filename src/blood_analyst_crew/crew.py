import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from crewai_tools import WebsiteSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

os.environ["SERPER_API_KEY"] = "164491fa8bd60fbf8f4a21fc82d6564460e3af16"

search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

def create_pdf(text, file_path):
    """Save the given text to a PDF file using FPDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if not isinstance(text, str):
        text = str(text)
    pdf.write(5, text)
    pdf.output(file_path)
def send_email(subject, body, to_email, attachments=None):
    """Send an email with optional attachments."""
    from_email = "deepanshukadam308@gmail.com"
    password = "osipmjfotfkowjie"  # Use the app password if 2FA is enabled

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for file_path in attachments:
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(file_path)}',
            )
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

@CrewBase
class HealthAdvisorCrew():
    """HealthAdvisorCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def blood_test_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['blood_test_analyzer'],
            llm=llm
        )
    
    @agent
    def web_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_searcher'],
            llm=llm,
            tools=[search_tool, web_search_tool]
        )
    
    @agent
    def health_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['health_recommender'],
            llm=llm,
            
        )
    
    
    @task
    def Analyze_Blood_Test(self) -> Task:
        return Task(
            config=self.tasks_config['Analyze_Blood_Test'],
            agent=self.blood_test_analyzer(),
            delegation=False,
            output_file="analysis_report.pdf",  # Specify the output file for PDF
            #callback=self.save_analysis_callback # Call the callback function after analysis
        )
    
    @task
    def search_health_articles_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_health_articles_task'],
            agent=self.web_searcher(),
            delegation=False
        )
    
    @task
    def generate_health_recommendations_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_health_recommendations_task'],
            agent=self.health_recommender(),
            output_file="recommendations_report.pdf",  # Specify the output file for PDF
            #callback=self.save_recommendations_callback  # Call the callback function after generating recommendations
        )
    
    
    @crew
    def crew(self) -> Crew:
        """Creates the HealthAdvisorCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    

    def create_and_send_pdf(self, result_text, recipient_email):
        """Create a PDF from the result text and send it via email."""
        if not isinstance(result_text, str):
            result_text = str(result_text)
        pdf_path = "output/health_recommendations.pdf"
        create_pdf(result_text, pdf_path)
        send_email(
            subject="Health Recommendations Report",
            body="Please find the health recommendations attached.",
            to_email=recipient_email,
            attachments=[pdf_path]
        )
        print("Email sent successfully with the PDF attachment.")

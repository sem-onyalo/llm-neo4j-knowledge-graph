# This will test the environment to ensure that the .env file is set up 
# correctly and that the OpenAI and Neo4j connections are working.
import os
import unittest

from dotenv import load_dotenv, find_dotenv
load_dotenv()

class TestEnvironment(unittest.TestCase):

    skip_env_variable_tests = True
    skip_openai_test = True
    skip_neo4j_test = True

    def test_env_file_exists(self):
        env_file_exists = True if find_dotenv() > "" else False
        if env_file_exists:
            TestEnvironment.skip_env_variable_tests = False
        self.assertTrue(env_file_exists, ".env file not found.")

    def env_variable_exists(self, variable_name):
        self.assertIsNotNone(
            os.getenv(variable_name),
            f"{variable_name} not found in .env file")

    def test_azure_openai_variables(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping OpenAI env variable test")

        self.env_variable_exists('AZURE_OPENAI_API_KEY')
        self.env_variable_exists('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME')
        self.env_variable_exists('AZURE_OPENAI_ENDPOINT')
        self.env_variable_exists('AZURE_OPENAI_MODEL_DEPLOYMENT_NAME')
        self.env_variable_exists('OPENAI_API_VERSION')
        TestEnvironment.skip_openai_test = False

    def test_neo4j_variables(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping Neo4j env variables test")

        self.env_variable_exists('NEO4J_URI')
        self.env_variable_exists('NEO4J_USERNAME')
        self.env_variable_exists('NEO4J_PASSWORD')
        TestEnvironment.skip_neo4j_test = False

    def test_azure_openai_connection(self):
        if TestEnvironment.skip_openai_test:
            self.skipTest("Skipping OpenAI test")

        from openai import APIConnectionError, NotFoundError
        from langchain_openai import AzureChatOpenAI

        llm = AzureChatOpenAI(
            azure_deployment=os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT_NAME'),
        )

        what_to_check = "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_MODEL_DEPLOYMENT_NAME, and OPENAI_API_VERSION values"

        try:
            response = llm.invoke("Who are you?")
        except NotFoundError:
            response = None
            what_to_check = "AZURE_OPENAI_MODEL_DEPLOYMENT_NAME key"
        except APIConnectionError:
            response = None
            what_to_check = "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and OPENAI_API_VERSION values"

        self.assertIsNotNone(
            response,
            f"Azure OpenAI connection failed. Check the {what_to_check} in .env file.")

    def test_neo4j_connection(self):
        if TestEnvironment.skip_neo4j_test:
            self.skipTest("Skipping Neo4j connection test")

        from neo4j import GraphDatabase

        driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USERNAME'), 
                  os.getenv('NEO4J_PASSWORD'))
        )
        try:
            driver.verify_connectivity()
            connected = True
        except Exception as e:
            connected = False

        driver.close()

        self.assertTrue(
            connected,
            "Neo4j connection failed. Check the NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD values in .env file."
            )
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEnvironment('test_env_file_exists'))
    suite.addTest(TestEnvironment('test_azure_openai_variables'))
    suite.addTest(TestEnvironment('test_neo4j_variables'))
    suite.addTest(TestEnvironment('test_azure_openai_connection'))
    suite.addTest(TestEnvironment('test_neo4j_connection'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    

from langchain_openai import ChatOpenAI;
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from ..config import settings
from ..prompts.legal_template import legal_system_prompt

class LegalAdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=1,
            model="gpt-4o-mini"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            legal_system_prompt,
            ("user", "{question}")
        ])

        self.chain = (
            {"question": RunnablePassthrough()} 
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )

    async def get_response(self, question: str) -> str:
        """
        Get a response from the legal advisor chain.
        
        Args:
            question: The legal question to answer
            
        Returns:
            str: The AI-generated response
        """
        try:
            response = await self.chain.ainvoke(question)
            return response
        except Exception as e:
            print(f"Error in legal advisor chain: {str(e)}")
            return "I apologize, but I encountered an error while processing your question. Please try again." 
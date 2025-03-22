from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from ..prompts.legal_template import legal_system_prompt
from ..config import settings

class LegalAdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.7,
            model="gpt-3.5-turbo"
            )
        
        self.messages = []
        
        self.prompt = ChatPromptTemplate.from_messages([
            legal_system_prompt,
            *self.messages,
            ("user", "{question}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def _update_messages(self, question: str, answer: str):
        """
        Update the conversation history with the new question and answer.
        
        Args:
            question: The user's question
            answer: The AI's response
        """
        self.messages.append(HumanMessage(content=question))
        self.messages.append(AIMessage(content=answer))
        
        self.prompt = ChatPromptTemplate.from_messages([
            legal_system_prompt,
            *self.messages,
            ("user", "{question}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    async def get_response(self, question: str) -> str:
        """
        Get a response from the legal advisor chain.
        
        Args:
            question: The legal question to answer
            
        Returns:
            str: The AI-generated response
        """
        try:
            response = await self.chain.ainvoke({"question": question})
            
            self._update_messages(question, response)
            
            return response
        except Exception as e:
            print(f"Error in legal advisor chain: {e}")
            return "I apologize, but I encountered an error while processing your question. Please try again." 
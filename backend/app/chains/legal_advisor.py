from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from ..prompts.legal_template import legal_system_prompt
from ..config import settings

class LegalAdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        
        self.memory = ConversationBufferMemory(
            return_messages=True,
            output_key="response",
            input_key="question"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            legal_system_prompt,
            ("user", "{question}")
        ])

        self.chain = (
            RunnablePassthrough.assign(
                history=lambda _: self.memory.load_memory_variables({})["history"]
            )
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
            response = await self.chain.ainvoke({"question": question})
            
            self.memory.save_context(
                {"question": question},
                {"response": response}
            )
            
            return response
        except Exception as e:
            print(f"Error in legal advisor chain: {e}")
            return "I apologize, but I encountered an error while processing your question. Please try again." 
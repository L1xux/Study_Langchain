from typing import Tuple
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from agents.linkedin_lookup_agent import lookup
from thired_parties.linkedin import scrape_linkedin_profile
from output_parser import Summary, summary_parser

def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    summary_template = """
        given the information {information} about a person from i want you to create:
        1. a short summary
        2. two interesting facts about them
        \n{format_instructions}
        
    """
    
    summary_prompt_template = PromptTemplate(
        input_variables="information", 
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )
    
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data})
    
    print(res)
    
    return res, linkedin_data.get("profile_pic_url")

if __name__ == '__main__':
    load_dotenv()
    
    ice_break_with(name="Eden Marco Udemy")

import config
from ai import AI
from luna import Luna
from PyPDF2 import PdfReader

from vectordb import vectorDB
ai = AI()
luna = Luna()

pageText = "";
with open("./tb-summary-100223.pdf", 'rb') as file:
  pdfReader = PdfReader(file)
  numPages = len(pdfReader.pages)
  for pageNum in range(numPages):
    page = pdfReader.pages[pageNum]
    pageText += page.extract_text()

db = vectorDB()
db.create_db_fromText(pageText, "nasa_base")
#qa = db.init_qa_context("nasa_file_name")
#res = qa("what is the gist of the text")
#print(res['result'])


#answer = db.get_answer_content("nasa_file_name", "Is there any ambiguity sentence: The System Safety Project Plan should describe interfaces within the assurance disciplines as well as the other project disciplines")
#print(answer)

user_prompt = "Partial or total autonomous control of safety-critical functions by software"
context = db.get_context_documents("nasa_base", "Get all document relating to:" + user_prompt)
print("context:---------------->")
print(context)
#resp = ai.prompt("with the context of " + context, "is this sentence written without ambiguity: Get all document relating to: improvements that may reduce the required effort to develop the software and/or the number of inherent defects")
#luna = Luna()
#resp = luna.prompt(context, "Assist me in reviewing NASA Technical Standards for clarity and consistency, identifying and rectifying any ambiguities or errors with the following: Partial or total autonomous control of safety-critical functions by software. Complex system with multiple subsystems, interacting parallel processors, or multiple interfaces.Some or all safety-critical functions are time critical.Control of hazard but other safety systems can partially mitigate.Detects hazards, notifies human operator of need for safety actions.Moderately complex with few subsystems and/or a few interfaces, no parallel processing.Some hazard control actions may be time critical but do not exceed time needed for adequate human operator or automated system response.Several mitigating systems prevent hazard if software malfunctions. Redundant sources of safety-critical information.Somewhat complex system, limited number of interfaces. Mitigating systems can respond within any time critical period.No control over hazardous hardware.")

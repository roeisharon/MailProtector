from pydantic import BaseModel

# Request model for incoming email data to be analyzed
class EmailRequest(BaseModel):
    subject: str
    sender: str
    body: str
    headers: str
    attachments: list[str] = []
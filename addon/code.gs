function getContextualAddOn(e) {
  const accessToken = e.gmail.accessToken;
  GmailApp.setCurrentMessageAccessToken(accessToken); 

  const message = GmailApp.getMessageById(e.gmail.messageId);
  const attachments = message.getAttachments({includeInlineImages: false});

  const attachmentNames = [];
  for (var i = 0; i < attachments.length; i++) {

    attachmentNames.push(
      attachments[i].getName()
    );
  }
 
  const payload = {
    subject: message.getSubject(),
    sender: message.getFrom(),
    body: message.getPlainBody(),
    headers: message.getRawContent(),
    attachments: attachmentNames
  }

  const BACKEND_URL = "PUT YOUR BACKEND URL HERE";
  const response = UrlFetchApp.fetch(
    BACKEND_URL,
    {
      method: "POST",
      contentType:"application/json",
      payload: JSON.stringify(payload)
    }
  );

  const result = JSON.parse(
    response.getContentText()
  );

  return buildResultCard(result);
}
function buildResultCard(result) {
  const card = CardService.newCardBuilder();
  const section = CardService.newCardSection();

  const severity = getSeverityConfig(result.verdict);

  section.addWidget(
    CardService.newDecoratedText()
      .setText("<b>Email Security Analysis</b>")
      .setBottomLabel("Risk Score: " + result.score + "/100")
  );

  section.addWidget(
    CardService.newTextParagraph()
      .setText("<b>" + severity.icon + " " + result.verdict + "</b>")
  );

  section.addWidget(CardService.newDivider());

  if (result.reasons.length > 0) {
    section.addWidget(
      CardService.newTextParagraph()
        .setText("<b>Detected Signals</b>")
    );
    for (var i = 0; i < result.reasons.length; i++) {
      section.addWidget(
        CardService.newTextParagraph()
          .setText(result.reasons[i])
      );
    }
  } else {
    section.addWidget(
      CardService.newDecoratedText()
        .setText("No major security concerns were detected")
    );
  }

  section.addWidget(CardService.newDivider());

  section.addWidget(
    CardService.newTextParagraph()
      .setText("<b>AI Security Summary</b>")
  );
  section.addWidget(
    CardService.newTextParagraph()
      .setText(result.llm_summary)
  );

  section.addWidget(CardService.newDivider());

  section.addWidget(
  CardService.newDecoratedText()
    .setBottomLabel(
      "⚠️ AI-assisted analysis. Always use caution with suspicious emails."
    )
  );

  card.addSection(section);
  return card.build();
}


function getSeverityConfig(verdict) {
  if (verdict === "Safe") return { icon: "✅" };
  if (verdict === "Low Risk") return { icon: "🟡" };
  if (verdict === "Suspicious") return { icon: "🟠" };
  if (verdict === "High Risk") return { icon: "🔴" };
  return { icon: "🚨" };
}
function buildResultCard(result) {
  const card = CardService.newCardBuilder();
  const section = CardService.newCardSection();

  const severity = getSeverityConfig(result.verdict);

  section.addWidget(
    CardService.newDecoratedText()
      .setText(forceLTR("<b>Email Security Analysis</b>"))
      .setBottomLabel(forceLTR("Risk Score: " + result.score + "/100"))
  );

  section.addWidget(
    CardService.newTextParagraph()
      .setText(forceLTR("<b>" + severity.icon + " " + result.verdict + "</b>"))
  );

  section.addWidget(CardService.newDivider());

  if (result.reasons.length > 0) {
    section.addWidget(
      CardService.newTextParagraph()
        .setText(forceLTR("<b>Detected Signals</b>"))
    );
    for (var i = 0; i < result.reasons.length; i++) {
      section.addWidget(
        CardService.newDecoratedText()
          .setText(forceLTR(result.reasons[i]))
      );
    }
  } else {
    section.addWidget(
      CardService.newDecoratedText()
        .setText(forceLTR("No major security concerns were detected"))
    );
  }

  section.addWidget(CardService.newDivider());

  section.addWidget(
    CardService.newTextParagraph()
      .setText(forceLTR("<b>AI Security Summary</b>"))
  );
  section.addWidget(
    CardService.newTextParagraph()
      .setText(forceLTR(result.llm_summary))
  );

  card.addSection(section);
  return card.build();
}

function forceLTR(text) {
  return "\u202A" + text + "\u202C";
}

function getSeverityConfig(verdict) {
  if (verdict === "Safe") return { icon: "✅" };
  if (verdict === "Low Risk") return { icon: "🟡" };
  if (verdict === "Suspicious") return { icon: "🟠" };
  if (verdict === "High Risk") return { icon: "🔴" };
  return { icon: "🚨" };
}
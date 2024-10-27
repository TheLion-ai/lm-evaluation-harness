# Copied from Master
def doc_to_text(doc) -> str:
    """
    Question: <question>
    Choices:
    A. <choice1>
    B. <choice2>
    C. <choice3>
    D. <choice4>
    Answer:
    """
    option_choices = {
        "A": doc["odpowiedzi"][0].strip(),
        "B": doc["odpowiedzi"][1].strip(),
        "C": doc["odpowiedzi"][2].strip(),
        "D": doc["odpowiedzi"][3].strip(),
    }

    prompt = "Pytanie: " + doc["pytanie"] + "\nOdpowiedzi do wyboru:\n"
    for choice, option in option_choices.items():
        prompt += f"{choice.upper()}. {option}\n"
    prompt += "Odpowiedź:"
    return prompt

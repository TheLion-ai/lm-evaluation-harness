def doc_to_text(doc) -> str:
    option_choices = {
        "A": doc["A"],
        "B": doc["B"],
        "C": doc["C"],
        "D": doc["D"],
        "E": doc["E"],
    }
    # answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    prompt = "Pytanie: " + doc["question"] + "\nOdpowiedzi do wyboru:\n"
    for choice, option in option_choices.items():
        prompt += f"{choice.upper()}. {option}\n"
    prompt += "Odpowiedź: "
    return prompt

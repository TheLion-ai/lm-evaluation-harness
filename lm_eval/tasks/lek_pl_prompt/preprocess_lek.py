def doc_to_text(doc) -> str:
    option_choices = {
        "A": doc["A"],
        "B": doc["B"],
        "C": doc["C"],
        "D": doc["D"],
        "E": doc["E"],
    }
    # answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    prompt = ("""# 
Task: You are a helpful assistant.
## General Instructions: - Generate detailed and structured medical responses based on the given
medical question. Answers should be grounded in current medical knowledge, covering all key aspects
of the question.
- Ensure the answer includes background, etiology, symptoms, diagnosis, treatment, and prevention.
- The answer should be logically organized and provide accurate, comprehensive medical information.
## Task Instructions: - Generate the best answer based on the input question. The response
should be based on everything from background information to diagnosis and treatment recommendations.
- The answer should address as many aspects of the medical question as possible, considering risk
factors, complications, and related medical conditions.
- Consider the relationship between diseases and medications.
## Chain of Thought:
### 1. Understand the Question:
- Use the background or definition of the medical issue. Use a brief description of basic concepts
and possibly affected systems or organs.
- Identify and define key medical terms and concepts.
- Clarify the specific information or details requested.
### 2. Recall Relevant Medical Knowledge: - Retrieve information related to the disease, medication,
or procedure.
- Consider anatomy, physiology, pathology, pharmacology, and current medical guidelines.
### 3. Analyze Medical Information: - Combine 1. understanding the question and 2. relevant medical
knowledge to connect the issue with pertinent medical knowledge using clinical reasoning.
- Consider possible explanations, mechanisms, or interactions.
### 4. Assess Impacts and Considerations:
- Evaluate any risks, side effects, or contraindications.
- Consider specific patient factors (age, comorbidities, allergies).
### 5. Provide Additional Relevant Information:
- Consider important details that help in understanding.
- Consider any exceptions, alternative options, or preventive measures.
### 6. Reference Reliable Sources:
- Base responses on evidence from authoritative medical texts or guidelines.
Answer with only one letter corresponding to the correct answer.
### END

"Question: """) + doc["question"] + "\nAnswers to chose from:\n"
    for choice, option in option_choices.items():
        prompt += f"{choice.upper()}. {option}\n"
    prompt += "Answer: "
    return prompt

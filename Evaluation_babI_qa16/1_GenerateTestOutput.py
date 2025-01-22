import sys
import os

lines = ""#"../../babI/task_16_v1-2/en-valid/qa16_test.txt"
with open("/Users/patham9/babI/tasks_1-20_v1-2/en/qa15_basic-deduction_test.txt") as f: #qa16_basic-induction_test.txt #qa15_basic-deduction_test.txt
    lines = f.read().split("\n")

cwd = os.getcwd()
sys.path.append(cwd + "/../")
os.chdir(cwd + "/../")
from NarsGPT import *
os.chdir(cwd)
import json

lastnum = -1
examples = []
example_cur = []
for line in lines:
    if line.strip() == "":
        continue
    words = line.split(" ")
    number, text = (int(words[0]), " ".join(words[1:]))
    if number < lastnum:
        examples.append(example_cur)
        example_cur = []
    example_cur.append(text)
    lastnum = number
examples.append(example_cur)

def question_and_expected_output(questionlines):
    L = []
    for questionline in questionlines:
        splitted = questionline.split("\t")
        L.append([splitted[0], splitted[1]])
    return [L]

examples = [[" ".join([x for x in example if "?" not in x])] + question_and_expected_output([x for x in example if "?" in x]) for example in examples]
#print(examples); exit(0)

Line_Input_Output_ExpectedOutput = []
ExampleID = 1
for example in examples:
    #print(example); exit(0)
    BeliefInput, QuestionInputs_expectedOutputs = example
    outputFromBeliefInput = AddInput(BeliefInput, Print=False, PrintInputSentenceOverride=True, PrintInputSentenceOverrideValue=True)["GPT_Answer"]
    for QuestionInput, expectedOutput in QuestionInputs_expectedOutputs:
        expectedOutput = expectedOutput.strip()
        actualOutput = AddInput(QuestionInput, Print=False, PrintInputSentenceOverride=True, PrintInputSentenceOverrideValue=True)["GPT_Answer"]
        Dic = {"ExampleID": ExampleID, "Input": BeliefInput + " " + QuestionInput, "OutputFromBeliefInput": outputFromBeliefInput,"actualOutput": actualOutput, "expectedOutput": expectedOutput}
        Line_Input_Output_ExpectedOutput.append(Dic)
    for k in Dic:
        print(k+":", Dic[k])
    print("\n")
    filename = "TestOutput.json"
    with open(filename, 'w') as f:
        json.dump(Line_Input_Output_ExpectedOutput, f)
    ExampleID += 1
    AddInput("*reset")



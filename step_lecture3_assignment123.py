import sys

## Tokenize numbers.
def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index

## Tokenize operators.
def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readMul(line, index):
  token = {'type': 'MUL'}
  return token, index + 1

def readDiv(line, index):
  token = {'type': 'DIV'}
  return token, index + 1

def readParenL(line, index):
  token = {'type': 'LPAREN'}
  return token, index + 1

def readParenR(line, index):
  token = {'type': 'RPAREN'}
  return token, index + 1


## Convert input into a set of tokens.
def tokenize(line):
  tokens = []
  index = 0
  token = None
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMul(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index) 
    elif line[index] == '(':
      (token, index) = readParenL(line, index)
    elif line[index] == ')':
      (token, index) = readParenR(line, index)
    else:
      print('Invalid character found: ' + line[index])
      sys.exit(1)
    tokens.append(token)
  return tokens


## Evaluates the atom of tokens (inside brakets)
def evaluate_atom(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1

  while index < len(tokens)-1:   # 1st iteration to calculate just multiplication and division.
    if tokens[index]['type'] == 'MUL':
      tokens[index-1]['number'] = tokens[index-1]['number']*tokens[index+1]['number']
      tokens.pop(index)
      tokens.pop(index)
    elif tokens[index]['type'] == 'DIV':
      if tokens[index+1]['number'] == 0:
        print('Error: Division by 0 ')  
        sys.exit(1)
      else:
        tokens[index-1]['number'] = tokens[index-1]['number']/tokens[index+1]['number']  
        tokens.pop(index)
        tokens.pop(index)
    elif tokens[index]['type'] == 'LPAREN':  # Check for extra left braket.
      print('Error: Invalid syntax')
      sys.exit(1)
    else:
      index += 1
  if tokens[-1]['type'] != 'NUMBER':
    print('Error: Invalid syntax')
    sys.exit(1)
  index = 1

  while index < len(tokens):  # 2nd iteration to calculate addition and subtraction. 
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Error: Invalid syntax')
        exit(1)
    index += 1
  return answer


## Evaluate whole list of tokens
def evaluate_whole(tokens):
  index = 0
  tokens_stack = []
  tokens_out = []

  while index < len(tokens):
    if tokens[index]['type'] == 'RPAREN':
      while True:    
        tokens_out.insert(0, tokens_stack.pop())
        if len(tokens_stack) == 0:  # Check for extra right braket.
          print("Error: Invalid syntax")
          sys.exit(1)
        if tokens_stack[-1]['type'] == 'LPAREN':
          tokens_stack.pop()
          break  
      tokens_stack.append({'type':'NUMBER', 'number': evaluate_atom(tokens_out)})
      tokens_out = []
    else:
      tokens_stack.append(tokens[index])   
    index += 1

  return evaluate_atom(tokens_stack)



def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate_whole(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))



def runTest():
  print("==== Test started! ====")
  test("1+2")         # Normal operation
  test("1.0+2.1-3")   # Floating number
  test("-2+2")        # Negative number
  test("1.0+0.5*2/4") # Division and Multiplication
  test("(1+1)/2")     # Brakets
  test("(1+2/(1+1))+1")   # Nested Brakets
  test("-(2+2)")      # Brakets with negative number
  test("((0.01)+2)")  # Brakets for entire function
  test("1")           # Single number
  test("((((1))))")   # Single number with brakets
  
  #test("1000000000/0.00000001")   # Overflow
  #test("1+2*")       # Invalid input
  #test("   ")        # Invalid input
  #test("2*7/(0.5))") # Unmatched brakets
  #test("((2+4)")     # Unmatched brakets
  #test("あ")         # Invalid input 
  #test("5/0")        # Division by 0
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate_whole(tokens)
  print("answer = %f\n" % answer)
  
  

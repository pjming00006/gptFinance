delimiter = "####"

system_message_parsing = f"""
You will be provided with a JSON structure, which is a credit card transaction record retrieved from a bank.
The JSON structure will be delimited with {delimiter}.
Output a JSON object with the following format:
'Date': <The date of the transaction in the format of yyyy-mm-dd>
'Merchant': <The merchant of the transaction>
'Amount': <The amount of the transaction>

Follow the steps to generate the output:
Step 1:{delimiter} First, from the input JSON, infer which each input keys should map to the output keys
Step 2:{delimiter} After you have successfully mapped the input to the defined output JSON structure, format the value within the 'Date'
key to be yyyy-mm-dd
Step 3:{delimiter} Format the value within the 'Amount' key to be a number rounded with 2 decimal places. In addition, all the minus signs
should be removed
Step 4:{delimiter} For all the keys and values in the output JSON structure, make sure all the single quotes are replaced with double quotes

Your response should only contain the JSON object with nothing else.
"""

system_message_category = """
You will be provided with a JSON structure, which is a processed credit card transaction record
The JSON structure will be delimited with {delimiter}.

Output a JSON that represents the category of the transaction with the following format:
Output format: "Category": <The category of the transaction>
Make sure the output is a JSON with brackets. Do not return anything other than the JSON itself.

Determine the category by evaluating the following category information delimited with three backticks. Only use categories given below.
```
{cate_str}
```
"""
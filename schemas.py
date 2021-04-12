#https://json-schema.org/understanding-json-schema/
#https://json-schema.org/learn/getting-started-step-by-step.html#data
#https://awslabs.github.io/aws-lambda-powertools-python/latest/utilities/validation/

INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "feedback form input schema",
    "description": "feedback form input schema",
    "examples": [{"name": "john wick", "country": "India", "subject": "some nonsense data"}],
    "required": ["name", "country", "subject"],
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 50
        },
        "country": {
            "type": "string",
            "pattern": "(India|New Zealand|Sri Lanka)",
            "maxLength": 50
        },
        "subject": {
            "type": "string",
            "maxLength": 50
        }
    },
}
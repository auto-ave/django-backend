STORE_TIMES_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'array',
    'properties': {
        'items': {
            'type': 'object',
        },
        'minItems': 7,
        'maxItems': 7,
    },
    'required': ['my_key']
}
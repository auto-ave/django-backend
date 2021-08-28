STORE_TIMES_FIELD_SCHEMA = {
    'type': 'array',
    'minItems': 7,
    'maxItems': 7,
    'items': {
        'type': 'object',
        'properties': {
            'opening_time': {'type': 'string'},
            'closing_time': {'type': 'string'},
        },
        'additionalProperties': False,
    },
    'required': ['my_key']
}
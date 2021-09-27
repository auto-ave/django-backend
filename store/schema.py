STORE_TIMES_FIELD_SCHEMA = {
    'type': 'array',
    'minItems': 7,
    'maxItems': 7,
    'items': {
        'type': 'object',
        'properties': {
            'opening_time': {'type': 'string',
                            'pattern': '^([01]?[0-9]|2[0-3]):[0-5][0-9]$'},
            'closing_time': {'type': 'string',
                            'pattern': '^([01]?[0-9]|2[0-3]):[0-5][0-9]$'},
        },
        'additionalProperties': False,
    },
    'required': ['my_key']
}
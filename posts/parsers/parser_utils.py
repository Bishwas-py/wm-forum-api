def get_p(obj):
    return {
        'id': obj.content_type.id,
        'type_': obj.content_type.model,
    }

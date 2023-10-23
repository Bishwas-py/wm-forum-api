def get_poly(obj, c_id=True, c_type=True):
    """
    Helps to get polymorphic content data.
    """
    data = {
        'obj_id': obj.content_object.id
    }
    if c_id:
        data['c_id'] = obj.content_type.id
    if c_type:
        data['c_type'] = obj.content_type.model
    return data

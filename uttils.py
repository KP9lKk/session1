
def to_json_str(value :str):
    return value.replace("True", "true").replace("False", "false").replace("\'", "\"").replace("None", "null")

def get_salary_value(to_value, from_value):
    if not from_value:
        from_value = 0
    if not to_value:
        to_value = 0

    return  (from_value + to_value) // 2
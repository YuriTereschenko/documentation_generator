
class Column:
    md_template = '|{name}|{type}|{required}|{default}|{constraint}|{description}|'

    def __init__(self, column_name, data_type, required_field, column_default, description, constraint):
        self.column_name = column_name.replace("_", "\\_")
        self.data_type = data_type
        self.required_field = required_field
        self.column_default = column_default
        self.description = description
        self.constraint = constraint

    def generate_md_string_column(self) -> str:
        return self.md_template.format(name=self.column_name,
                                        type=self.data_type,
                                        required=self.required_field,
                                        default=self.column_default,
                                        constraint=self.constraint,
                                        description=self.description)
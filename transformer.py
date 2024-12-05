# transformer.py
import json
import os

class SchemaTransformer:
    def build_from_json(self, json_file_path):
        with open(json_file_path) as f:
            input_data = json.load(f)
            
        filename = os.path.basename(json_file_path)
        provider, schema_name = filename.split('_')[:2]
        schema_name = schema_name.split('.')[0]
        
        schema = json.load(open(f'schema/{schema_name}.json'))
        mapping_config = json.load(open('mapping.json'))
        
        mappings = mapping_config.get(schema_name, {}).get(provider, {})
        output = {}
        
        # Handle mapped fields
        for src_field, target_field in mappings.items():
            if src_field in input_data:
                output[target_field] = input_data[src_field]
                
        # Handle nested fields and validate types
        for field, value in input_data.items():
            if field in schema and field not in mappings:
                if isinstance(schema[field], dict):
                    if not isinstance(value, dict):
                        raise ValueError(f"Field {field} must be an object")
                    output[field] = value
                elif schema[field].startswith('list'):
                    if not isinstance(value, list):
                        raise ValueError(f"Field {field} must be a list")
                    output[field] = value
                else:
                    if not isinstance(value, str):
                        raise ValueError(f"Field {field} must be a string")
                    output[field] = value

        # Validate required fields
        required_fields = {k for k in schema if k != 'optional' and isinstance(schema[k], (str, dict))}
        optional_fields = set(schema.get('optional', []))
        valid_fields = required_fields | optional_fields | set(mappings.values())
        
        missing_required = required_fields - optional_fields - set(output.keys())
        if missing_required:
            raise ValueError(f"Missing required fields: {missing_required}")
            
        return output
import pytest
from transformer import SchemaTransformer

def test_valid_input():
    transformer = SchemaTransformer()
    result = transformer.build_from_json('sample_data/input_files/google_user.json')
    assert 'displayName' in result
    assert isinstance(result['addresses'], list)

def test_type_validation():
    transformer = SchemaTransformer()
    with pytest.raises(ValueError, match="must be a list"):
        transformer.build_from_json('test_data/invalid_type.json')

def test_required_fields():
    transformer = SchemaTransformer()
    with pytest.raises(ValueError, match="Missing required fields"):
        transformer.build_from_json('sample_data/input_files/google_user_required_missing.json')
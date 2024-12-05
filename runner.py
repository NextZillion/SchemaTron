from transformer import SchemaTransformer
import json

def main():
    transformer = SchemaTransformer()
    input_files = [
        'sample_data/input_files/google_user.json',
    ]
    
    for input_file in input_files:
        try:
            result = transformer.build_from_json(input_file)
            output_file = input_file.replace('input_files', 'output_files').replace('.json', '_output.json')
            
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Processed {input_file}")
            
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")

if __name__ == "__main__":
    main()
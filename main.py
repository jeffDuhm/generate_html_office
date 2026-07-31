import argparse
from pathlib import Path
import re
from docx import Document
import json

from parser.word_reader import WordReader
from renderer.html_renderer import renderer_html
from normalizers.blocks_normalizer import normalize_blocks

# Carga el rules correspondiente de cada sitio
def load_rules(site):
    with open(f"config/{site}.json", 'r', encoding="utf-8") as file:
        return json.load(file)
    
def sanitize_filename(filename: str) -> str:
    name = Path(filename).stem # sin .docx

    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "-", name.strip())
    
    return name.lower()
    
def main(site, input_dir="input", output_dir="output"):
    
    rules = load_rules(site)
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    docx_files = list(input_path.glob("*.docx"))
    
    for file in docx_files:
        
        doc = Document(file)
        
        reader = WordReader(rules)
        blocks = reader.parse_document(doc)
        #normalized_blocks = normalize_blocks(blocks)
        html = renderer_html(blocks, rules)
        
        output_name = f"{sanitize_filename(file.name)}.html"
        output_file = output_path / output_name
        
        output_file.write_text(html, encoding="utf-8")
        
        print(f"Generado: {output_file}")

if __name__ == "__main__":

    valid_sites = [
        p.stem for p in Path("config").glob("*.json")
    ]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--site",
        required=True,
        choices=valid_sites,
        help=f"Sitios disponibles: {', '.join(valid_sites)}"
    )

    parser.add_argument("--input", default="input")
    parser.add_argument("--output", default="output")

    args = parser.parse_args()

    main(args.site, args.input, args.output)
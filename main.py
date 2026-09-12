import argparse
from pathlib import Path
from utils.filename import sanitize_filename
from config.config_loader import ConfigLoader
from converter.word_to_html_converter import WordToHtmlConverter
from docx import Document
    
def main(site, input_dir="input", output_dir="output"):
    
    rules = ConfigLoader.load_rules(site)
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    docx_files = list(input_path.glob("*.docx"))
    
    for file in docx_files:
        
        doc = Document(file)
        
        converter = WordToHtmlConverter(doc, rules)
        html = converter.convert()
        
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
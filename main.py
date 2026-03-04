import os
import logging
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

from pdf_parser import extract_text_from_pdf
from llm_client import analyze_text_with_groq
from utils import chunk_text, youtube_links

load_dotenv()
print("API KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_chunk(index, chunk):
    logging.info(f"Processing section {index} ({len(chunk)} chars)...")
    raw = analyze_text_with_groq(chunk)
    result = youtube_links(raw)
    return index, f"## Section {index}\n{result}\n---"

def main():
    # File picker popup
    root = tk.Tk()
    root.withdraw()
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_path:
        logging.info("No file selected.")
        return
        
    logging.info("Extracting text from PDF...")
    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        logging.error(f"Error: {e}")
        return
        
    if not text.strip():
        logging.warning("No readable text found.")
        return
        
    logging.info("Analyzing with Groq...")
    chunks = chunk_text(text, target_size=4000)
    
    results_dict = {}
    total_chunks = len(chunks)
    
    # Process chunks in parallel
    max_workers = min(5, total_chunks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_chunk, i+1, chunk): i+1 for i, chunk in enumerate(chunks)}
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            try:
                chunk_index, result_text = future.result()
                results_dict[chunk_index] = result_text
            except Exception as e:
                logging.error(f"Unhandled exception in future for section {index}: {e}")
                results_dict[index] = f"\n> [!WARNING]\n> Error processing section {index}: {e}\n"

    outputs = [
        f"# AI Study Notes\n\nGenerated from: `{os.path.basename(pdf_path)}`\n\n---\n"
    ]
    
    # Reassemble in order
    for i in range(1, total_chunks + 1):
        if i in results_dict:
            outputs.append(results_dict[i])

    final_output = "\n".join(outputs)
    output_path = os.path.splitext(pdf_path)[0] + "_study_notes.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)
        
    logging.info(f"Success! Results saved to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()

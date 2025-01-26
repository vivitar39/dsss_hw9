from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download

# Define the model ID from Hugging Face
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("Downloading TinyLlama model...")

# Download the model to a local folder
snapshot_download(repo_id=MODEL_ID, local_dir="TinyLlama-1.1B")

print("Model download complete! The model is saved in 'TinyLlama-1.1B'.")

# Load the tokenizer and model to verify the download
tokenizer = AutoTokenizer.from_pretrained("TinyLlama-1.1B")
model = AutoModelForCausalLM.from_pretrained("TinyLlama-1.1B")

print("TinyLlama model is ready to use!")


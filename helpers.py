from transformers import BartForConditionalGeneration, BartTokenizer

def load_model_and_tokenizer(model_path):
    """Load the fine-tuned model and tokenizer."""
    model = BartForConditionalGeneration.from_pretrained(model_path)
    tokenizer = BartTokenizer.from_pretrained(model_path)
    return model, tokenizer

# from transformers import BertTokenizer, BertForSequenceClassification
# import torch 


# def get_BERT():
#     model = BertForSequenceClassification.from_pretrained(r"C:/PreTrainedModels/BERT_PyTorch/")
#     tokenizer = BertTokenizer.from_pretrained(r"C:/PreTrainedModels/BERT_PyTorch/")
#     return model, tokenizer

# def preprocess_text(text, tokenizer, max_length=512):
#     tokens = tokenizer(
#         text,
#         max_length=max_length,
#         truncation=True,
#         padding="max_length",
#         return_tensors="pt",
#     )
#     return tokens

# def predict_sentiment(article):
#     model, tokenizer = get_BERT()

#     # Preprocess the text
#     inputs = preprocess_text(article, tokenizer)

#     # Perform inference
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits

#     # Convert logits to probabilities
#     probabilities = torch.softmax(logits, dim=1).flatten()
#     sentiment_score = probabilities.argmax().item()
#     return sentiment_score  # Example: 0 (negative), 1 (neutral), 2 (positive)




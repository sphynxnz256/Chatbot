import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Set up 4-bit quantization for memory efficiency
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# Load model and tokenizer
model_name = "Qwen/Qwen-7B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    bf16=True,
)

# Generate a repsonse from a prompt
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,    
        return_dict_in_generate=True,        
    )

    generated_ids = outputs.sequences[0, inputs["input_ids"].shape[-1]:]

    # Filter junk from start of response
    print("Generated token IDs (sliced):", generated_ids)
    return tokenizer.decode(generated_ids, skip_special_tokens=True)

# Check CUDA
print("CUDA Available:", torch.cuda.is_available())
print("Device", torch.cuda.get_device_name(0))

# Test with a sample prompt
#prompt = "You are a helpful chatbot. Answer this: What is the capital of France?"
prompt = "<|im_start|>system\nYou are a helpful chatbot.<|im_end|>\n<|im_start|>user\nWhat is the capital of France?<|im_end|>\n<|im_start|>assistant"
response = generate_response(prompt)
print("Model response:", response)
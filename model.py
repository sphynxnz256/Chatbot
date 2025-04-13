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
    try:
        # Format promt in Qwen's chat template
        # Format prompt manually
        formatted_prompt = (
            f"<|im_start|>system\nYou are a helpful chatbot.<|im_end>\n"
            f"<|im_start|>user\n{prompt}<|im_end>\n"
            f"<|im_start|>assistant"
        )

        inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,          
        )

        # Decode and extract assistant's response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        # Extract text after <|im_start|>assistant and before <|im_end|>
        assistant_marker = "<|im_start|>assistant"
        end_marker = "<|im_end|>"
        if assistant_marker in full_response:
            # Get everything after assistant marker
            response = full_response.split(assistant_marker, 1)[1]
            # Trim at end marker if present
            if end_marker in response:
                response = response.split(end_marker, 1)[0]
            response = response.strip()
        else:
            response = full_response.strip()
        return response
    except Exception as e:
        return f"Error: {e}"

# Check CUDA
if torch.cuda.is_available():
    print("CUDA Available:", torch.cuda.is_available())
    print("Device", torch.cuda.get_device_name(0))
else:
    print("CUDA not availible.")
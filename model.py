import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import re

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
conversation_history = []
def generate_response(prompt):
    global conversation_history

    try:
        # Add the new user prompt to the conversation history
        conversation_history.append((f"user\n{prompt}"))

        # Start building the formatted prompt from the conversation history
        formatted_prompt = "<|im_start|>system\nYou are a helpful chatbot.<|im_end>\n"

        for item in conversation_history:
            formatted_prompt += f"<|im_start|>\n{item}<|im_end>\n"

        # Append assistant tag to indicate we're expecting its reply
        formatted_prompt += "<|im_start|>assistant"

        # Check token length, trim if too long
        max_tokens = 2048
        inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")        
        token_count = len(inputs['input_ids'][0])
        while token_count > max_tokens:
            # Remove the earliest prompt-response pair (first in history)
            conversation_history.pop(0)
            formatted_prompt = "<|im_start|>system\nYou are a helpful chatbot.<|im_end|>\n"
            for item in conversation_history:
                formatted_prompt += f"<|im_start|>{item}<|im_end>\n"
            formatted_prompt += f"<|im_start|>assistant"
            inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
            token_count = len(inputs['input_ids'][0])

        # Generate the model's response
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

        if assistant_marker in full_response:
            # Get text starting at the assistant marker
            response = full_response.split(assistant_marker, 1)[1]
            # Strip anything after the first <|im_end|>, even if there are multiple
            response = re.split(r"<\|im_end\|>", response, maxsplit=1)[0]
            response = response.strip()
        else:
            response = full_response.strip()

        # Add the assistant’s response to the conversation history
        conversation_history.append((f"assistant\n{response}"))

        return response
    except Exception as e:
        return f"Error: {e}"

# Check CUDA
if torch.cuda.is_available():
    print("CUDA Available:", torch.cuda.is_available())
    print("Device", torch.cuda.get_device_name(0))
else:
    print("CUDA not availible.")
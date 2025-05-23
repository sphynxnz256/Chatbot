import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import re

# Set up 4-bit quantization for memory efficiency
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# Manages the AI model, tokenizer, conversation history, and response generation.
# Implements a Singleton pattern to ensure only one instance exists.
class ModelManager:
    _instance = None
    MAX_CONTEXT_TOKENS = 8192

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelManager, cls).__new__(cls, *args, *kwargs)
        return cls._instance
    
    def __init__(self):
        # Prevents re-initialization if the instance already exists.
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        # Load model and tokenizer
        self.model_name = "Qwen/Qwen-7B-Chat"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            bf16=True,
        )

        # System prompt defines the bot's behavior
        self.system_prompt = (
            "You are an intelligent, friendly assistant who gives accurate, direct, and concise answers. "
            "You understand lighthearted, playful, or humorous questions and respond in kind without overreacting or moralizing. "
            "If a question is clearly hypothetical or imaginative, feel free to play along creatively unless it involves real harm. "
            "Avoid disclaimers about being an AI or lacking feelings unless the user directly asks. "
            "Never assume ill intent from the user unless explicitly stated. "
            "Prioritize clarity, logic, and relevance over excessive caution or warnings. "
            "When users present reasoning, engage with it step-by-step. "
            "Maintain a conversational tone. Be context-aware and avoid boilerplate responses even in long sessions. "
            "Above all, be helpful, sensible, and engaging without being defensive or overly formal."
        )

        self.conversation_history = []

    def set_history(self, history):
        self.conversation_history = history

    def get_history(self):
        return self.conversation_history
    
    def clear_history(self):
        self.conversation_history = []
    
    # Generates a response from the model based on the given prompt and current conversation history.
    # Manages context window by trimming old messages if necessary.
    def generate_response(self, prompt):
        try:
            # Add the new user prompt to the conversation history
            self.conversation_history.append((f"user\n{prompt}"))

            # Helper function to build the formatted prompt and count its tokens.
            def _build_and_count_prompt(history):
                prompt_list = [f"<|im_start|>system\n{self.system_prompt}<|im_end>"]
                for item in history:
                    prompt_list.append(f"<|im_start|>\n{item}<|im_end>")
                formatted_prompt = "".join(prompt_list) + "<|im_start|>assistant"
                inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
                token_count = len(inputs['input_ids'][0])

                return formatted_prompt, token_count
            
            formatted_prompt, token_count = _build_and_count_prompt(self.conversation_history)

            # Trim conversation history from the earliest entries if it exceeds MAX_CONTEXT_TOKENS.
            while token_count > self.MAX_CONTEXT_TOKENS:
                # Remove the earliest prompt-response pair (first in history).
                # This assumes history is always added in pairs or at least oldest first.
                self.conversation_history.pop(0)
                formatted_prompt, token_count = _build_and_count_prompt(self.conversation_history)

            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to("cuda")

            # Generate the model's response
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,          
            )

            # Decode and extract assistant's response from the full model output.
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)

            # Extract text after <|im_start|>assistant and before <|im_end|>
            assistant_marker = "<|im_start|>assistant"

            if assistant_marker in full_response:        
                response = full_response.split(assistant_marker, 1)[1]
                response = re.split(r"<?\|im_end\|>", response, maxsplit=1)[0]
                response = response.strip()
            else:
                response = full_response.strip()

            # Add the assistant’s response to the conversation history
            self.conversation_history.append((f"assistant\n{response}"))

            return response
        except Exception as e:
            return f"Error: {e}"
        
model_manager = ModelManager()

# Check CUDA
if torch.cuda.is_available():
    print("CUDA Available:", torch.cuda.is_available())
    print("Device", torch.cuda.get_device_name(0))
else:
    print("CUDA not availible.")
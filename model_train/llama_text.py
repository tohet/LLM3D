from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

device = torch.device("cuda")

tokenizer = AutoTokenizer.from_pretrained("D:/diploma/trainer_output/checkpoint-177", trust_remote_code=True) # "D:/diploma/LongWriter/LongWriter/train/output/llama3/longwriter"
model = AutoModelForCausalLM.from_pretrained("D:/diploma/trainer_output/checkpoint-177", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="cuda") # "D:/diploma/LongWriter/LongWriter/train/output/llama3/longwriter"
model = model.eval()
query = """
Create a 3D model of a hammer that has at least 332 polygons.
Write coordinates of verteces and vertex definitions of polygons in the following format:
verts = [(-1.001, -1.043, 0.031), (1.123, -1.441, 0.124), (-1.124, 1.655, 1.331), (1.433, 1.1, 0.009), ...]
faces = [[0, 1, 3, 2], ... ]
where verts is a python list of tuples of x, y, z coordinates in 3D space and faces is a list of indeces for the verts list. write only the coordinates and face definitions and absolutely nothing else. Create as many verteces and as many polygons as possible. model as many parts of an object as possible.
"""
prompt = f"[INST]{query}[/INST]"
input = tokenizer(prompt, truncation=False, return_tensors="pt").to(device)
context_length = input.input_ids.shape[-1]
print("started generating output")
output = model.generate(
    **input,
    max_new_tokens=32768,
    num_beams=1,
    do_sample=True,
    temperature=0.5,
)[0]
response = tokenizer.decode(output[context_length:], skip_special_tokens=True)
print(response)
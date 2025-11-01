from huggingface_hub import snapshot_download

# base model
snapshot_download("Soul-AILab/SoulX-Podcast-1.7B", local_dir="pretrained_models/SoulX-Podcast-1.7B")

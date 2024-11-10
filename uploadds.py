from datasets import load_dataset

dataset = load_dataset("images", data_dir=".")

print(dataset["train"]["image_id"])
# dataset.push_to_hub("arfrie22/metric-screw-image-classification")
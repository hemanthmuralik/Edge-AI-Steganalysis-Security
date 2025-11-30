# Example usage (Linux / macOS)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate dataset (2000 images total)
python dataset_gen.py --outdir ./data --num 2000

# Train quickly for a few epochs
python train.py --data ./data --epochs 8 --batch_size 64 --model_out model.h5

# Run detection on a single image
python detect.py --model model.h5 --image ./data/clean/0000.png

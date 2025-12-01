# train_pruned.py
import tensorflow_model_optimization as tfmot
import tensorflow as tf
from train import create_edge_model, HPFLayer # Import your existing model logic

# 1. Load your trained model
model = create_edge_model()
model.load_weights('edge_stego_model.h5')

# 2. Define Pruning Parameters
# This tells TF to start with 50% sparsity and go up to 80% (remove 80% of connections!)
pruning_params = {
    'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.50,
        final_sparsity=0.80,
        begin_step=0,
        end_step=1000
    )
}

# 3. Wrap the model to make it "Prunable"
model_for_pruning = tfmot.sparsity.keras.prune_low_magnitude(model, **pruning_params)

# 4. Fine-tune the model (Retrain it slightly so it adjusts to missing connections)
model_for_pruning.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_for_pruning.fit(
    train_images, train_labels, # You need to load your data here
    epochs=2,
    callbacks=[tfmot.sparsity.keras.UpdatePruningStep()]
)

# 5. Strip the pruning wrappers to save the final clean model
final_model = tfmot.sparsity.keras.strip_pruning(model_for_pruning)
final_model.save('pruned_stego_model.h5')

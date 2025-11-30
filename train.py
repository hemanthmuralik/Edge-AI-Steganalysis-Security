import os, argparse, numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, InputLayer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint

def build_model(input_shape=(32,32,3)):
    model = Sequential([
        InputLayer(input_shape=input_shape),
        Conv2D(32, (3,3), activation='relu', padding='same'),
        Conv2D(32, (3,3), activation='relu', padding='same'),
        MaxPooling2D(),
        Dropout(0.25),
        Conv2D(64, (3,3), activation='relu', padding='same'),
        MaxPooling2D(),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(1e-3), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def main(data_dir='./data', epochs=10, batch_size=64, model_out='model.h5'):
    clean_dir = os.path.join(data_dir, 'clean')
    stego_dir = os.path.join(data_dir, 'stego')
    if not os.path.exists(clean_dir) or not os.path.exists(stego_dir):
        raise RuntimeError('Data directories not found. Run dataset_gen.py first.')

    # Use ImageDataGenerator to stream images
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.15)

    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(32,32),
        batch_size=batch_size,
        class_mode='binary',
        subset='training',
        shuffle=True
    )
    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(32,32),
        batch_size=batch_size,
        class_mode='binary',
        subset='validation',
        shuffle=False
    )
    model = build_model((32,32,3))
    ckpt = ModelCheckpoint(model_out, save_best_only=True, monitor='val_accuracy', mode='max')
    model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=[ckpt])
    print('Training complete. Best model saved to', model_out)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='./data')
    p.add_argument('--epochs', type=int, default=8)
    p.add_argument('--batch_size', type=int, default=64)
    p.add_argument('--model_out', default='model.h5')
    args = p.parse_args()
    main(args.data, args.epochs, args.batch_size, args.model_out)

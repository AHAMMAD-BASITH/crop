import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go to root folder
train_dir = os.path.join(BASE_DIR, "indian crop", "Train")
val_dir = os.path.join(BASE_DIR, "indian crop", "Validation")

print("Train Directory:", train_dir)  # Debugging
print("Validation Directory:", val_dir)
# Set dataset paths


# Image Preprocessing
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, zoom_range=0.2)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(299, 299), batch_size=32, class_mode='categorical')

val_generator = val_datagen.flow_from_directory(
    val_dir, target_size=(299, 299), batch_size=32, class_mode='categorical')

# Load Pretrained Xception Model
base_model = Xception(weights='imagenet', include_top=False, input_shape=(299, 299, 3))
base_model.trainable = False  # Freeze base model

# Custom Model
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
x = Dense(len(train_generator.class_indices), activation='softmax')(x)  # Output layer

model = Model(inputs=base_model.input, outputs=x)

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Model
model.fit(train_generator, validation_data=val_generator, epochs=10)

# Save Model
model.save("xception_leaf_disease_model.h5")
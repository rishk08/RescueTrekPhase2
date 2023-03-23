import tensorflow as tf

# Check if GPU is available
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    print("GPU is available")
    print("GPU(s) details:")
    for device in physical_devices:
        print(f"- {device}")
else:
    print("GPU is not available")

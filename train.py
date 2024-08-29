import os
import tensorflow as tf
from official.projects.movinet.modeling import movinet
from official.projects.movinet.modeling import movinet_model
from official.projects.movinet.tools import export_saved_model
import argparse
import dataloader
import logging
import tensorflow_addons as tfa
import pathlib
from contextlib import contextmanager


"""
python3 train.py -id a1 -c '2,3' --lr 0.0005 --b 16 -g 2 -d 0.5
"""


logging.getLogger('absl').setLevel(logging.ERROR)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cuda", type=str, default='0',
                help="CUDA_VISIBLE_DEVICES")
ap.add_argument("-id", "--model_id", type=str, default='a2',
                help="model type, eg: a2")

ap.add_argument("-b", "--batch_size", type=int, default=8,
                help="batch_size")
ap.add_argument("-l", "--lr", type=float, default=0.0001,
                help="initial learning rate")
ap.add_argument("-g", "--gamma", type=float, default=2.0,
                help="focal loss gamma")
ap.add_argument("-d", "--dropout", type=float, default=0.0,
                help="dropout rate")
ap.add_argument("-sd", "--stochastic_depth_drop_rate", type=float, default=0.0,
                help="stochastic_depth_drop_rate")
ap.add_argument("-r", "--regularizer", type=str, default=None,
                help="regularizer: None, l2")

ap.add_argument("-t", "--train_data_path", type=str,
                help="path to data dir", default='data/V1.2/train')
ap.add_argument("-i", "--test_data_path", type=str,
                help="path to data dir", default='data/V1.2/test')
ap.add_argument("-n", "--num_frames", type=int, default=16,
                help="num_frames")
ap.add_argument("-s", "--resolution", type=int, default=224,
                help="video resolution")
ap.add_argument("-e", "--num_epochs", type=int, default=10,
                help="number of training epochs")
ap.add_argument("--pre_ckpt", type=str, default='pretrain_k600/',
                help="path to pre-trained checkpoint dir")
ap.add_argument("--save_ckpt", type=str, default='checkpoint/ckpt-1',
                help="path to save trained checkpoint eg: checkpoints/ckpt-1")
ap.add_argument("--export", type=str, default='savedmodel/',
                help="path to export model")
ap.add_argument("-o", "--save", type=str, default='model.tflite',
                help="path to export tflite model")
ap.add_argument("-f", "--float", type=int, default=32,
                choices=[32, 16],
                help="model quantization")


args = vars(ap.parse_args())



os.environ['CUDA_VISIBLE_DEVICES'] = args['cuda']



gpus = tf.config.experimental.list_logical_devices("GPU")

if len(gpus) > 1:
    distribution_strategy = tf.distribute.MirroredStrategy([gpu.name for gpu in gpus])
    print('Running on multiple GPUs ', [gpu.name for gpu in gpus])
else:
    distribution_strategy = "none"
  


train_data_path = pathlib.Path(args['train_data_path'])
test_data_path = pathlib.Path(args['test_data_path'])

batch_size = args['batch_size']
num_frames = args['num_frames']

resolution = args['resolution']

model_id = args['model_id']
if model_id == "a2":
    resolution = 224

num_epochs = args['num_epochs']
lr = args['lr']
focal_loss_gamma = args['gamma']
dropout_rate = args['dropout']

regularizer = args['regularizer']

num_classes = 11

stochastic_depth_drop_rate = args['stochastic_depth_drop_rate']


result_path = f"results/{model_id}_b{batch_size}_lr{lr}_g{focal_loss_gamma}_d{dropout_rate}_sd{stochastic_depth_drop_rate}"

if regularizer is not None:
    result_path += "_l2"


# checkpoint_dir = f'movinet_{model_id}_stream'
pre_ckpt_dir = os.path.join(args['pre_ckpt'], f'movinet_{model_id}_stream/')
# checkpoint_path = f"movinet_{model_id}_stream_checkpoint1/ckpt-1"
save_ckpt_dir = os.path.join(result_path, args['save_ckpt'])
# saved_model_dir=f"my_model/movinet_{model_id}_stream_violance"
saved_model_dir = os.path.join(result_path, args['export'])
# path_save_tflite = 'model.tflite'
path_save_tflite = os.path.join(result_path, args['save'])

os.makedirs(result_path, exist_ok=True) 

output_signature = (tf.TensorSpec(shape = (None, None, None, 3), dtype = tf.float32),
                    tf.TensorSpec(shape = (), dtype = tf.int16))

print("\nLoading Datasets...")
train_dataset = dataloader.create_complete_dataset(train_data_path, resolution=resolution, augmentation=True, batch_size=batch_size, oversample=True, target_samples_per_class=120, shuffle=True)
test_dataset = dataloader.create_complete_dataset(test_data_path, resolution=resolution, batch_size=batch_size, oversample=False, shuffle=False)


# for frames, labels in train_dataset.take(10):
#     print(labels)

#     print(f"Shape: {frames.shape}")
#     print(f"Label: {labels.shape}")


tf.keras.backend.clear_session()

print("\nBuilding stream model...")

@contextmanager
def optional_strategy_scope(strategy, condition):
    """Context manager to conditionally apply a distribution strategy."""
    if condition:
        with strategy.scope():
            yield
    else:
        yield

with optional_strategy_scope(distribution_strategy, len(gpus) > 1):

    backbone = movinet.Movinet(
        model_id=model_id,
        causal=True,
        conv_type='2plus1d',
        se_type='2plus3d',
        activation='hard_swish',
        gating_activation='hard_sigmoid',
        use_external_states=False,
        # kernel_regularizer=regularizer,
        stochastic_depth_drop_rate=stochastic_depth_drop_rate
    )
    backbone.trainable = True # !!

    model = movinet_model.MovinetClassifier(
        backbone, num_classes=600)

    inputs = tf.ones([1, num_frames, resolution, resolution, 3])
    model.build(inputs.shape)


    checkpoint_path = tf.train.latest_checkpoint(pre_ckpt_dir)
    checkpoint = tf.train.Checkpoint(model=model)
    status = checkpoint.restore(checkpoint_path)
    status.assert_existing_objects_matched()

    def build_classifier(batch_size, num_frames, resolution, backbone, num_classes, freeze_backbone=False):
        """Builds a classifier on top of a backbone model."""
        model = movinet_model.MovinetClassifier(
            backbone=backbone,
            num_classes=num_classes,
            dropout_rate=dropout_rate)
        model.build([batch_size, num_frames, resolution, resolution, 3])

        return model


    model = build_classifier(batch_size, num_frames, resolution, backbone, num_classes)
    # model.summary()

    loss = tfa.losses.SigmoidFocalCrossEntropy(from_logits = True, alpha = 0.25, gamma = focal_loss_gamma, name = 'sigmoid_focal_crossentropy', reduction=tf.keras.losses.Reduction.AUTO)
    
    train_steps = 5600 // batch_size
    total_train_steps = train_steps * num_epochs

    lr_scheduler = tf.keras.optimizers.schedules.CosineDecay(initial_learning_rate=lr, decay_steps=total_train_steps, alpha=0.0, name='CosineDecay')
    optimizer = tf.keras.optimizers.Adam(learning_rate = lr_scheduler)

    model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy', tfa.metrics.F1Score(average='macro',num_classes=num_classes)])


    class LogMetricsCallback(tf.keras.callbacks.Callback):
        def __init__(self, optimizer, file_name='train.log'):
            super(LogMetricsCallback, self).__init__()
            self.file_name = file_name
            self.optimizer = optimizer
            if os.path.exists(self.file_name):
                os.remove(self.file_name)

        def on_epoch_end(self, epoch, logs=None):
            logs = logs or {}
            if callable(self.optimizer.learning_rate):
                current_lr = self.optimizer.learning_rate(self.optimizer.iterations)
            else:
                current_lr = self.optimizer.learning_rate

            with open(self.file_name, 'a') as log_file:
                log_file.write(f"Epoch {epoch + 1}\n")
                log_file.write(f"Learning Rate: {current_lr:.12e}\n")
                for metric, value in logs.items():
                    log_file.write(f"{metric}: {value:.4f}\n")
                log_file.write("\n")



    print("Start Training!")

    results = model.fit(train_dataset,
                        validation_data=test_dataset,
                        epochs=num_epochs,
                        validation_freq=1,
                        callbacks=[tf.keras.callbacks.ModelCheckpoint(filepath=f"{result_path}/checkpoint/cp.ckpt"
                                            ,save_weights_only=True, monitor='val_accuracy', mode='max', save_best_only=True),
                                LogMetricsCallback(optimizer=optimizer, file_name=f'{result_path}/train.log'),
                                tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=4)],
                        verbose=1)

print(results.history)
model.trainable = False # !!


print("Building stream model...")

weights=model.get_weights()
input_shape = [1, 1, resolution, resolution, 3]

tf.keras.backend.clear_session()

stream_backbone = movinet.Movinet(
    model_id=model_id,
    causal=True,
    conv_type='2plus1d',
    se_type='2plus3d',
    activation='hard_swish',
    gating_activation='hard_sigmoid',
    use_external_states=True
    )

stream_backbone.trainable=False
stream_model = movinet_model.MovinetClassifier(
    backbone=stream_backbone,
    num_classes=num_classes,
    output_states=True)


inputs = tf.ones([1, num_frames, resolution, resolution, 3])
stream_model.build(inputs.shape)

stream_model.set_weights(weights)
stream_model.get_weights()[0] 
model.get_weights()[0]


# Export Model
export_saved_model.export_saved_model(
    model=stream_model,
    input_shape=input_shape,
    export_path=saved_model_dir,
    causal=True,
    bundle_input_init_states_fn=True)
print(f'[INFO] Exported model: {saved_model_dir}')

# To TFLite
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
# if args['float'] == 16:
#     converter.optimizations = [tf.lite.Optimize.DEFAULT]
#     converter.target_spec.supported_types = [tf.float16]
tflite_model = converter.convert()
with open(path_save_tflite, 'wb') as f:
    f.write(tflite_model)
print(f'[INFO] Saved TFLite model to : {path_save_tflite}')

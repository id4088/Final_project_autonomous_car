import os
import random
import fnmatch
import datetime
import pickle

#data processing
import numpy as np
np.set_printoptions(formatter={'float_kind : lambda x: "%.4f' })

import pandas as pd
pd.set_option('display.width',320)
pd.set_option('display.float_format','{:,.4f}'.format)
pd.set_option('display.max_colwidth',160)

#tensorflow
import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPool2D,Dropout,Flatten,Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

print(f'tf.__version__: {tf.__version__}')
print(f'.keras.__version__: {tensorflow.keras.__version__}')

#sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#imaging
import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#matplotlib inline
from PIL import Image

def my_imread(image_path):
    image = cv2.imread(image_path)
    return image

def img_preprocess(image):
    image = image/255
    return image

def nvidia_model():
    model = Sequential(name ='Nvidia_Model')

    model.add(Conv2D(24,(5,5),strides=(2,2), input_shape=(80, 320,), activation ='elu'))
    model.add(Conv2D(36,(5,5),strides=(2,2), activation ='elu'))
    model.add(Conv2D(48,(5,5),strides=(2,2), activation ='elu'))
    model.add(Conv2D(64,(5,5), activation ='elu'))
    model.add(Dropout(0.2))
    model.add(Conv2D(64, (3,3), activation ='elu'))

    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))

    model.add(Dense(1))

    # Cus_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='mse', optimizer='adam')

    return model

def image_data_generator(image_paths, steering_angles, batch_size):
    while True:
        batch_images =[]
        batch_steering_angles = []

        for i in range(batch_size):
            random_index = random.randint(0,len(image_paths)-1)
            image_path = image_paths[random_index]
            image = my_imread(image_paths[random_index])
            steering_angle = steering_angles[random_index]

            image = img_preprocess(image)
            batch_images.append(image)
            batch_steering_angles.append(steering_angle)

        yield(np.asarray(batch_images),np.asarray(batch_steering_angles))



data_dir = "C:\\Users\\KOSTA\\tensorflow\\video"
file_list = os.listdir(data_dir)
image_paths=[]
steering_angle =[]
pattern = "*png"
for filename in file_list:
    if fnmatch.fnmatch(filename,pattern):
        image_paths.append(os.path.join(data_dir,filename))
        angle = int(filename[-7:-4])
        steering_angle.append(angle)

image_index =10
plt.imshow(Image.open(image_paths[image_index]))
print("image_path: %s" %image_paths[image_index])
print("steering_Angle: %d" %steering_angle[image_index])
Image_change_Angle = pd.DataFrame()
Image_change_Angle['ImagePath'] = image_paths
Image_change_Angle['Angle'] = steering_angle

num_of_bins = 25
hist, bins = np.histogram(Image_change_Angle['Angle'],num_of_bins)

# fig, axes = plt.subplots(1,1,figsize=(12,4))
# axes.hist(Image_change_Angle['Angle'],bins=num_of_bins,width=1,color='blue')

##plt.show()

X_train, X_valid, y_train, y_valid = train_test_split( image_paths, steering_angle, test_size=0.2)
print("Trainin data: %d\n Validation data: %d" %(len(X_train), len(X_valid)))

# fig, axes = plt.subplots(1,2,figsize =(12,4))
# axes[0].hist(y_train,bins = num_of_bins, width=1,color ='blue')
# axes[0].set_title('Training Data')
# axes[1].hist(y_valid, bins = num_of_bins, width =1, color = 'red')
# axes[1].set_title('Validation Data')


# fig, axes = plt.subplots(1, 2,figsize=(15,10))
# image_orig = my_imread(image_paths[image_index])
# image_processed = img_preprocess(image_orig)

# axes[0].imshow(image_orig)
# axes[0].set_title("orig")
# axes[1].imshow(image_processed)
# axes[1].set_title("processed")

model =nvidia_model()
print(model.summary())
#plt.show()

ncol =2
nrow =2

X_train_batch,y_train_batch =next(image_data_generator(X_train,y_train,nrow))
X_valid_batch,y_valid_batch =next(image_data_generator(X_valid,y_valid,nrow))

fig, axes =plt.subplots(nrow,ncol,figsize=(15,6))
fig.tight_layout()

for i in range(nrow):
    axes[i][0].imshow(X_train_batch[i])
    axes[i][0].set_title("traing, angle=%s" % y_train_batch[i])
    axes[i][1].imshow(X_valid_batch[i])
    axes[i][1].set_title("validation, angle=%s" % y_valid_batch[i])

model_output_dir = 'C:\\Users\\KOSTA\\tensorflow\\AI_data'

checkpoint_callback = tensorflow.keras.callbacks.ModelCheckpoint(filepath=os.path.join(model_output_dir,'lane_navigation_check.h5'),verbose=1,save_best_only=True)

history = model.fit_generator(image_data_generator(X_train,y_train, batch_size =100),steps_per_epoch=300,epochs=20,validation_data=image_data_generator(X_valid,y_valid,batch_size=100),validation_steps=200,verbose=1,shuffle=1,callbacks=[checkpoint_callback])

model.save(os.path.join(model_output_dir,'lane_navigation_final.h5'))

history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path,"wb") as f:
    pickle.dump(history.history,f,pickle.HIGHEST_PROTOCOL)


from sklearn.metrics import mean_squared_error, r2_score

history.history

history_path = os.path.join(model_output_dir,'history.pickle')
with open(history_path,'rb') as f:
    history = pickle.load(f)

history
plt.plot(history['loss'],color='blue')
plt.plot(history['val_loss'],color = 'red')
plt.legend(['training loss', 'validation loss'])

def summarize_prediction(Y_true,Y_pred):

    mse = mean_squared_error(Y_true,Y_pred)
    r_squared = r2_score(Y_true,Y_pred)

    print(f' mse = {mse:.2}')
    print(f' r_squared = {r_squared:.2%}')
    print()

def predict_and_summarize(X,Y):
    model = load_model(f' {model_output_dir}/lane_navigation_check.h5')
    Y_pred = model.predict(X)
    summarize_prediction(Y,Y_pred)
    return Y_pred

n_tests =100
X_test,y_test = next(image_data_generator(X_valid,y_valid, 100))

y_pred = predict_and_summarize(X_test,y_test)

n_tests_show =2
fig, axes = plt.subpplots(n_tests_show,1,figsize(10,4*n_tests_show))

for i in range(n_tests_show):
    axes[i].imshow(X_test[i])
    axes[i].set_title(f' actual angle={y_test[i]}, predicted angle ={int(y_pred[i])}, diff ={int(y_pred[i])-y_test[i]}')

plt.show()

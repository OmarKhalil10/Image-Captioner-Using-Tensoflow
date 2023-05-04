# Image-Captioner-Using-Tensoflow

## To add a new page
* Create the html, css, js in the specified folder using the same folder structure.
* Create a new route in the [app.py](./app.py) file with the name you want using only dashes to seperate words.
```PYTHON
@app.route('NEW-ROUTE')
```
* Define your serving function using a unique name not used before in the whole application.
```PYTHON
def NEW_UNIQUE_NAME():
```
* Return your html file path using render_template.
```PYTHON
return render_template('FOLDER_PATH/FILE_PATH.html')
```
* Your newely created route should look like this.
```PYTHON
@app.route('NEW-ROUTE')
def NEW_UNIQUE_NAME():
    return render_template('FOLDER_PATH/FILE_PATH.html')
```

## Initialize and activate a virtualenv using
```
python -m virtualenv venv
source venv/Scripts/activate
```
## to deactivate 
```
deactivate
```
## Install the dependencies
```
pip install -r requirements.txt
```
## To run the development server

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=true
flask run --reload
```

## Flickr8K Image Captioning using CNNs+LSTMs
### Flickr8k dataset

The Flickr8k dataset is a collection of images and their corresponding captions. It was created for the purpose of evaluating image captioning algorithms. The dataset consists of 8,000 images, each with five captions that describe the image. The images were collected from the photo-sharing website Flickr and cover a wide range of scenes, objects, and activities.


The Flickr8k dataset is widely used in the research community as a benchmark for evaluating image captioning algorithms. It has been used in many research papers to evaluate the performance of different approaches to image captioning. The dataset has also been used to train deep learning models for image captioning.

The dataset is available for download from the website of the University of Illinois at Urbana-Champaign. The website provides links to the images and captions, as well as the code for downloading and processing the dataset. It is important to note that the use of the Flickr8k dataset is subject to the terms and conditions set by Flickr and the University of Illinois at Urbana-Champaign.

### Download links:

[Filckr8k_dataset](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip)

[Flickr8k_text](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip)

### What is Image Captioning ?

* Image Captioning is the process of generating textual description of an image. It uses both Natural Language Processing and Computer Vision to generate the captions.
* This task lies at the intersection of computer vision and natural language processing. Most image captioning systems use an encoder-decoder framework, where an input image is encoded into an intermediate representation of the information in the image, and then decoded into a descriptive text sequence.
**CNNs + RNNs (LSTMs)**

* To perform Image Captioning we will require two deep learning models combined into one for the training purpose
* CNNs extract the features from the image of some vector size aka the vector embeddings. The size of these embeddings depend on the type of pretrained network being used for the feature extraction
* LSTMs are used for the text generation process. The image embeddings are concatenated with the word embeddings and passed to the LSTM to generate the next word
* For a more illustrative explanation of this architecture check the Modelling section for a picture representation

![data_sample](/documentation/images/data_sample.png)

### Caption Text Preprocessing Steps

* Convert sentences into lowercase
* Remove special characters and numbers present in the text
* Remove extra spaces
* Remove single characters
* Add a starting and an ending tag to the sentences to indicate the beginning and the ending of a sentence

### Tokenization and Encoding

* The words in a sentence are separated/tokenized and encoded in a one hot representation
* These encodings are then passed to the embeddings layer to generate word embeddings

![lookup_table](/documentation/images/lookup_table.gif)

### Image Feature Extraction

* DenseNet 201 Architecture is used to extract the features from the images
* Any other pretrained architecture can also be used for extracting features from these images
* Since the Global Average Pooling layer is selected as the final layer of the DenseNet201 model for our feature extraction, our image embeddings will be a vector of size 1920

![Image Feature Extraction](/documentation/images/Image%20Feature%20Extraction.png)

### Data Generation
* Since Image Caption model training like any other neural network training is a highly resource utillizing process we cannot load the data into the main memory all at once, and hence we need to generate the data in the required format batch wise
* The inputs will be the image embeddings and their corresonding caption text embeddings for the training process
* The text embeddings are passed word by word for the caption generation during inference time


### Modelling
* The image embedding representations are concatenated with the first word of sentence ie. starseq and passed to the LSTM network
* The LSTM network starts generating words after each input thus forming a sentence at the end

![flickr8k_model](/documentation/images/model.png)

### Model Modification
* A slight change has been made in the original model architecture to push the performance. The image feature embeddings are added to the output of the LSTMs and then passed on to the fully connected layers
* This slightly improves the performance of the model orignally proposed back in 2014: [Show and Tell: A Neural Image Caption Generator](https://arxiv.org/pdf/1411.4555.pdf)

### Train
Configure and execute the training for **100** epochs

![model_training](/documentation/images/train.gif)

### Learning Curves

### Loss Curve
![loss_curve](/documentation/images/loss.png)

### Accuracy Curve
![accuracy_curve](/documentation/images/accuracy.png)

### Result

![result](/documentation/images/result.png)

### Conclusion

This may not be the best performing model, but the objective of this kernel is to give a gist of how Image Captioning problems can be approached. In the future work of this kernel Attention model training with Flickr30k dataset will be performed.
## vit-gpt2-image-captioning

The ViT (Vision Transformer) and GPT-2 (Generative Pre-trained Transformer 2) are two different types of transformer-based models, with ViT being primarily used for computer vision tasks and GPT-2 being primarily used for natural language processing tasks. While both models share similar transformer-based architectures, their input and output formats are quite different, and therefore it is not straightforward to convert a ViT model to a GPT-2 model.


To create an encoder-decoder model that can generate text from images, one possible approach would be to use a combination of both models, where the ViT model is used to encode the input image and produce a vector representation of the visual features, which is then passed to the GPT-2 decoder model to generate text based on the encoded visual information.


This can be achieved by fine-tuning a pre-trained GPT-2 model on a dataset of paired image and text data, where the ViT model is used to extract the visual features from the images and the text is used as the decoder output. During training, the GPT-2 model learns to generate text that is conditioned on the visual features encoded by the ViT model.


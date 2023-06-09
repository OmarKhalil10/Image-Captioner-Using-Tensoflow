# Image-Captioner-Using-Tensoflow

## To run the application
### Initialize and activate a virtualenv using
```
python -m virtualenv venv
source venv/Scripts/activate
```
### to deactivate
```
deactivate
```
### Install the dependencies
```
pip install -r requirements.txt
```
## run the development server

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


Flickr30k Image Caption Generator is a deep learning-based model that generates natural language captions for images in the Flickr30k dataset. The model uses a convolutional neural network (CNN) to extract features from the images and a recurrent neural network (RNN) to generate captions.

## Flickr30k Image Captioning using CNNs+LSTMs

### Flickr30k dataset

The [Flickr30k dataset](https://arxiv.org/abs/1505.04870) contains **31,783** images, each with five reference captions. The dataset is split into a training set of **29,000** images and a validation set of **1,000** images, with the remaining images held out for testing.

To train the image caption generator, the CNN extracts features from the images, which are then fed into an RNN. The RNN generates a sequence of words, one at a time, by predicting the probability distribution over the vocabulary at each time step. The model is trained using a combination of cross-entropy loss and reinforcement learning to optimize the generated captions.

The Flickr30k Image Caption Generator has achieved state-of-the-art performance on the Flickr30k dataset, with a BLEU score of 59.6 on the test set. This indicates that the generated captions are highly similar to the reference captions provided for each image.

Overall, the Flickr30k Image Caption Generator is a powerful tool for automatically generating natural language descriptions of images, which has many potential applications in areas such as image search, image retrieval, and image understanding.

### Download links:

[Flickr30k dataset](https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset/download?datasetVersionNumber=1)

### Modelling
The model is based on encoder-decoder architecture. A two-dimensional convolutional neural network is used to encode the image features, and a one-dimensional
convolutional neural network is used to encode the word sequences of the caption data. Later, both the encoded image and text features are merged and passed
to a decoder to predict the caption in a word by word manner.

![model](/documentation/images/flickr30k/model.png)

### The model is divided into three parts

1. **Image Feature Encoder:** We used pre-trained ResNet-50 as image feature extractor. It is trained on ImageNet dataset. Traditionally, neural networks with many layers tend to perform well in recognizing patterns. However, they also suffer from overfitting issues and are not easy to optimize.
Residual CNNs are designed to have shortcut connections between layers. These connections perform identity mapping. ResNets are easy to optimize, and their performance increase with increasing network depth. We discard the final output layer of the ResNet-50 as it contains the output of image
classification and used only the encoded image features produced by the hidden layers.

2. **Word Sequence Encoder:** Two-dimensional convolutional neural networks have been extensively used in pattern recognition, image classification, and time series forecasting. The same property of these networks can be used in sequence processing. In our model, we used one-dimensional CNN for extracting one-dimensional patches from a sequence of words. The CNN has 512 filters with a kernel size of 3. The activation used is Rectified Linear Units(ReLU). The CNN is followed by a Global Max Pooling Layer, which captures critical features from the convolutional layer’s output.

3. **Caption Generator:** The caption generator is a simple decoder containing a Dense 512 layer with ReLU activation. The output of the image feature encoder and word sequence encoder are combined by concatenation and used as input to the dense layer. The dense layer generates a softmax prediction for each word in the vocabulary to be the next word in the sequence, and the word with the highest probability is selected. This process continues until an ending token is generated.

The caption generator’s output is transformed into a probability score for each word in the vocabulary. The greedy method chooses the word with the highest probability for each time step. This method may not always provide the best
possible caption as any word’s prediction depends on all the previously predicted words. So, it is more efficient to select the sequence with the highest overall score from a candidate of sequences. So we use the beam search technique with a beam size of 5. It considers the top 5 candidate words at the first decode step. For each of the first words, it generates five-second words and chooses the top five combinations of first and second words based on the additive score. After the termination of five sequences, the sequence with the best overall score is selected. This method allows the process to be flexible and generate consistent
results

### Quantitative analysis of performances among different models

![search-alg-comp](/documentation/images/test_analysis.png)


### Result and Analysis
## vit-gpt2-image-captioning

![thanos](/documentation/images/thanos.gif)

The ViT (Vision Transformer) and GPT-2 (Generative Pre-trained Transformer 2) are two different types of transformer-based models, with ViT being primarily used for computer vision tasks and GPT-2 being primarily used for natural language processing tasks. While both models share similar transformer-based architectures, their input and output formats are quite different, and therefore it is not straightforward to convert a ViT model to a GPT-2 model.


To create an encoder-decoder model that can generate text from images, one possible approach would be to use a combination of both models, where the ViT model is used to encode the input image and produce a vector representation of the visual features, which is then passed to the GPT-2 decoder model to generate text based on the encoded visual information.


This can be achieved by fine-tuning a pre-trained GPT-2 model on a dataset of paired image and text data, where the ViT model is used to extract the visual features from the images and the text is used as the decoder output. During training, the GPT-2 model learns to generate text that is conditioned on the visual features encoded by the ViT model.

### A comparison of the used datasets

![comparison](/documentation/images/flickr30k/comparison-30k-8k.png)

## Searching Algorithm Used
### Greedy Search algorithm

Initialize the algorithm by setting the initial image as the input and an empty caption as the output.
Define a language model that assigns a probability score to each possible word in the vocabulary given the current input image and the previous words in the caption.
Loop until a stopping condition is reached (e.g., a maximum caption length is reached or the probability score falls below a certain threshold):

* Calculate the probability score for each possible word in the vocabulary given the current input image and the previous words in the caption.
* Select the word with the highest probability score as the next word in the caption.
* Update the input image by encoding the current caption using an image encoder.
* Add the selected word to the caption and repeat the loop.
* Return the final caption as the output.

![caption](/documentation/images/greedy.png)

## Sequence Model
![sequence_model](/documentation/images/sequence_model.png)

## Reimplementation
We do not intend to reimplement a proven solution for image captioning, as we aim to create our own solution that is unique and tailored to the specific needs of our users. However, we will draw inspiration from existing solutions and use their techniques as a foundation for building our own model. We will also evaluate our model against existing solutions to ensure that it performs at least as well as the state-of-the-art.

### Future Work

- [ ] The reset function accelerate the _ in the caption --> find the root cause and solve it 
- [ ] Fix the responsible view in caption and home pages
- [ ] Fix the Burger icon --> it does't expand
- [ ] Fix the spacing between input and output in the caption page
- [ ] Find the correct way to display the effect of dark/light theme
- [ ] Try to make the sizing between the i/p and o/p suitable
- [ ] Modify the requirements file (transformers,torch)
- [ ] Modify Radio Buttons in Caption page
- [ ] Launch demo model Button caption page Put onboard description
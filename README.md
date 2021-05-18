# Neural Language Models trained on Brown Corpus

### Methodology
- The brown dataset contains about 99007 lines
- Data is preprocessed and cleaned and split into train and test set
- Input is encoded to integers and then one hot encoded using Keras to_categorical()
- A stacked LSTM architecture is used
- ‘Categorical cross entropy’ loss is used as this is a multi-class classification and Adam optimiser is used which is efficient. The model is fit on the data for 10 training epochs
- Analysed using perplexity scores and compared with statistical models

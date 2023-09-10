Book Recommendation System
==========================

A recommendation system built using the Funk SVD model to suggest books based on user ratings.

Overview
--------

*   **Model**: Funk SVD
*   **Dataset**: [Book Recommendation Dataset from Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
*   **Key Metrics**: RMSE (achieved ~3.455943 in tests)

Getting Started
---------------

### Prerequisites

Ensure you have the following installed:

*   Python 3.x
*   Streamlit
*   Surprise library
*   PyYAML

### Dataset and Model Setup

Due to the large size of the dataset and model files:

1.  Download the dataset files from the [Kaggle link](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) and place them inside a folder named `dataset` in the project directory.
    
2.  Before running the Streamlit app, execute the `main.ipynb` notebook. This will generate the necessary model files. Note: You can skip the hyperparameter tuning process in the notebook as it is time-consuming.
    
### Running the Model

1.  Clone the repository:

bash

```bash
git clone https://github.com/haranobuhardo/surprise-svd-book-recommendation-system
```

2.  Navigate to the project directory:

bash

```bash
cd surprise-svd-book-recommendation-system
```

3.  Run the Streamlit app:

bash

```bash
streamlit run app.py
```

This will launch a web application where you can test the recommendation system.

Deployment
----------

The model can be deployed using Streamlit for real-time book recommendations. Ensure you have Streamlit installed and simply run the provided `app.py` to start the server and interact with the model.

Report
---------
For a detailed report on the project, check out the article: [Recommendation System: Harnessing Machine Learning for Enhanced Book Recommendations (Medium)](https://medium.com/@haranobuhardo/recommendation-system-harnessing-machine-learning-for-enhanced-book-recommendations-3e32680447a5)
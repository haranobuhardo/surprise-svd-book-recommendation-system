import streamlit as st
import src.util as utils
import pandas as pd

config = utils.load_config()

svd_model = utils.pickle_load(config['svd_model_path'])
rating_data = pd.read_csv(config['ratings_dataset_path'])
book_data = pd.read_csv(config['book_dataset_path'], usecols=range(5), dtype={3: str}, index_col='ISBN')
user_data = pd.read_csv(config['users_dataset_path'])

rating_data.columns=['user_id','item_id','rating']
book_data.columns = ['title', 'author', 'year', 'publisher']


# Let's create a function
def get_unrated_item(userid, rating_data):
    """
    Get unrated item id from a user id

    Parameters
    ----------
    userid : int
        The user id

    rating_data : pandas DataFrame
        The rating data

    Returns
    -------
    unrated_item_id : set
        The unrated item id
    """
    # Find the whole item id
    unique_item_id = set(rating_data['item_id'])

    # Find the item id that was rated by user id
    rated_item_id = set(rating_data.loc[rating_data['user_id']==userid, 'item_id'])

    # Find the unrated item id
    unrated_item_id = unique_item_id.difference(rated_item_id)

    return unrated_item_id


# Let's create this into a function
def get_pred_unrated_item(userid, estimator, unrated_item_id):
    """
    Get the predicted unrated item id from user id

    Parameters
    ----------
    userid : int
        The user id

    estimator : Surprise object
        The estimator

    unrated_item_id : set
        The unrated item id

    Returns
    -------
    pred_data : pandas Dataframe
        The predicted rating of unrated item of user id
    """
    # Initialize dict
    pred_dict = {
        'user_id': userid,
        'item_id': [],
        'predicted_rating': []
    }

    # Loop for over all unrated movie Id
    for id in unrated_item_id:
        # Create a prediction
        pred_id = estimator.predict(uid = pred_dict['user_id'],
                                    iid = id)

        # Append
        pred_dict['item_id'].append(id)
        pred_dict['predicted_rating'].append(pred_id.est)

    # Create a dataframe
    pred_data = pd.DataFrame(pred_dict).sort_values('predicted_rating',
                                                     ascending = False)

    return pred_data

def get_top_highest_unrated(estimator, k, userid, rating_data, metadata):
    """
    Get top k highest of unrated movie from a Surprise estimator RecSys

    Parameters
    ----------
    estimator : Surprise model
        The RecSys model

    k : int
        The number of Recommendations

    userid : int
        The user Id to recommend

    rating_data : pandas Data Frame
        The rating data

    movie_data : pandas DataFrame
        The movie meta data

    Returns
    -------
    top_item_pred : pandas DataFrame
        The top items recommendations
    """
    # 1. Get the unrated item id of a user id
    unrated_item_id = get_unrated_item(userid=userid, rating_data=rating_data)

    # 2. Create prediction from estimator to all unrated item id
    predicted_unrated_item = get_pred_unrated_item(userid = userid,
                                                   estimator = estimator,
                                                   unrated_item_id = unrated_item_id)

    # 3. Filter out books that are not available in metadata
    available_books = predicted_unrated_item[predicted_unrated_item['item_id'].isin(metadata.index)]

    # 4. Sort & get top k books
    top_item_pred = available_books.head(k).copy()
    # top_item_pred = predicted_unrated_item.head(k).copy()

    # 5. Fetch book details from metadata
    top_item_pred_detail = metadata.loc[top_item_pred['item_id'], :]

    return top_item_pred_detail

# Streamlit app
st.title("Book Recommendation System")

# Input user ID
user_id = st.text_input("Enter User ID:")

# Button to get recommendations
if st.button("Get Recommendations"):
    print("button pressed!")
    recommendations = get_top_highest_unrated(estimator=svd_model,
                                              k=5,
                                              userid=int(user_id),
                                              rating_data=rating_data,
                                              metadata=book_data)
    print(recommendations)

    for _, row in recommendations.iterrows():
        st.write("### Title:", row['title'])
        st.write("Author:", row['author'])
        st.write("Year:", row['year'])
        st.write("Publisher:", row['publisher'])
        st.write("ISBN:", row.name)



# Credit
st.markdown("""
---
Made for **Pacman Recommendation System Class Final Project** by [haranobuhardo@gmail.com](mailto:haranobuhardo@gmail.com)
""")

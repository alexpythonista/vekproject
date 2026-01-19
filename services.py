import pandas as pd
from pathlib import Path

from constants import DataFields, FIELDS, FIELDS_TO_SORT, SORT_ORDER

current_dir = Path(__file__).resolve().parent
path = current_dir / 'data' / 'test.csv'


def get_raw_data(path=path):
    return pd.read_csv(path)


def get_data_by_user(data, user_id):
    """
    If user_id is a new user we return recommendations based on the whole data.
    If user_id is our current user we return recommendations based on current user history excluding
    products he has already purchased.
    """
    if user_id not in data[str(DataFields.UID)].values:
        return data
    else:
        return data[
            (data[DataFields.UID] == user_id) & (data[DataFields.PURCHASE] == 0)
            ]


def get_prepared_data(
        data, fields=FIELDS, fields_to_sort=FIELDS_TO_SORT, sort_order=SORT_ORDER, group=str(DataFields.BRAND)
):
    """
    We select the priority in sorting from values with more weight to values with less weight:
    'purchase' -> 'add_to_cart' -> 'click' in our case.
    Also, we ensure that the maximum quantity of the most popular products of each brand does not exceed 2 units:
    >> apply(lambda x: x.nlargest(2, ...)
    """
    prepared_data = (
        data[[*fields]]
        .groupby(group)
        .apply(lambda x: x.nlargest(2, [*fields_to_sort]), include_groups=False)
        .sort_values(
            by=[*fields_to_sort], ascending=sort_order
        )
    )
    return prepared_data


def get_recommendations(user_id, data_limit=5):
    raw_data = get_raw_data()
    user_data = get_data_by_user(raw_data, user_id)
    prepared_data = get_prepared_data(user_data)
    return prepared_data[str(DataFields.PID)].head(data_limit).tolist()

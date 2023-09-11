# import for only dag
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# data prep import
import pandas as pd

# train model import
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def data_prep(ti, path="/opt/airflow/data/Order.csv"):
    data = pd.read_csv(path, low_memory=False)
    # datetime convert
    data["Sales_Order_date"] = pd.to_datetime(data["Sales_Order_date"])
    data = data.groupby(["Customer_Code", "Sales_Order_date"])["Order_Amount"].sum().reset_index()
    # data sort and get date diff
    data.sort_values(["Customer_Code", "Sales_Order_date"], inplace=True)
    data["date_diff"] = data.groupby("Customer_Code")["Sales_Order_date"].diff().dt.days
    #  target data prepare
    data["next_buy"] = data.groupby("Customer_Code")["date_diff"].shift(-1)
    # remove date_diff and remove null
    data = data.drop(columns=["date_diff"])
    data = data.dropna()
    # date feature
    data["sales_day"] = data["Sales_Order_date"].dt.day
    data["sales_day_of_week"] = data["Sales_Order_date"].dt.dayofweek
    data["sales_month"] = data["Sales_Order_date"].dt.month
    data["sales_days_in_month"] = data["Sales_Order_date"].dt.days_in_month # number of days in that month
    # customer summary
    customer_order_summary = data.groupby("Customer_Code")["Order_Amount"].agg(["mean", "median", "max", "min"]).reset_index()
    customer_date_summary = data.groupby("Customer_Code")['next_buy'].agg(['mean', 'median', 'max', 'min']).reset_index()
    customer_date_summary = customer_date_summary.add_prefix('date_')
    customer_order_summary = customer_order_summary.add_prefix('order_')
    customer_summary = customer_date_summary.merge(
    customer_order_summary,
    right_on="order_Customer_Code",
    left_on="date_Customer_Code"
    )
    customer_summary = customer_summary.drop(columns=["date_Customer_Code"])
    print(customer_summary.head())
    # merge with orginal data
    data = data.merge(customer_summary, right_on="order_Customer_Code", left_on="Customer_Code")
    data = data.drop(columns=["order_Customer_Code"])
    print(data.head())
    data.to_csv("/opt/airflow/data/feature.csv", index=False)
    xcom_dict = {"feature_dir": "/opt/airflow/data/feature.csv"}
    ti.xcom_push(key="feature", value=xcom_dict)
    return True


def train(ti):
    x_com = ti.xcom_pull(key="feature")
    print(x_com)
    # error after adding customer summary
    feature = ["Order_Amount", "sales_day", "sales_day_of_week", "sales_month", "sales_days_in_month", "date_mean", "date_median",
               "date_max", "date_min", "order_mean", "order_median", "order_max", "order_min"]
    data = pd.read_csv(x_com.get("feature_dir"))

    x = data[feature]
    y = data["next_buy"]
    x_train, x_test, y_train, y_test = train_test_split(
            x, y, random_state=1, test_size=0.3,
            shuffle=True)
    del data
    model = LinearRegression()
    trained_model = model.fit(x_train, y_train)
    y_pred = trained_model.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"mae {mae} r2 {r2} ")
    return True


# dag code
next_buy = DAG(
    "next_buy",
    schedule_interval="0 12 * * *",
    start_date=datetime(2023, 9, 7)
)


with next_buy:
    data_preparation_task = PythonOperator(
        task_id="data_prep_task_id",
        python_callable=data_prep,
        provide_context=True
    )
    model_train_task = PythonOperator(
        task_id="model_train_task_id",
        python_callable=train,
        provide_context=True
    )

    data_preparation_task >> model_train_task
